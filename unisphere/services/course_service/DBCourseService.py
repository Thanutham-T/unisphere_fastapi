from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models.course_model import CourseModel, CourseTranslationModel
from unisphere.models.user_enroll_model import UserEnrollModel
from unisphere.schemas.course_schema import (CourseCreateSchema, CourseSchema,
                                             CourseUpdateSchema)
from unisphere.schemas.course_translation_schema import (
    CourseTranslationCreateSchema, CourseTranslationSchema,
    CourseTranslationUpdateSchema)
from unisphere.schemas.user_enroll_schema import UserEnrollSchema

from .CourseServiceInterface import CourseServiceInterface


class DBCourseService(CourseServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    # ----------------------
    # Course CRUD
    # ----------------------
    async def get_courses_by_semester(self, semester_id: int) -> List[CourseSchema]:
        query = select(CourseModel).where(CourseModel.semester_id == semester_id)
        result = await self.session.exec(query)
        return [CourseSchema.model_validate(c) for c in result.all()]

    async def get_user_courses(self, user_id: int, semester_id: Optional[int] = None) -> List[CourseSchema]:
        query = select(CourseModel).join(UserEnrollModel).where(UserEnrollModel.user_id == user_id)
        if semester_id:
            query = query.where(CourseModel.semester_id == semester_id)
        result = await self.session.exec(query)
        return [CourseSchema.model_validate(c) for c in result.all()]

    async def enroll_user_to_course(self, user_id: int, course_id: int) -> UserEnrollSchema:
        enroll = UserEnrollModel(user_id=user_id, course_id=course_id, section_id=1)
        self.session.add(enroll)
        await self.session.commit()
        await self.session.refresh(enroll)
        return UserEnrollSchema.model_validate(enroll)

    async def withdraw_user_from_course(self, user_id: int, course_id: int) -> bool:
        query = select(UserEnrollModel).where(
            UserEnrollModel.user_id == user_id,
            UserEnrollModel.course_id == course_id
        )
        result = await self.session.exec(query)
        enrollment = result.first()
        if not enrollment:
            return False
        await self.session.delete(enrollment)
        await self.session.commit()
        return True

    async def create_course(self, course_data: CourseCreateSchema) -> CourseSchema:
        course = CourseModel(**course_data.model_dump())
        self.session.add(course)
        await self.session.commit()
        await self.session.refresh(course)
        return CourseSchema.model_validate(course)

    async def update_course(self, course_id: int, course_data: CourseUpdateSchema) -> CourseSchema:
        query = select(CourseModel).where(CourseModel.course_id == course_id)
        result = await self.session.exec(query)
        course = result.first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        for key, value in course_data.model_dump(exclude_unset=True).items():
            setattr(course, key, value)
        self.session.add(course)
        await self.session.commit()
        await self.session.refresh(course)
        return CourseSchema.model_validate(course)

    async def delete_course(self, course_id: int) -> bool:
        query = select(CourseModel).where(CourseModel.course_id == course_id)
        result = await self.session.exec(query)
        course = result.first()
        if not course:
            return False
        await self.session.delete(course)
        await self.session.commit()
        return True

    # ----------------------
    # Course Translation CRUD
    # ----------------------
    async def create_translation(self, data: CourseTranslationCreateSchema) -> CourseTranslationSchema:
        translation = CourseTranslationModel.from_orm(data)
        self.session.add(translation)
        await self.session.commit()
        await self.session.refresh(translation)
        return CourseTranslationSchema.model_validate(translation)

    async def get_translation(self, course_id: int, language_code: str) -> CourseTranslationSchema:
        query = select(CourseTranslationModel).where(
            CourseTranslationModel.course_id == course_id,
            CourseTranslationModel.language_code == language_code
        )
        result = await self.session.exec(query)
        translation = result.first()
        if not translation:
            raise HTTPException(status_code=404, detail="Translation not found")
        return CourseTranslationSchema.model_validate(translation)

    async def update_translation(
        self, course_id: int, language_code: str, data: CourseTranslationUpdateSchema
    ) -> CourseTranslationSchema:
        query = select(CourseTranslationModel).where(
            CourseTranslationModel.course_id == course_id,
            CourseTranslationModel.language_code == language_code
        )
        result = await self.session.exec(query)
        translation = result.first()
        if not translation:
            raise HTTPException(status_code=404, detail="Translation not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(translation, key, value)
        self.session.add(translation)
        await self.session.commit()
        await self.session.refresh(translation)
        return CourseTranslationSchema.model_validate(translation)

    async def delete_translation(self, course_id: int, language_code: str) -> bool:
        query = select(CourseTranslationModel).where(
            CourseTranslationModel.course_id == course_id,
            CourseTranslationModel.language_code == language_code
        )
        result = await self.session.exec(query)
        translation = result.first()
        if not translation:
            return False
        await self.session.delete(translation)
        await self.session.commit()
        return True

    async def list_translations(self, course_id: int) -> List[CourseTranslationSchema]:
        query = select(CourseTranslationModel).where(CourseTranslationModel.course_id == course_id)
        result = await self.session.exec(query)
        translations = result.all()
        return [CourseTranslationSchema.model_validate(t) for t in translations]
