from fastapi import APIRouter

from . import greeting_router

router = APIRouter(prefix="/v1")


# add test router to v1
router.include_router(greeting_router.router)
