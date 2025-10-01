from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CourseBaseSchema(BaseModel):
    course_code: str
    branch_id: int
    semester_id: int
    status: str = "active"


class CourseCreateSchema(CourseBaseSchema):
    pass


class CourseUpdateSchema(BaseModel):
    course_code: Optional[str] = None
    branch_id: Optional[int] = None
    semester_id: Optional[int] = None
    status: Optional[str] = None
    archived_at: Optional[datetime] = None


class CourseSchema(CourseBaseSchema):
    course_id: int
    archived_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
