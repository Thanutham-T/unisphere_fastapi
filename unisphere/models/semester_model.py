from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class SemesterBaseModel(SQLModel):
    semester_code: str = Field(unique=True, max_length=20)
    start_date: date
    end_date: date
    status: str = Field(default="active", max_length=20)
    archived_at: Optional[datetime] = None


class SemesterModel(SemesterBaseModel, table=True):
    __tablename__ = "semesters"
    semester_id: Optional[int] = Field(default=None, primary_key=True)
