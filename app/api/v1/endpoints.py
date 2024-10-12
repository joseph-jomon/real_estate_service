from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.authentication import authenticate_api_key
from app.services.data_fetch import fetch_real_estate_data
from app.services.image_service import validate_image_links
from app.core.utils import save_to_dataframe
from app.services.batch_processing import send_text_batch, send_image_batch, get_task_status

# Initialize the templates engine
templates = Jinja2Templates(directory="app/frontend/templates")

router = APIRouter()

# Route to serve the API Key form (base.html)
@router.get("/api-key-page", response_class=HTMLResponse)
async def get_api_key_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# Route to serve the Dashboard (dashboard.html)
@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    # Placeholder for future data processing logic to send to the dashboard
    plotly_data = []  # Replace with actual plotly data
    return templates.TemplateResponse("dashboard.html", {"request": request, "plotly_data": plotly_data})

# FlowFact API key authentication
@router.post("/authenticate/")
async def authenticate(api_key: str):
    token = await authenticate_api_key(api_key)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid API key")
    return {"message": "Authentication successful", "token": token}

# Fetch real estate data from FlowFact API
@router.get("/fetch-data/")
async def fetch_data(token: str = Depends(authenticate_api_key)):
    real_estate_data = await fetch_real_estate_data(token)
    return {"data": real_estate_data}

# Validate image links for real estate objects
@router.post("/validate-images/")
async def validate_images():
    invalid_ids = await validate_image_links()
    return {"invalid_ids": invalid_ids}

# Process text and image batches
@router.post("/process-text-batch/")
async def process_text_batch(text_batch: list):
    task_id = await send_text_batch(text_batch)
    return {"task_id": task_id}

@router.post("/process-image-batch/")
async def process_image_batch(image_batch: list):
    task_id = await send_image_batch(image_batch)
    return {"task_id": task_id}

# Check task status
@router.get("/task-status/{task_id}")
async def task_status(task_id: str):
    status = await get_task_status(task_id)
    return {"status": status}
