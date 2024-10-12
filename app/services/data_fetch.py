import httpx
from app.core.config import settings

async def fetch_real_estate_data(token: str):
    url = f"{settings.BASE_URL}/search-service/schemas/estates"
    headers = {
        'cognitoToken': token,
        'Content-Type': 'application/json',
    }
    params = {"page": 1, "size": 50, "offset": 0}
    all_entries = []
    
    async with httpx.AsyncClient() as client:
        while True:
            response = await client.post(url, headers=headers, json={}, params=params)
            result = response.json()
            entries = result.get("entries", [])
            if not entries:
                break
            all_entries.extend(entries)
            params["page"] += 1
            params["offset"] += params["size"]
    
    return all_entries
