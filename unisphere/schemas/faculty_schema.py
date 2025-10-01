from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class FacultyBaseSchema(BaseModel):
    faculty_code: str
    status: str = "active"


class FacultyCreateSchema(FacultyBaseSchema):
    pass


class FacultyUpdateSchema(BaseModel):
    faculty_code: Optional[str] = None
    status: Optional[str] = None
    archived_at: Optional[datetime] = None


class FacultySchema(FacultyBaseSchema):
    faculty_id: int
    archived_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
