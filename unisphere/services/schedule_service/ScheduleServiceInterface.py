from abc import ABC, abstractmethod
from typing import List

from unisphere.schemas.schedule_schema import (SectionScheduleCreateSchema,
                                               SectionScheduleSchema,
                                               SectionScheduleUpdateSchema)


class ScheduleServiceInterface(ABC):

    @abstractmethod
    async def create_schedule(self, data: SectionScheduleCreateSchema) -> SectionScheduleSchema:
        pass

    @abstractmethod
    async def list_schedules(self, section_id: int) -> List[SectionScheduleSchema]:
        pass

    @abstractmethod
    async def update_schedule(self, schedule_id: int, data: SectionScheduleUpdateSchema) -> SectionScheduleSchema:
        pass

    @abstractmethod
    async def delete_schedule(self, schedule_id: int) -> bool:
        pass
