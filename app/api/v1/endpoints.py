from fastapi import APIRouter, Depends, HTTPException, Request
from app.services.authentication import authenticate_api_key
from app.services.data_fetch import fetch_real_estate_data
from app.services.image_service import validate_image_links
from app.services.dataset_preparation import prepare_and_save_dataset
from app.services.batch_processing import start_batch_processing
from pydantic import BaseModel



router = APIRouter()

class APIKey(BaseModel):
    api_key: str

@router.post("/authenticate/")
async def authenticate(api_key: APIKey, request: Request):
    # Pass both the api_key and request to the function
    token = await authenticate_api_key(api_key.api_key, request)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid API key")
    return {"message": "Authentication successful", "token": token}

# Fetch real estate data from FlowFact API
@router.get("/fetch-data/")
async def fetch_data(request: Request, token: str = Depends(authenticate_api_key)):
    try:
        # Retrieve the company_name from the session
        company_name = request.session.get('company_name')
        if not company_name:
            raise HTTPException(status_code=400, detail="Company name not found in session")

        # Call the service to fetch the data and store it locally
        result = await fetch_real_estate_data(token, company_name)

        # Return a simple success message to the frontend
        return {"message": "Data fetched successfully", "entries_fetched": result["fetched_entries"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

# Validate image links for real estate objects
@router.post("/validate-images/")
async def validate_images(request: Request, token: str = Depends(authenticate_api_key)):
    try:
        # Retrieve company name from session
        company_name = request.session.get('company_name')
        if not company_name:
            raise HTTPException(status_code=400, detail="Company name not found in session")

        invalid_ids = await validate_image_links(token, company_name)
        return {"invalid_ids": invalid_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during image validation: {str(e)}")

# Prepare the dataset by filtering and processing text and image data
@router.post("/prepare-dataset/")
async def prepare_dataset(request: Request, token: str = Depends(authenticate_api_key)):
    try:
        # Retrieve company name from session
        company_name = request.session.get('company_name')
        if not company_name:
            raise HTTPException(status_code=400, detail="Company name not found in session")

        await prepare_and_save_dataset(token, company_name)
        return {"message": "Dataset prepared successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dataset preparation failed: {e}")

# Start batch processing for text and image data
@router.post("/start-batch-processing/")
async def start_batch_processing_endpoint(request: Request, token: str = Depends(authenticate_api_key)):
    try:
        # Retrieve company name from session
        company_name = request.session.get('company_name')
        if not company_name:
            raise HTTPException(status_code=400, detail="Company name not found in session")

        await start_batch_processing(company_name)
        return {"message": "Batch processing started."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {e}")
