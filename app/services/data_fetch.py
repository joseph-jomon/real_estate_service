import httpx
import os
from app.core.config import settings
from app.core.utils import save_to_dataframe

async def fetch_real_estate_data(token: str, company_name: str):
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
    # Data output path based on company name
    company_folder = os.path.join(settings.DATA_OUTPUT_FOLDER, company_name)
    os.makedirs(company_folder, exist_ok=True)
    output_path = os.path.join(company_folder, "final_dataset.csv")



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
    save_to_dataframe(all_entries, output_path)

    # Return a success message and the count of fetched entries
    return {"status": "success", "fetched_entries": len(all_entries)}
