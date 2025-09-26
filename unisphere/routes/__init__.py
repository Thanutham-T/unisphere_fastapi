from fastapi import APIRouter

from . import health, v1

router = APIRouter()
router.include_router(v1.router)
router.include_router(health.router)
