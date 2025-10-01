from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SectionBaseSchema(BaseModel):
    course_id: int
    section_code: str
    student_limit: int
    status: str = "active"


class SectionCreateSchema(SectionBaseSchema):
    pass


class SectionUpdateSchema(BaseModel):
    course_id: Optional[int] = None
    section_code: Optional[str] = None
    student_limit: Optional[int] = None
    status: Optional[str] = None
    archived_at: Optional[datetime] = None


class SectionSchema(SectionBaseSchema):
    section_id: int
    archived_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
