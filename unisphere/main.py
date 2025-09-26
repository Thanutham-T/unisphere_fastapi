from contextlib import asynccontextmanager

from fastapi import FastAPI

import unisphere.models as models
import unisphere.routes as routers
from unisphere.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    await models.init_db()
    yield
    # Shutdown
    await models.close_db()
    await models.close_redis()

app = FastAPI(lifespan=lifespan)
app.include_router(routers.router)

settings = get_settings()


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to Unisphere API", "version": settings.APP_VERSION}


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint for production monitoring."""
    return {"status": "healthy", "app": settings.APP_NAME}
