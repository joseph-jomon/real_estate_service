from sqlalchemy import Column, Integer, String, Boolean
from app.database.session import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    api_key = Column(String, nullable=True)  # New column for storing the FlowFact API key
    is_active = Column(Boolean, default=True)
