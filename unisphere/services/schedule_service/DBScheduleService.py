from typing import List

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models.schedule_model import SectionScheduleModel
from unisphere.schemas.schedule_schema import (SectionScheduleCreateSchema,
                                               SectionScheduleSchema,
                                               SectionScheduleUpdateSchema)

from .ScheduleServiceInterface import ScheduleServiceInterface


class DBScheduleService(ScheduleServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_schedule(self, data: SectionScheduleCreateSchema) -> SectionScheduleSchema:
        schedule = SectionScheduleModel(**data.model_dump())
        self.session.add(schedule)
        await self.session.commit()
        await self.session.refresh(schedule)
        return SectionScheduleSchema.model_validate(schedule)

    async def list_schedules(self, section_id: int) -> List[SectionScheduleSchema]:
        query = select(SectionScheduleModel).where(SectionScheduleModel.section_id == section_id)
        result = await self.session.exec(query)
        return [SectionScheduleSchema.model_validate(s) for s in result.all()]

    async def update_schedule(self, schedule_id: int, data: SectionScheduleUpdateSchema) -> SectionScheduleSchema:
        query = select(SectionScheduleModel).where(SectionScheduleModel.schedule_id == schedule_id)
        result = await self.session.exec(query)
        schedule = result.first()
        if not schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(schedule, key, value)
        self.session.add(schedule)
        await self.session.commit()
        await self.session.refresh(schedule)
        return SectionScheduleSchema.model_validate(schedule)

    async def delete_schedule(self, schedule_id: int) -> bool:
        query = select(SectionScheduleModel).where(SectionScheduleModel.schedule_id == schedule_id)
        result = await self.session.exec(query)
        schedule = result.first()
        if not schedule:
            return False
        await self.session.delete(schedule)
        await self.session.commit()
        return True
