import os
import pandas as pd
import httpx
from app.core.utils import check_image_url
from app.core.config import settings

async def validate_image_links(token: str, company_name: str):
    invalid_ids = []

    # Step 1: Define the company-specific CSV path and extract the 'id' column
    csv_path = os.path.join(settings.DATA_OUTPUT_FOLDER, company_name, "final_dataset.csv")
    df = pd.read_csv(csv_path)
    all_ids = df['id'].tolist()  # Load IDs from CSV, assuming it has a column named 'id'

    # Step 2: Validate image links for each ID
    async with httpx.AsyncClient() as client:
        for id in all_ids:
            url = f"{settings.BASE_URL}/entity-service/entities/{id}"
            headers = {
                'cognitoToken': token,
                'Content-Type': 'application/json',
            }
            response = await client.get(url, headers=headers)
            json_data = response.json()
            image_links = json_data.get('mainImage', {}).get('values', [])

            if not image_links:
                invalid_ids.append(id)
            else:
                for image in image_links:
                    if not await check_image_url(image.get('uri')):
                        invalid_ids.append(id)
                        break
    
    # Step 3: Write invalid IDs to a company-specific CSV file in the same directory
    invalid_ids_path = os.path.join(settings.DATA_OUTPUT_FOLDER, company_name, "invalid_ids.csv")
    invalid_ids_df = pd.DataFrame(invalid_ids, columns=["id"])
    
    try:
        invalid_ids_df.to_csv(invalid_ids_path, index=False)
        print(f"Invalid IDs saved to {invalid_ids_path}")
    except Exception as e:
        print(f"Failed to save invalid IDs to {invalid_ids_path}: {e}")
    
    return invalid_ids
