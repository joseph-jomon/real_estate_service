import httpx
from fastapi import Request, HTTPException
from app.core.config import settings

def sanitize_company_name(company_name: str) -> str:
    return company_name.strip().replace(" ", "_").lower()

async def authenticate_api_key(api_key: str, request: Request):
    url = "https://api.production.cloudios.flowfact-prod.cloud/admin-token-service/public/adminUser/authenticate"
    headers = {'token': api_key}
    
    async with httpx.AsyncClient() as client:
        api_response = await client.get(url, headers=headers)
    
    if api_response.status_code == 200:
        token = api_response.text
        request.session['token'] = token  # Store token in session

        # Fetch and sanitize company details
        company_info = await fetch_company_info(token)
        sanitized_company_name = sanitize_company_name(company_info['companyName'])
        request.session['company_name'] = sanitized_company_name
        request.session['company_id'] = company_info['id']
        
        return token
    else:
        raise HTTPException(status_code=400, detail="Invalid API key")


async def fetch_company_info(token: str):
    url = f"{settings.BASE_URL}/company-service/company"
    headers = {'cognitoToken': token}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=500, detail="Failed to fetch company info")
