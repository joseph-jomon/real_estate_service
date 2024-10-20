from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from app.api.v1.endpoints import router as flowfact_router
from app.api.v1.user_endpoints import router as user_router
from app.database.session import engine
from app.database.session import Base
from pathlib import Path
import os
from fastapi.middleware.cors import CORSMiddleware

# Lifespan context manager for the FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code for starting the application (e.g., connecting to DB)
    async with engine.begin() as conn:
        # Optionally, ensure all tables are created (remove if not needed)
        await conn.run_sync(Base.metadata.create_all)
        app.state.db = conn  # Optionally store the connection in the app state

    yield  # This runs the app

    # Code for cleanup (e.g., closing DB connection)
    await conn.close()

# Initialize FastAPI with the lifespan event
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the base directory dynamically using pathlib
BASE_DIR = Path(__file__).resolve().parent # Adjust depending on your structure
print(f"Serving static files from: {BASE_DIR / 'frontend' / 'static'}")


# Serve the static folder
app.mount("/static", StaticFiles(directory=BASE_DIR / "frontend" / "static"), name="static")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# Include routers for your FlowFact and user-related endpoints
app.include_router(flowfact_router, prefix="/flowfact")
app.include_router(user_router, prefix="/users")
