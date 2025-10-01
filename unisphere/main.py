from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import unisphere.models as models
import unisphere.routes as routers
from unisphere.core.config import get_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Application lifespan manager."""
    # Startup
    await models.init_db()
    yield
    # Shutdown
    await models.close_db()
    await models.close_redis()

app = FastAPI(lifespan=lifespan)

# Mount static files for uploaded images
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include API routes
app.include_router(routers.router)

settings = get_settings()


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to Unisphere API", "version": settings.APP_VERSION}


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint for production monitoring."""
    return {"status": "healthy", "app": settings.APP_NAME}
