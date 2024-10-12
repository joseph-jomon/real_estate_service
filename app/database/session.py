from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Asynchronous PostgreSQL connection URL format: postgresql+asyncpg://user:password@host:port/database
DATABASE_URL = "postgresql+asyncpg://your_db_user:your_db_password@localhost/your_db_name"

# Create the asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory bound to the async engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Base class for declarative models
Base = declarative_base()

# Dependency to get the DB session
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
