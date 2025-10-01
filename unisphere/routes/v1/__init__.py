from fastapi import APIRouter

from . import (
    announcement_router,
    auth_router,
    branch_router,
    course_router,
    day_of_week_router,
    event_router,
    faculty_router,
    greeting_router,
    schedule_router,
    section_router,
    semester_router,
    upload_router,
    user_place_router,
)

router = APIRouter(prefix="/v1")


# add routers to v1
router.include_router(greeting_router.router)
router.include_router(auth_router.router)
router.include_router(event_router.router)
router.include_router(upload_router.router)
router.include_router(announcement_router.router)
router.include_router(user_place_router.router)
router.include_router(course_router.router)
router.include_router(semester_router.router)
router.include_router(branch_router.router)
router.include_router(faculty_router.router)
router.include_router(day_of_week_router.router)
router.include_router(section_router.router)
router.include_router(schedule_router.router)
