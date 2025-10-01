from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models import get_session
from unisphere.schemas.section_instructor_schema import (
    SectionInstructorCreateSchema, SectionInstructorSchema)
from unisphere.schemas.section_rrule_schema import (SectionRRuleCreateSchema,
                                                    SectionRRuleSchema,
                                                    SectionRRuleUpdateSchema)
from unisphere.schemas.section_schema import (SectionCreateSchema,
                                              SectionSchema,
                                              SectionUpdateSchema)
from unisphere.services.section_service.DBSectionService import \
    DBSectionService
from unisphere.services.section_service.SectionServiceInterface import \
    SectionServiceInterface

router = APIRouter(prefix="/sections", tags=["sections"])

def get_section_service(session: AsyncSession = Depends(get_session)) -> SectionServiceInterface:
    return DBSectionService(session)

# ----------------------
# Section CRUD
# ----------------------
@router.post("/", response_model=SectionSchema, status_code=status.HTTP_201_CREATED)
async def create_section(data: SectionCreateSchema, service: SectionServiceInterface = Depends(get_section_service)):
    return await service.create_section(data)

@router.get("/", response_model=List[SectionSchema])
async def list_sections(course_id: Optional[int] = Query(None), service: SectionServiceInterface = Depends(get_section_service)):
    return await service.list_sections(course_id)

@router.get("/{section_id}", response_model=SectionSchema)
async def get_section(section_id: int, service: SectionServiceInterface = Depends(get_section_service)):
    return await service.get_section(section_id)

@router.put("/{section_id}", response_model=SectionSchema)
async def update_section(section_id: int, data: SectionUpdateSchema, service: SectionServiceInterface = Depends(get_section_service)):
    return await service.update_section(section_id, data)

@router.delete("/{section_id}", response_model=bool)
async def delete_section(section_id: int, service: SectionServiceInterface = Depends(get_section_service)):
    return await service.delete_section(section_id)

# ----------------------
# Section Instructor CRUD
# ----------------------
@router.post("/{section_id}/instructors", response_model=SectionInstructorSchema, status_code=status.HTTP_201_CREATED)
async def assign_instructor(section_id: int, data: SectionInstructorCreateSchema, service: SectionServiceInterface = Depends(get_section_service)):
    return await service.assign_instructor(data)

@router.get("/{section_id}/instructors", response_model=List[SectionInstructorSchema])
async def list_instructors(section_id: int, service: SectionServiceInterface = Depends(get_section_service)):
    return await service.list_instructors(section_id)

@router.delete("/instructors/{enroll_id}", response_model=bool)
async def remove_instructor(enroll_id: int, service: SectionServiceInterface = Depends(get_section_service)):
    return await service.remove_instructor(enroll_id)

# ----------------------
# Section RRule CRUD
# ----------------------
@router.post("/{section_id}/rrules", response_model=SectionRRuleSchema, status_code=status.HTTP_201_CREATED)
async def create_rrule(section_id: int, data: SectionRRuleCreateSchema, service: SectionServiceInterface = Depends(get_section_service)):
    return await service.create_rrule(data)

@router.get("/{section_id}/rrules", response_model=List[SectionRRuleSchema])
async def list_rrules(section_id: int, service: SectionServiceInterface = Depends(get_section_service)):
    return await service.list_rrules(section_id)

@router.get("/rrules/{rrule_id}", response_model=SectionRRuleSchema)
async def get_rrule(rrule_id: int, service: SectionServiceInterface = Depends(get_section_service)):
    return await service.get_rrule(rrule_id)

@router.put("/rrules/{rrule_id}", response_model=SectionRRuleSchema)
async def update_rrule(rrule_id: int, data: SectionRRuleUpdateSchema, service: SectionServiceInterface = Depends(get_section_service)):
    return await service.update_rrule(rrule_id, data)

@router.delete("/rrules/{rrule_id}", response_model=bool)
async def delete_rrule(rrule_id: int, service: SectionServiceInterface = Depends(get_section_service)):
    return await service.delete_rrule(rrule_id)