from fastapi import FastAPI
from fastapi.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from app.api.v1.endpoints import router as flowfact_router
from app.api.v1.user_endpoints import router as user_router
from app.database.session import engine

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

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# Include routers for your FlowFact and user-related endpoints
app.include_router(flowfact_router, prefix="/flowfact")
app.include_router(user_router, prefix="/users")
