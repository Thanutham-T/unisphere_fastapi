from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models.semester_model import SemesterModel
from unisphere.schemas import semester_schema

from .SemesterServiceInterface import SemesterServiceInterface


class DBSemesterService(SemesterServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_semesters(self, include_archived: bool = False) -> List[SemesterModel]:
        query = select(SemesterModel)
        if not include_archived:
            query = query.where(SemesterModel.archived_at.is_(None))
        result = await self.session.exec(query)
        return result.all()

    async def get_semester_by_id(self, semester_id: int) -> SemesterModel:
        result = await self.session.exec(select(SemesterModel).where(SemesterModel.semester_id == semester_id))
        semester = result.first()
        if not semester:
            raise HTTPException(status_code=404, detail="Semester not found")
        return semester

    async def create_semester(self, semester_create: semester_schema.SemesterCreateSchema) -> SemesterModel:
        new_semester = SemesterModel(**semester_create.model_dump())
        self.session.add(new_semester)
        await self.session.commit()
        await self.session.refresh(new_semester)
        return new_semester

    async def update_semester(self, semester_id: int, semester_update: semester_schema.SemesterUpdateSchema) -> SemesterModel:
        result = await self.session.exec(select(SemesterModel).where(SemesterModel.semester_id == semester_id))
        semester = result.first()
        if not semester:
            raise HTTPException(status_code=404, detail="Semester not found")

        update_data = semester_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(semester, field, value)

        self.session.add(semester)
        await self.session.commit()
        await self.session.refresh(semester)
        return semester

    async def delete_semester(self, semester_id: int) -> SemesterModel:
        result = await self.session.exec(select(SemesterModel).where(SemesterModel.semester_id == semester_id))
        semester = result.first()
        if not semester:
            raise HTTPException(status_code=404, detail="Semester not found")

        await self.session.delete(semester)
        await self.session.commit()
        return semester

    async def archive_semester(self, semester_id: int, archived_at: Optional[datetime] = None) -> SemesterModel:
        result = await self.session.exec(select(SemesterModel).where(SemesterModel.semester_id == semester_id))
        semester = result.first()
        if not semester:
            raise HTTPException(status_code=404, detail="Semester not found")

        semester.archived_at = archived_at or datetime.utcnow()
        self.session.add(semester)
        await self.session.commit()
        await self.session.refresh(semester)
        return semester
