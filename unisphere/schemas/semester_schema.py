from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SemesterBaseSchema(BaseModel):
    semester_code: str
    start_date: datetime
    end_date: datetime
    status: str = "active"


class SemesterCreateSchema(SemesterBaseSchema):
    pass


class SemesterUpdateSchema(BaseModel):
    semester_code: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    archived_at: Optional[datetime] = None


class SemesterSchema(SemesterBaseSchema):
    semester_id: int
    archived_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
