import httpx
import os
import pandas as pd
import base64
import asyncio  # Adding asyncio for orchestrating the batch processes
from app.core.config import settings

BATCH_SIZE = 5  # You can adjust the batch size according to the service limits

async def send_text_batch(text_batch):
    url = settings.BATCH_VECTOR_TEXT_API
    payload = {
        "texts": [{"id": text_data["id"], "immo_text": text_data["Combined_Text"]} for text_data in text_batch]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get('task_id')
        raise Exception(f"Error sending text batch: {response.status_code}")

async def send_image_batch(image_batch):
    url = settings.BATCH_VECTOR_IMAGE_API
    payload = {
        "images": [{"id": image_data["id"], "image": image_data["base64_image"]} for image_data in image_batch]
    }
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get('task_id')
        raise Exception(f"Error sending image batch: {response.status_code}")

async def process_text_data_in_batches():
    # Read the filtered dataset
    dataset_path = os.path.join(settings.DATA_OUTPUT_FOLDER, "filtered_final_dataset.csv")
    df = pd.read_csv(dataset_path)

    # Split into batches and send
    for start_idx in range(0, len(df), BATCH_SIZE):
        text_batch = df.iloc[start_idx:start_idx+BATCH_SIZE].to_dict(orient='records')
        task_id = await send_text_batch(text_batch)
        print(f"Text batch starting from index {start_idx} sent with task ID: {task_id}")

async def process_image_data_in_batches():
    # Read the filtered dataset
    dataset_path = os.path.join(settings.DATA_OUTPUT_FOLDER, "filtered_final_dataset.csv")
    df = pd.read_csv(dataset_path)

    # Split into batches and process
    for start_idx in range(0, len(df), BATCH_SIZE):
        image_batch = []
        batch_df = df.iloc[start_idx:start_idx + BATCH_SIZE]

        for _, row in batch_df.iterrows():
            image_path = row['Image']
            try:
                with open(image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                image_batch.append({
                    "id": row['id'],
                    "base64_image": base64_image
                })
            except FileNotFoundError:
                print(f"Image for ID {row['id']} not found at path: {image_path}")

        # Send the batch if there are images to process
        if image_batch:
            task_id = await send_image_batch(image_batch)
            print(f"Image batch starting from index {start_idx} sent with task ID: {task_id}")

    print("All image batches have been processed.")

# Orchestrator function to start both text and image batch processing
async def start_batch_processing():
    print("Starting text batch processing...")
    await process_text_data_in_batches()

    print("Starting image batch processing...")
    await process_image_data_in_batches()

# Call the main processing function from another service or API when needed.
# Example: `asyncio.run(start_batch_processing(token))`
