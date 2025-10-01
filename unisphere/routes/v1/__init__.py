from fastapi import APIRouter

from . import (
    announcement_router,
    auth_router,
    event_router,
    greeting_router,
    upload_router,
)

router = APIRouter(prefix="/v1")


# add routers to v1
router.include_router(greeting_router.router)
router.include_router(auth_router.router)
router.include_router(event_router.router)
router.include_router(upload_router.router)
router.include_router(announcement_router.router)
