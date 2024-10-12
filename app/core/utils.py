import httpx
import os
import pandas as pd

async def check_image_url(url: str) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            return response.status_code == 200
        except httpx.RequestError:
            return False

def save_to_dataframe(data):
    df = pd.DataFrame(data)
    df.to_csv('./data/final_dataset.csv', index=False)
    return df
