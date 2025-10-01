import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

import unisphere.models as models
import unisphere.routes as routers
from unisphere.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup: skip DB init when running tests to let fixtures control DB
    if os.getenv("ENVIRONMENT") != "test" and not os.getenv("TEST_DATABASE_URL") and not os.getenv("PYTEST_CURRENT_TEST"):
        await models.init_db()
    yield
    # Shutdown
    if os.getenv("ENVIRONMENT") != "test" and not os.getenv("TEST_DATABASE_URL") and not os.getenv("PYTEST_CURRENT_TEST"):
        await models.close_db()
        await models.close_redis()

app = FastAPI(lifespan=lifespan)
app.include_router(routers.router)

settings = get_settings()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to Unisphere API", "version": settings.APP_VERSION}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for production monitoring."""
    return {"status": "healthy", "app": settings.APP_NAME}
