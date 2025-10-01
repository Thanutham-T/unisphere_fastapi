from abc import ABC, abstractmethod
from typing import List, Optional

from unisphere.schemas.faculty_schema import (FacultyCreateSchema,
                                              FacultySchema,
                                              FacultyUpdateSchema)
from unisphere.schemas.faculty_translation_schema import (
    FacultyTranslationCreateSchema, FacultyTranslationSchema,
    FacultyTranslationUpdateSchema)


class FacultyServiceInterface(ABC):
    # ==============================
    # Faculty CRUD
    # ==============================
    @abstractmethod
    async def create_faculty(self, data: FacultyCreateSchema) -> FacultySchema:
        pass

    @abstractmethod
    async def get_faculty(self, faculty_id: int) -> FacultySchema:
        pass

    @abstractmethod
    async def update_faculty(self, faculty_id: int, data: FacultyUpdateSchema) -> FacultySchema:
        pass

    @abstractmethod
    async def delete_faculty(self, faculty_id: int) -> None:
        pass

    @abstractmethod
    async def list_faculties(self, status: Optional[str] = None) -> List[FacultySchema]:
        pass

    # ==============================
    # Faculty Translation CRUD
    # ==============================
    @abstractmethod
    async def create_translation(self, data: FacultyTranslationCreateSchema) -> FacultyTranslationSchema:
        pass

    @abstractmethod
    async def get_translation(self, faculty_id: int, language_code: str) -> FacultyTranslationSchema:
        pass

    @abstractmethod
    async def update_translation(
        self, faculty_id: int, language_code: str, data: FacultyTranslationUpdateSchema
    ) -> FacultyTranslationSchema:
        pass

    @abstractmethod
    async def delete_translation(self, faculty_id: int, language_code: str) -> None:
        pass

    @abstractmethod
    async def list_translations(self, faculty_id: int) -> List[FacultyTranslationSchema]:
        pass
