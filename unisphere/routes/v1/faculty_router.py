from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models import get_session
from unisphere.schemas.faculty_schema import (FacultyCreateSchema,
                                              FacultySchema,
                                              FacultyUpdateSchema)
from unisphere.schemas.faculty_translation_schema import (
    FacultyTranslationCreateSchema, FacultyTranslationSchema,
    FacultyTranslationUpdateSchema)
from unisphere.services.faculty_service.DBFacultyService import \
    DBFacultyService

router = APIRouter(prefix="/faculties", tags=["faculties"])

# Dependency
async def get_faculty_service(session: AsyncSession = Depends(get_session)) -> DBFacultyService:
    return DBFacultyService(session)


# Faculty Endpoints
@router.post("/", response_model=FacultySchema, status_code=status.HTTP_201_CREATED)
async def create_faculty(data: FacultyCreateSchema, service: DBFacultyService = Depends(get_faculty_service)):
    return await service.create_faculty(data)

@router.get("/{faculty_id}", response_model=FacultySchema)
async def get_faculty(faculty_id: int, service: DBFacultyService = Depends(get_faculty_service)):
    return await service.get_faculty(faculty_id)

@router.put("/{faculty_id}", response_model=FacultySchema)
async def update_faculty(faculty_id: int, data: FacultyUpdateSchema, service: DBFacultyService = Depends(get_faculty_service)):
    return await service.update_faculty(faculty_id, data)

@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faculty(faculty_id: int, service: DBFacultyService = Depends(get_faculty_service)):
    await service.delete_faculty(faculty_id)
    return None

@router.get("/", response_model=List[FacultySchema])
async def list_faculties(status: Optional[str] = None, service: DBFacultyService = Depends(get_faculty_service)):
    return await service.list_faculties(status=status)


# Faculty Translation Endpoints
@router.post("/{faculty_id}/translations", response_model=FacultyTranslationSchema, status_code=status.HTTP_201_CREATED)
async def create_translation(faculty_id: int, data: FacultyTranslationCreateSchema, service: DBFacultyService = Depends(get_faculty_service)):
    return await service.create_translation(data)

@router.get("/{faculty_id}/translations/{language_code}", response_model=FacultyTranslationSchema)
async def get_translation(faculty_id: int, language_code: str, service: DBFacultyService = Depends(get_faculty_service)):
    return await service.get_translation(faculty_id, language_code)

@router.put("/{faculty_id}/translations/{language_code}", response_model=FacultyTranslationSchema)
async def update_translation(faculty_id: int, language_code: str, data: FacultyTranslationUpdateSchema, service: DBFacultyService = Depends(get_faculty_service)):
    return await service.update_translation(faculty_id, language_code, data)

@router.delete("/{faculty_id}/translations/{language_code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_translation(faculty_id: int, language_code: str, service: DBFacultyService = Depends(get_faculty_service)):
    await service.delete_translation(faculty_id, language_code)
    return None

@router.get("/{faculty_id}/translations", response_model=List[FacultyTranslationSchema])
async def list_translations(faculty_id: int, service: DBFacultyService = Depends(get_faculty_service)):
    return await service.list_translations(faculty_id)
