from abc import ABC, abstractmethod
from typing import List

from unisphere.schemas.day_of_week_schema import (DayOfWeekCreateSchema,
                                                  DayOfWeekSchema,
                                                  DayOfWeekUpdateSchema)
from unisphere.schemas.day_of_week_translation_schema import (
    DayTranslationCreateSchema, DayTranslationSchema,
    DayTranslationUpdateSchema)


class DayOfWeekServiceInterface(ABC):

    # --- Day CRUD ---
    @abstractmethod
    async def create_day(self, data: DayOfWeekCreateSchema) -> DayOfWeekSchema:
        pass

    @abstractmethod
    async def get_day(self, day_id: int) -> DayOfWeekSchema:
        pass

    @abstractmethod
    async def update_day(self, day_id: int, data: DayOfWeekUpdateSchema) -> DayOfWeekSchema:
        pass

    @abstractmethod
    async def delete_day(self, day_id: int) -> bool:
        pass

    @abstractmethod
    async def list_days(self) -> list[DayOfWeekSchema]:
        pass

    # --- Day Translation CRUD ---
    @abstractmethod
    async def create_translation(self, data: DayTranslationCreateSchema) -> DayTranslationSchema:
        pass

    @abstractmethod
    async def get_translation(self, day_id: int, language_code: str) -> DayTranslationSchema:
        pass

    @abstractmethod
    async def update_translation(self, day_id: int, language_code: str, data: DayTranslationUpdateSchema) -> DayTranslationSchema:
        pass

    @abstractmethod
    async def delete_translation(self, day_id: int, language_code: str) -> bool:
        pass

    @abstractmethod
    async def list_translations(self, day_id: int) -> list[DayTranslationSchema]:
        pass
