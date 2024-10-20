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

def save_to_dataframe(data, output_path):
    # Resolve directory and ensure it exists
    directory = os.path.dirname(output_path)

    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
        
        # Create DataFrame from data
        df = pd.DataFrame(data)

        # Write DataFrame to CSV
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
        
    except Exception as e:
        # Catch any exception and print it
        print(f"Failed to save data to {output_path}: {e}")