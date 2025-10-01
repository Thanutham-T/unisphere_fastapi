from abc import ABC, abstractmethod
from typing import List, Optional

from unisphere.schemas.section_instructor_schema import (
    SectionInstructorCreateSchema, SectionInstructorSchema)
from unisphere.schemas.section_rrule_schema import (SectionRRuleCreateSchema,
                                                    SectionRRuleSchema,
                                                    SectionRRuleUpdateSchema)
from unisphere.schemas.section_schema import (SectionCreateSchema,
                                              SectionSchema,
                                              SectionUpdateSchema)


class SectionServiceInterface(ABC):
    @abstractmethod
    async def create_section(self, data: SectionCreateSchema) -> SectionSchema:
        pass

    @abstractmethod
    async def get_section(self, section_id: int) -> SectionSchema:
        pass

    @abstractmethod
    async def update_section(self, section_id: int, data: SectionUpdateSchema) -> SectionSchema:
        pass

    @abstractmethod
    async def delete_section(self, section_id: int) -> bool:
        pass

    @abstractmethod
    async def list_sections(self, course_id: Optional[int] = None) -> List[SectionSchema]:
        pass

    # Section Instructor CRUD
    @abstractmethod
    async def assign_instructor(self, data: SectionInstructorCreateSchema) -> SectionInstructorSchema:
        pass

    @abstractmethod
    async def list_instructors(self, section_id: int) -> List[SectionInstructorSchema]:
        pass

    @abstractmethod
    async def remove_instructor(self, enroll_id: int) -> bool:
        pass
    
    # --- SectionRRule CRUD ---
    @abstractmethod
    async def create_rrule(self, data: SectionRRuleCreateSchema) -> SectionRRuleSchema:
        pass

    @abstractmethod
    async def get_rrule(self, rrule_id: int) -> SectionRRuleSchema:
        pass

    @abstractmethod
    async def update_rrule(self, rrule_id: int, data: SectionRRuleUpdateSchema) -> SectionRRuleSchema:
        pass

    @abstractmethod
    async def delete_rrule(self, rrule_id: int) -> bool:
        pass

    @abstractmethod
    async def list_rrules(self, section_id: int) -> list[SectionRRuleSchema]:
        pass