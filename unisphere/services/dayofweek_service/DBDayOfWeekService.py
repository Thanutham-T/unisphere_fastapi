from typing import List

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models.day_of_week_model import DayModel, DayTranslationModel
from unisphere.schemas.day_of_week_schema import (DayOfWeekCreateSchema,
                                                  DayOfWeekSchema,
                                                  DayOfWeekUpdateSchema)
from unisphere.schemas.day_of_week_translation_schema import (
    DayTranslationCreateSchema, DayTranslationSchema,
    DayTranslationUpdateSchema)

from .DayOfWeekService import DayOfWeekServiceInterface


class DBDayOfWeekService(DayOfWeekServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    # ----------------------
    # Day CRUD
    # ----------------------
    async def create_day(self, data: DayOfWeekCreateSchema) -> DayOfWeekSchema:
        day = DayModel(**data.model_dump())
        self.session.add(day)
        await self.session.commit()
        await self.session.refresh(day)
        return DayOfWeekSchema.model_validate(day)

    async def get_day(self, day_id: int) -> DayOfWeekSchema:
        query = select(DayModel).where(DayModel.day_id == day_id)
        result = await self.session.exec(query)
        day = result.first()
        if not day:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
        return DayOfWeekSchema.model_validate(day)

    async def update_day(self, day_id: int, data: DayOfWeekUpdateSchema) -> DayOfWeekSchema:
        query = select(DayModel).where(DayModel.day_id == day_id)
        result = await self.session.exec(query)
        day = result.first()
        if not day:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(day, key, value)
        self.session.add(day)
        await self.session.commit()
        await self.session.refresh(day)
        return DayOfWeekSchema.model_validate(day)

    async def delete_day(self, day_id: int) -> bool:
        query = select(DayModel).where(DayModel.day_id == day_id)
        result = await self.session.exec(query)
        day = result.first()
        if not day:
            return False
        await self.session.delete(day)
        await self.session.commit()
        return True

    async def list_days(self) -> List[DayOfWeekSchema]:
        query = select(DayModel)
        result = await self.session.exec(query)
        return [DayOfWeekSchema.model_validate(d) for d in result.all()]

    # ----------------------
    # Day Translation CRUD
    # ----------------------
    async def create_translation(self, data: DayTranslationCreateSchema) -> DayTranslationSchema:
        translation = DayTranslationModel(**data.model_dump())
        self.session.add(translation)
        await self.session.commit()
        await self.session.refresh(translation)
        return DayTranslationSchema.model_validate(translation)

    async def get_translation(self, day_id: int, language_code: str) -> DayTranslationSchema:
        query = select(DayTranslationModel).where(
            DayTranslationModel.day_id == day_id,
            DayTranslationModel.language_code == language_code
        )
        result = await self.session.exec(query)
        translation = result.first()
        if not translation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Translation not found")
        return DayTranslationSchema.model_validate(translation)

    async def update_translation(self, day_id: int, language_code: str, data: DayTranslationUpdateSchema) -> DayTranslationSchema:
        query = select(DayTranslationModel).where(
            DayTranslationModel.day_id == day_id,
            DayTranslationModel.language_code == language_code
        )
        result = await self.session.exec(query)
        translation = result.first()
        if not translation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Translation not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(translation, key, value)
        self.session.add(translation)
        await self.session.commit()
        await self.session.refresh(translation)
        return DayTranslationSchema.model_validate(translation)

    async def delete_translation(self, day_id: int, language_code: str) -> bool:
        query = select(DayTranslationModel).where(
            DayTranslationModel.day_id == day_id,
            DayTranslationModel.language_code == language_code
        )
        result = await self.session.exec(query)
        translation = result.first()
        if not translation:
            return False
        await self.session.delete(translation)
        await self.session.commit()
        return True

    async def list_translations(self, day_id: int) -> List[DayTranslationSchema]:
        query = select(DayTranslationModel).where(DayTranslationModel.day_id == day_id)
        result = await self.session.exec(query)
        return [DayTranslationSchema.model_validate(t) for t in result.all()]
