import os
import httpx
import asyncio
import logging
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retry parameters
MAX_RETRIES = 3
TIMEOUT = 30  # seconds
CONCURRENCY_LIMIT = 50  # Max number of simultaneous requests

# Semaphore to limit concurrent downloads
semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

async def download_images_from_filtered_data(filtered_df, token: str, company_name: str):
    """
    Downloads images for each ID in the filtered DataFrame and saves them to the company's output folder.
    Handles retries, timeouts, and error logging.
    """
    api_endpoint = f'{settings.BASE_URL}/entity-service/entities'
    # Create company-specific output folder
    output_folder = os.path.join(settings.IMAGE_OUTPUT_PATH, company_name)
    os.makedirs(output_folder, exist_ok=True)

    async def download_image_for_row(row):
        id_value = row['id']
        headers = {
            'cognitoToken': token,
            'Content-Type': 'application/json'
        }

        async with semaphore:
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    async with httpx.AsyncClient() as client:
                        # Make API call to fetch the image links for the given ID
                        response = await client.get(f'{api_endpoint}/{id_value}', headers=headers, timeout=TIMEOUT)

                        if response.status_code == 200:
                            json_data = response.json()

                            # Get image links
                            image_links = json_data.get('mainImage', {}).get('values', [])
                            if image_links:
                                for index, link in enumerate(image_links):
                                    await download_single_image(link, id_value, index, client)
                            else:
                                logger.warning(f"No image links found for ID {id_value}")
                            return  # Exit on success

                        else:
                            logger.error(f"Failed to retrieve data for ID {id_value}. Status code: {response.status_code}")
                            return  # Exit on permanent failure (non-recoverable error)

                except httpx.RequestError as exc:
                    retries += 1
                    logger.error(f"Request error for ID {id_value}: {str(exc)}. Retrying {retries}/{MAX_RETRIES}...")
                    await asyncio.sleep(2 ** retries)  # Exponential backoff on retries

            logger.error(f"Failed to retrieve data for ID {id_value} after {MAX_RETRIES} retries.")

    async def download_single_image(link, id_value, index, client):
        image_url = link.get('uri')
        image_filename = f"{id_value}_image_{index+1}.jpg"
        image_path = os.path.join(output_folder, image_filename)

        try:
            # Download the image
            image_response = await client.get(image_url, timeout=TIMEOUT)
            if image_response.status_code == 200:
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_response.content)
                logger.info(f"Image {index+1} for ID {id_value} downloaded successfully.")
            else:
                logger.error(f"Failed to download image {index+1} for ID {id_value}. Status code: {image_response.status_code}")

        except httpx.RequestError as exc:
            logger.error(f"Error downloading image {index+1} for ID {id_value}: {str(exc)}")

    # Use `await` to process the async function for each row
    tasks = [download_image_for_row(row) for _, row in filtered_df.iterrows()]
    await asyncio.gather(*tasks)

    logger.info(f"Finished downloading images for {len(filtered_df)} IDs.")
