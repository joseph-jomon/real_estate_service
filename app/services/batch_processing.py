import httpx
from app.core.config import settings

async def send_text_batch(text_batch):
    url = f"{settings.BATCH_VECTOR_API}/process-text-batch/"
    payload = {
        "texts": [{"id": text_data["id"], "immo_text": text_data["text"]} for text_data in text_batch]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get('task_id')
        raise Exception(f"Error sending text batch: {response.status_code}")

async def send_image_batch(image_batch):
    url = f"{settings.BATCH_VECTOR_API}/process-image-batch/"
    payload = {
        "images": [{"id": image_data["id"], "image": image_data["image"]} for image_data in image_batch]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get('task_id')
        raise Exception(f"Error sending image batch: {response.status_code}")

async def get_task_status(task_id):
    url = f"{settings.BATCH_VECTOR_API}/task-status/{task_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json().get("status")
        raise Exception(f"Error fetching task status: {response.status_code}")


