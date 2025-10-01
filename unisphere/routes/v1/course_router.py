from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models import get_session
from unisphere.schemas.course_schema import (CourseCreateSchema, CourseSchema,
                                             CourseUpdateSchema)
from unisphere.schemas.course_translation_schema import (
    CourseTranslationCreateSchema, CourseTranslationSchema,
    CourseTranslationUpdateSchema)
from unisphere.schemas.user_enroll_schema import UserEnrollSchema
from unisphere.services.course_service.CourseServiceInterface import \
    CourseServiceInterface
from unisphere.services.course_service.DBCourseService import DBCourseService

router = APIRouter(prefix="/courses", tags=["courses"])

# ----------------------
# Dependencies
# ----------------------
def get_course_service(session: AsyncSession = Depends(get_session)) -> CourseServiceInterface:
    return DBCourseService(session=session)

# ----------------------
# Course Endpoints
# ----------------------
@router.get("/", response_model=List[CourseSchema])
async def list_courses(
    semester_id: int = Query(..., description="Semester ID"),
    service: CourseServiceInterface = Depends(get_course_service),
):
    return await service.get_courses_by_semester(semester_id)


@router.get("/user/{user_id}", response_model=List[CourseSchema])
async def get_user_courses(
    user_id: int,
    semester_id: Optional[int] = Query(None, description="Filter by semester"),
    service: CourseServiceInterface = Depends(get_course_service),
):
    return await service.get_user_courses(user_id, semester_id)


@router.post("/{course_id}/enroll", response_model=UserEnrollSchema)
async def enroll_user(
    course_id: int,
    user_id: int = Query(..., description="User ID to enroll"),
    service: CourseServiceInterface = Depends(get_course_service),
):
    return await service.enroll_user_to_course(user_id, course_id)


@router.delete("/{course_id}/withdraw", response_model=bool)
async def withdraw_user(
    course_id: int,
    user_id: int = Query(..., description="User ID to withdraw"),
    service: CourseServiceInterface = Depends(get_course_service),
):
    success = await service.withdraw_user_from_course(user_id, course_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    return success


@router.post("/", response_model=CourseSchema, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreateSchema,
    service: CourseServiceInterface = Depends(get_course_service),
):
    return await service.create_course(course_data)


@router.put("/{course_id}", response_model=CourseSchema)
async def update_course(
    course_id: int,
    course_data: CourseUpdateSchema,
    service: CourseServiceInterface = Depends(get_course_service),
):
    try:
        return await service.update_course(course_id, course_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{course_id}", response_model=bool)
async def delete_course(
    course_id: int,
    service: CourseServiceInterface = Depends(get_course_service),
):
    success = await service.delete_course(course_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return success

# ----------------------
# Course Translation Endpoints
# ----------------------
@router.post("/{course_id}/translations", response_model=CourseTranslationSchema, status_code=status.HTTP_201_CREATED)
async def create_translation(
    course_id: int,
    data: CourseTranslationCreateSchema,
    service: CourseServiceInterface = Depends(get_course_service),
):
    return await service.create_translation(data)


@router.get("/{course_id}/translations", response_model=List[CourseTranslationSchema])
async def list_translations(
    course_id: int,
    service: CourseServiceInterface = Depends(get_course_service),
):
    return await service.list_translations(course_id)


@router.get("/{course_id}/translations/{language_code}", response_model=CourseTranslationSchema)
async def get_translation(
    course_id: int,
    language_code: str,
    service: CourseServiceInterface = Depends(get_course_service),
):
    return await service.get_translation(course_id, language_code)


@router.put("/{course_id}/translations/{language_code}", response_model=CourseTranslationSchema)
async def update_translation(
    course_id: int,
    language_code: str,
    data: CourseTranslationUpdateSchema,
    service: CourseServiceInterface = Depends(get_course_service),
):
    return await service.update_translation(course_id, language_code, data)


@router.delete("/{course_id}/translations/{language_code}", response_model=bool)
async def delete_translation(
    course_id: int,
    language_code: str,
    service: CourseServiceInterface = Depends(get_course_service),
):
    success = await service.delete_translation(course_id, language_code)
    return success
