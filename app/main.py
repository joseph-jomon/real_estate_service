from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from app.api.v1.endpoints import router as flowfact_router
from pathlib import Path
import os
from fastapi.middleware.cors import CORSMiddleware



# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the base directory dynamically using pathlib
BASE_DIR = Path(__file__).resolve().parent # Adjust depending on your structure

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# Include routers for your FlowFact and user-related endpoints
app.include_router(flowfact_router, prefix="/flowfact")
