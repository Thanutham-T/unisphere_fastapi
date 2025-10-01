from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models import get_session
from unisphere.schemas.semester_schema import (SemesterCreateSchema,
                                               SemesterSchema,
                                               SemesterUpdateSchema)
from unisphere.services.semester_service.DBSemesterService import \
    DBSemesterService
from unisphere.services.semester_service.SemesterServiceInterface import \
    SemesterServiceInterface


# Dependency injection
def get_semester_service(session: AsyncSession = Depends(get_session)) -> SemesterServiceInterface:
    # settings = get_settings()
    # if settings.USE_MOCK:
    #     return MockCourseService()
    return DBSemesterService(session=session)

router = APIRouter(prefix="/semesters", tags=["semesters"])


@router.get("/", response_model=List[SemesterSchema])
async def list_semesters(
    include_archived: bool = Query(False, description="Include archived semesters"),
    service: SemesterServiceInterface = Depends(get_semester_service),
):
    """Get all semesters (optionally include archived)."""
    return await service.get_all_semesters(include_archived)


@router.get("/{semester_id}", response_model=SemesterSchema)
async def get_semester(
    semester_id: int,
    service: SemesterServiceInterface = Depends(get_semester_service),
):
    """Get a semester by ID."""
    semester = await service.get_semester_by_id(semester_id)
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    return semester


@router.post("/", response_model=SemesterSchema)
async def create_semester(
    semester_create: SemesterCreateSchema,
    service: SemesterServiceInterface = Depends(get_semester_service),
):
    """Create a new semester."""
    return await service.create_semester(semester_create)


@router.put("/{semester_id}", response_model=SemesterSchema)
async def update_semester(
    semester_id: int,
    semester_update: SemesterUpdateSchema,
    service: SemesterServiceInterface = Depends(get_semester_service),
):
    """Update an existing semester."""
    updated = await service.update_semester(semester_id, semester_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Semester not found")
    return updated


@router.delete("/{semester_id}", response_model=bool)
async def delete_semester(
    semester_id: int,
    service: SemesterServiceInterface = Depends(get_semester_service),
):
    """Delete a semester."""
    deleted = await service.delete_semester(semester_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Semester not found")
    return deleted


@router.post("/{semester_id}/archive", response_model=SemesterSchema)
async def archive_semester(
    semester_id: int,
    archived_at: Optional[datetime] = Query(None, description="Datetime to set as archived"),
    service: SemesterServiceInterface = Depends(get_semester_service),
):
    """Archive a semester."""
    archived = await service.archive_semester(semester_id, archived_at)
    if not archived:
        raise HTTPException(status_code=404, detail="Semester not found")
    return archived
