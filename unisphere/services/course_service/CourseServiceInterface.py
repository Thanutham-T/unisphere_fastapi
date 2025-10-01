from abc import ABC, abstractmethod
from typing import List, Optional

from unisphere.schemas.course_schema import (CourseCreateSchema, CourseSchema,
                                             CourseUpdateSchema)
from unisphere.schemas.course_translation_schema import (
    CourseTranslationCreateSchema, CourseTranslationSchema,
    CourseTranslationUpdateSchema)
from unisphere.schemas.user_enroll_schema import UserEnrollSchema


class CourseServiceInterface(ABC):
    @abstractmethod
    async def get_courses_by_semester(self, semester_id: int) -> List[CourseSchema]:
        pass

    @abstractmethod
    async def get_user_courses(self, user_id: int, semester_id: Optional[int] = None) -> List[CourseSchema]:
        pass

    @abstractmethod
    async def enroll_user_to_course(self, user_id: int, course_id: int) -> UserEnrollSchema:
        pass

    @abstractmethod
    async def withdraw_user_from_course(self, user_id: int, course_id: int) -> bool:
        pass

    @abstractmethod
    async def create_course(self, course_data: CourseCreateSchema) -> CourseSchema:
        pass

    @abstractmethod
    async def update_course(self, course_id: int, course_data: CourseUpdateSchema) -> CourseSchema:
        pass

    @abstractmethod
    async def delete_course(self, course_id: int) -> bool:
        pass

    @abstractmethod
    async def create_translation(self, data: CourseTranslationCreateSchema) -> CourseTranslationSchema:
        pass

    @abstractmethod
    async def get_translation(self, course_id: int, language_code: str) -> CourseTranslationSchema:
        pass

    @abstractmethod
    async def update_translation(
        self, course_id: int, language_code: str, data: CourseTranslationUpdateSchema
    ) -> CourseTranslationSchema:
        pass

    @abstractmethod
    async def delete_translation(self, course_id: int, language_code: str) -> bool:
        pass

    @abstractmethod
    async def list_translations(self, course_id: int) -> list[CourseTranslationSchema]:
        pass