from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from unisphere.schemas.semester_schema import (SemesterCreateSchema,
                                               SemesterSchema,
                                               SemesterUpdateSchema)


class SemesterServiceInterface(ABC):
    @abstractmethod
    async def create_semester(self, semester_create: SemesterCreateSchema) -> SemesterSchema:
        """
        Create a new semester.
        """
        pass

    @abstractmethod
    async def get_semester_by_id(self, semester_id: int) -> Optional[SemesterSchema]:
        """
        Retrieve a semester by its ID.
        """
        pass

    @abstractmethod
    async def get_all_semesters(self, include_archived: bool = False) -> List[SemesterSchema]:
        """
        Retrieve all semesters, optionally including archived ones.
        """
        pass

    @abstractmethod
    async def update_semester(
        self, semester_id: int, semester_update: SemesterUpdateSchema
    ) -> Optional[SemesterSchema]:
        """
        Update an existing semester by ID.
        """
        pass

    @abstractmethod
    async def delete_semester(self, semester_id: int) -> bool:
        """
        Delete a semester by ID.
        Returns True if deleted, False if not found.
        """
        pass

    @abstractmethod
    async def archive_semester(self, semester_id: int, archived_at: Optional[datetime] = None) -> Optional[SemesterSchema]:
        """
        Archive a semester by setting its archived_at datetime.
        """
        pass
