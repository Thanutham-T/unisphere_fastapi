from datetime import datetime, timezone
from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models.schedule_model import SectionRRuleModel
from unisphere.models.section_instructor import SectionInstructorModel
from unisphere.models.section_model import SectionModel
from unisphere.schemas.section_instructor_schema import (
    SectionInstructorCreateSchema, SectionInstructorSchema)
from unisphere.schemas.section_rrule_schema import (SectionRRuleCreateSchema,
                                                    SectionRRuleSchema,
                                                    SectionRRuleUpdateSchema)
from unisphere.schemas.section_schema import (SectionCreateSchema,
                                              SectionSchema,
                                              SectionUpdateSchema)

from .SectionServiceInterface import SectionServiceInterface


class DBSectionService(SectionServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    # ----------------------
    # Section CRUD
    # ----------------------
    async def create_section(self, data: SectionCreateSchema) -> SectionSchema:
        section = SectionModel(**data.model_dump())
        self.session.add(section)
        await self.session.commit()
        await self.session.refresh(section)
        return SectionSchema.model_validate(section)

    async def get_section(self, section_id: int) -> SectionSchema:
        query = select(SectionModel).where(SectionModel.section_id == section_id)
        result = await self.session.exec(query)
        section = result.first()
        if not section:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
        return SectionSchema.model_validate(section)

    async def update_section(self, section_id: int, data: SectionUpdateSchema) -> SectionSchema:
        query = select(SectionModel).where(SectionModel.section_id == section_id)
        result = await self.session.exec(query)
        section = result.first()
        if not section:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(section, key, value)
        self.session.add(section)
        await self.session.commit()
        await self.session.refresh(section)
        return SectionSchema.model_validate(section)

    async def delete_section(self, section_id: int) -> bool:
        query = select(SectionModel).where(SectionModel.section_id == section_id)
        result = await self.session.exec(query)
        section = result.first()
        if not section:
            return False
        await self.session.delete(section)
        await self.session.commit()
        return True

    async def list_sections(self, course_id: Optional[int] = None) -> List[SectionSchema]:
        query = select(SectionModel)
        if course_id is not None:
            query = query.where(SectionModel.course_id == course_id)
        result = await self.session.exec(query)
        return [SectionSchema.model_validate(s) for s in result.all()]

    # ----------------------
    # Section Instructor CRUD
    # ----------------------
    async def assign_instructor(self, data: SectionInstructorCreateSchema) -> SectionInstructorSchema:
        instructor = SectionInstructorModel(
            user_id=data.user_id,
            section_id=data.section_id,
            created_at=datetime.now(timezone.utc)
        )
        self.session.add(instructor)
        await self.session.commit()
        await self.session.refresh(instructor)
        return SectionInstructorSchema.model_validate(instructor)

    async def list_instructors(self, section_id: int) -> List[SectionInstructorSchema]:
        query = select(SectionInstructorModel).where(SectionInstructorModel.section_id == section_id)
        result = await self.session.exec(query)
        return [SectionInstructorSchema.model_validate(i) for i in result.all()]

    async def remove_instructor(self, enroll_id: int) -> bool:
        query = select(SectionInstructorModel).where(SectionInstructorModel.enroll_id == enroll_id)
        result = await self.session.exec(query)
        instructor = result.first()
        if not instructor:
            return False
        await self.session.delete(instructor)
        await self.session.commit()
        return True

# ----------------------
# Section RRule CRUD
# ----------------------
async def create_rrule(self, data: SectionRRuleCreateSchema) -> SectionRRuleSchema:
    rrule = SectionRRuleModel(**data.model_dump())
    self.session.add(rrule)
    await self.session.commit()
    await self.session.refresh(rrule)
    return SectionRRuleSchema.model_validate(rrule)

async def get_rrule(self, rrule_id: int) -> SectionRRuleSchema:
    query = select(SectionRRuleModel).where(SectionRRuleModel.rrule_id == rrule_id)
    result = await self.session.exec(query)
    rrule = result.first()
    if not rrule:
        raise HTTPException(status_code=404, detail="RRule not found")
    return SectionRRuleSchema.model_validate(rrule)

async def update_rrule(self, rrule_id: int, data: SectionRRuleUpdateSchema) -> SectionRRuleSchema:
    query = select(SectionRRuleModel).where(SectionRRuleModel.rrule_id == rrule_id)
    result = await self.session.exec(query)
    rrule = result.first()
    if not rrule:
        raise HTTPException(status_code=404, detail="RRule not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(rrule, key, value)
    self.session.add(rrule)
    await self.session.commit()
    await self.session.refresh(rrule)
    return SectionRRuleSchema.model_validate(rrule)

async def delete_rrule(self, rrule_id: int) -> bool:
    query = select(SectionRRuleModel).where(SectionRRuleModel.rrule_id == rrule_id)
    result = await self.session.exec(query)
    rrule = result.first()
    if not rrule:
        return False
    await self.session.delete(rrule)
    await self.session.commit()
    return True

async def list_rrules(self, section_id: int) -> list[SectionRRuleSchema]:
    query = select(SectionRRuleModel).where(SectionRRuleModel.section_id == section_id)
    result = await self.session.exec(query)
    return [SectionRRuleSchema.model_validate(r) for r in result.all()]