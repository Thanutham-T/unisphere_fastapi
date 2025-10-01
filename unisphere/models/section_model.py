from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class SectionBaseModel(SQLModel):
    course_id: int = Field(foreign_key="courses.course_id")
    section_code: str = Field(max_length=50)
    student_limit: int
    status: str = Field(default="active", max_length=20)
    archived_at: Optional[datetime] = None


class SectionModel(SectionBaseModel, table=True):
    __tablename__ = "sections"
    section_id: Optional[int] = Field(default=None, primary_key=True)
