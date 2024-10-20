from fastapi import APIRouter, Depends, HTTPException, Request
from app.database.session import get_db
from app.services.user_service import create_user, authenticate_user
from sqlalchemy.ext.asyncio import AsyncSession  # Import AsyncSession

router = APIRouter()

@router.post("/register/")
async def register_user(username: str, email: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await create_user(db, username, email, password)
    return {"message": "User registered successfully", "user": user}

@router.post("/login/")
async def login_user(username: str, password: str, request: Request, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Store user information in the session
    request.session["user_id"] = user.id
    return {"message": "Login successful"}

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()  # Clear the session
    return {"message": "Logged out successfully"}
