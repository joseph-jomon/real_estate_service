import httpx
from app.core.utils import check_image_url
from app.core.config import settings

async def validate_image_links():
    invalid_ids = []
    all_ids = []  # Load the IDs from previous data fetch
    async with httpx.AsyncClient() as client:
        for id in all_ids:
            url = f"{settings.BASE_URL}/entity-service/entities/{id}"
            headers = {'cognitoToken': settings.API_KEY}
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
    return invalid_ids
