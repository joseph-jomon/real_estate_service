import httpx
from fastapi import Request, HTTPException

async def authenticate_api_key(api_key: str, request: Request):
    url = "https://api.production.cloudios.flowfact-prod.cloud/admin-token-service/public/adminUser/authenticate"
    headers = {'token': api_key}
    
    async with httpx.AsyncClient() as client:
        api_response = await client.get(url, headers=headers)
    
    if api_response.status_code == 200:
        token = api_response.text
        request.session['token'] = token  # Store token in session
        return token
    else:
        raise HTTPException(status_code=400, detail="Invalid API key")
