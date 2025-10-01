from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models.faculty_model import (FacultyModel,
                                            FacultyTranslationModel)
from unisphere.schemas.faculty_schema import (FacultyCreateSchema,
                                              FacultySchema,
                                              FacultyUpdateSchema)
from unisphere.schemas.faculty_translation_schema import (
    FacultyTranslationCreateSchema, FacultyTranslationSchema,
    FacultyTranslationUpdateSchema)

from .FacultyServiceInterface import FacultyServiceInterface


class DBFacultyService(FacultyServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    # ==============================
    # Faculty CRUD
    # ==============================
    async def create_faculty(self, data: FacultyCreateSchema) -> FacultySchema:
        faculty = FacultyModel.from_orm(data)
        self.session.add(faculty)
        await self.session.commit()
        await self.session.refresh(faculty)
        return FacultySchema.from_orm(faculty)

    async def get_faculty(self, faculty_id: int) -> FacultySchema:
        faculty = await self.session.get(FacultyModel, faculty_id)
        if not faculty:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")
        return FacultySchema.from_orm(faculty)

    async def update_faculty(self, faculty_id: int, data: FacultyUpdateSchema) -> FacultySchema:
        faculty = await self.session.get(FacultyModel, faculty_id)
        if not faculty:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")

        for field, value in data.dict(exclude_unset=True).items():
            setattr(faculty, field, value)

        self.session.add(faculty)
        await self.session.commit()
        await self.session.refresh(faculty)
        return FacultySchema.from_orm(faculty)

    async def delete_faculty(self, faculty_id: int) -> None:
        faculty = await self.session.get(FacultyModel, faculty_id)
        if not faculty:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")

        await self.session.delete(faculty)
        await self.session.commit()

    async def list_faculties(self, status: Optional[str] = None) -> List[FacultySchema]:
        query = select(FacultyModel)
        if status:
            query = query.where(FacultyModel.status == status)
        result = await self.session.execute(query)
        faculties = result.scalars().all()
        return [FacultySchema.from_orm(f) for f in faculties]

    # ==============================
    # Faculty Translation CRUD
    # ==============================
    async def create_translation(self, data: FacultyTranslationCreateSchema) -> FacultyTranslationSchema:
        translation = FacultyTranslationModel.from_orm(data)
        self.session.add(translation)
        await self.session.commit()
        await self.session.refresh(translation)
        return FacultyTranslationSchema.from_orm(translation)

    async def get_translation(self, faculty_id: int, language_code: str) -> FacultyTranslationSchema:
        query = select(FacultyTranslationModel).where(
            FacultyTranslationModel.faculty_id == faculty_id,
            FacultyTranslationModel.language_code == language_code
        )
        result = await self.session.execute(query)
        translation = result.scalar_one_or_none()
        if not translation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Translation not found")
        return FacultyTranslationSchema.from_orm(translation)

    async def update_translation(
        self, faculty_id: int, language_code: str, data: FacultyTranslationUpdateSchema
    ) -> FacultyTranslationSchema:
        query = select(FacultyTranslationModel).where(
            FacultyTranslationModel.faculty_id == faculty_id,
            FacultyTranslationModel.language_code == language_code
        )
        result = await self.session.execute(query)
        translation = result.scalar_one_or_none()
        if not translation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Translation not found")

        for field, value in data.dict(exclude_unset=True).items():
            setattr(translation, field, value)

        self.session.add(translation)
        await self.session.commit()
        await self.session.refresh(translation)
        return FacultyTranslationSchema.from_orm(translation)

    async def delete_translation(self, faculty_id: int, language_code: str) -> None:
        query = select(FacultyTranslationModel).where(
            FacultyTranslationModel.faculty_id == faculty_id,
            FacultyTranslationModel.language_code == language_code
        )
        result = await self.session.execute(query)
        translation = result.scalar_one_or_none()
        if not translation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Translation not found")

        await self.session.delete(translation)
        await self.session.commit()

    async def list_translations(self, faculty_id: int) -> List[FacultyTranslationSchema]:
        query = select(FacultyTranslationModel).where(FacultyTranslationModel.faculty_id == faculty_id)
        result = await self.session.execute(query)
        translations = result.scalars().all()
        return [FacultyTranslationSchema.from_orm(t) for t in translations]
