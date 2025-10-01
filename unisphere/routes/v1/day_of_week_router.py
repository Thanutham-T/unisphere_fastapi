from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models import get_session
from unisphere.schemas.day_of_week_schema import (DayOfWeekCreateSchema,
                                                  DayOfWeekSchema,
                                                  DayOfWeekUpdateSchema)
from unisphere.schemas.day_of_week_translation_schema import (
    DayTranslationCreateSchema, DayTranslationSchema,
    DayTranslationUpdateSchema)
from unisphere.services.dayofweek_service import DBDayOfWeekService
from unisphere.services.dayofweek_service.DayOfWeekService import \
    DayOfWeekServiceInterface

router = APIRouter(prefix="/days", tags=["days"])

def get_day_service(session: AsyncSession = Depends(get_session)) -> DayOfWeekServiceInterface:
    return DBDayOfWeekService(session)

# ----------------------
# Day CRUD
# ----------------------
@router.post("/", response_model=DayOfWeekSchema, status_code=status.HTTP_201_CREATED)
async def create_day(data: DayOfWeekCreateSchema, service: DayOfWeekServiceInterface = Depends(get_day_service)):
    return await service.create_day(data)

@router.get("/", response_model=List[DayOfWeekSchema])
async def list_days(service: DayOfWeekServiceInterface = Depends(get_day_service)):
    return await service.list_days()

@router.get("/{day_id}", response_model=DayOfWeekSchema)
async def get_day(day_id: int, service: DayOfWeekServiceInterface = Depends(get_day_service)):
    return await service.get_day(day_id)

@router.put("/{day_id}", response_model=DayOfWeekSchema)
async def update_day(day_id: int, data: DayOfWeekUpdateSchema, service: DayOfWeekServiceInterface = Depends(get_day_service)):
    return await service.update_day(day_id, data)

@router.delete("/{day_id}", response_model=bool)
async def delete_day(day_id: int, service: DayOfWeekServiceInterface = Depends(get_day_service)):
    return await service.delete_day(day_id)

# ----------------------
# Day Translation CRUD
# ----------------------
@router.post("/{day_id}/translations", response_model=DayTranslationSchema, status_code=status.HTTP_201_CREATED)
async def create_translation(day_id: int, data: DayTranslationCreateSchema, service: DayOfWeekServiceInterface = Depends(get_day_service)):
    return await service.create_translation(data)

@router.get("/{day_id}/translations", response_model=List[DayTranslationSchema])
async def list_translations(day_id: int, service: DayOfWeekServiceInterface = Depends(get_day_service)):
    return await service.list_translations(day_id)

@router.get("/{day_id}/translations/{language_code}", response_model=DayTranslationSchema)
async def get_translation(day_id: int, language_code: str, service: DayOfWeekServiceInterface = Depends(get_day_service)):
    return await service.get_translation(day_id, language_code)

@router.put("/{day_id}/translations/{language_code}", response_model=DayTranslationSchema)
async def update_translation(day_id: int, language_code: str, data: DayTranslationUpdateSchema, service: DayOfWeekServiceInterface = Depends(get_day_service)):
    return await service.update_translation(day_id, language_code, data)

@router.delete("/{day_id}/translations/{language_code}", response_model=bool)
async def delete_translation(day_id: int, language_code: str, service: DayOfWeekServiceInterface = Depends(get_day_service)):
    return await service.delete_translation(day_id, language_code)
