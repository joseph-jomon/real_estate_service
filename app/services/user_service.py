from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash passwords
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Asynchronous function to create a new user
async def create_user(db: AsyncSession, username: str, email: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    
    # Check if the username or email already exists
    result = await db.execute(select(User).filter((User.username == username) | (User.email == email)))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    user = User(username=username, email=email, hashed_password=hashed_password)
    
    db.add(user)
    await db.commit()  # Asynchronous commit
    await db.refresh(user)  # Asynchronous refresh to get the updated user object
    return user

# Asynchronous function to authenticate a user
async def authenticate_user(db: AsyncSession, username: str, password: str) -> User:
    # Use asynchronous query with select statement
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalar_one_or_none()  # Retrieve one or None
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return user

# Asynchronous function to update the user's FlowFact API key
async def update_user_api_key(db: AsyncSession, user_id: int, api_key: str) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.api_key = api_key
    await db.commit()
    await db.refresh(user)
    return user

# Asynchronous function to retrieve the user's FlowFact API key
async def get_user_api_key(db: AsyncSession, user_id: int) -> str:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.api_key:
        raise HTTPException(status_code=404, detail="API key not found for this user")
    
    return user.api_key
