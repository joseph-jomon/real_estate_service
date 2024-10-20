import httpx
import os
from app.core.config import settings
from app.core.utils import save_to_dataframe

async def fetch_real_estate_data(token: str):
    url = f"{settings.BASE_URL}/search-service/schemas/estates"
    headers = {
        'cognitoToken': token,
        'Content-Type': 'application/json',
    }
    body = {
        "target": "ENTITY",
        "fetch": [],
        "conditions": [
            {
                "type": "AND",
                "conditions": [
                    {
                        "type": "HASFIELD",
                        "field": "status",
                    }
                ]
            }
        ],
        "sorts": [
            {
                "field": "_metadata.createdTimestamp",
                "direction": "ASC"
            }
        ]
    }

    # Set pagination parameters
    params = {"page": 1, "size": 50, "offset": 0}
    all_entries = []

    async with httpx.AsyncClient() as client:
        while True:
            response = await client.post(url, headers=headers, json=body, params=params)
            result = response.json()
            entries = result.get("entries", [])
            if not entries:
                break
            all_entries.extend(entries)
            params["page"] += 1
            params["offset"] += params["size"]

    # Save the fetched data to a CSV file using the config path
    save_to_dataframe(all_entries, settings.DATA_OUTPUT_PATH)

    # Return a success message and the count of fetched entries
    return {"status": "success", "fetched_entries": len(all_entries)}
