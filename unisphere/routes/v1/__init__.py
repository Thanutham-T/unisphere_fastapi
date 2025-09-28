from fastapi import APIRouter

from . import auth_router, greeting_router

router = APIRouter(prefix="/v1")


# add test router to v1
router.include_router(greeting_router.router)
router.include_router(auth_router.router)
