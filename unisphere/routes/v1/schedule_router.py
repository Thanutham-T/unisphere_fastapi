from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models import get_session
from unisphere.schemas.schedule_schema import (SectionScheduleCreateSchema,
                                               SectionScheduleSchema,
                                               SectionScheduleUpdateSchema)
from unisphere.services.schedule_service.DBScheduleService import \
    DBScheduleService
from unisphere.services.schedule_service.ScheduleServiceInterface import \
    ScheduleServiceInterface

router = APIRouter(prefix="/schedules", tags=["schedules"])

def get_schedule_service(session: AsyncSession = Depends(get_session)) -> ScheduleServiceInterface:
    return DBScheduleService(session)

# ----------------------
# CRUD Endpoints
# ----------------------
@router.post("/", response_model=SectionScheduleSchema, status_code=status.HTTP_201_CREATED)
async def create_schedule(data: SectionScheduleCreateSchema, service: ScheduleServiceInterface = Depends(get_schedule_service)):
    return await service.create_schedule(data)

@router.get("/{section_id}", response_model=List[SectionScheduleSchema])
async def list_schedules(section_id: int, service: ScheduleServiceInterface = Depends(get_schedule_service)):
    return await service.list_schedules(section_id)

@router.put("/{schedule_id}", response_model=SectionScheduleSchema)
async def update_schedule(schedule_id: int, data: SectionScheduleUpdateSchema, service: ScheduleServiceInterface = Depends(get_schedule_service)):
    return await service.update_schedule(schedule_id, data)

@router.delete("/{schedule_id}", response_model=bool)
async def delete_schedule(schedule_id: int, service: ScheduleServiceInterface = Depends(get_schedule_service)):
    return await service.delete_schedule(schedule_id)
