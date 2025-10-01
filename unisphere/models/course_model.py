from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class CourseBaseModel(SQLModel):
    branch_id: int = Field(foreign_key="branchs.branch_id")
    semester_id: int = Field(foreign_key="semesters.semester_id")
    course_code: str = Field(max_length=50, unique=True)
    status: str = Field(default="active", max_length=20)
    archived_at: Optional[datetime] = None


class CourseModel(CourseBaseModel, table=True):
    __tablename__ = "courses"
    course_id: Optional[int] = Field(default=None, primary_key=True)


class CourseTranslationBaseModel(SQLModel):
    course_id: int = Field(foreign_key="courses.course_id")
    language_code: str = Field(max_length=10)
    subject_name: str = Field(max_length=255)
    description: Optional[str] = None


class CourseTranslationModel(CourseTranslationBaseModel, table=True):
    __tablename__ = "course_translations"
    course_id: int = Field(foreign_key="courses.course_id", primary_key=True)
    language_code: str = Field(primary_key=True, max_length=10)
