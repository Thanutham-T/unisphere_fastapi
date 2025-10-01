from datetime import date, time
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StudentScheduleOverrideBaseSchema(BaseModel):
    user_id: int
    section_id: int
    schedule_date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: str = "active"
    note: Optional[str] = None


class StudentScheduleOverrideCreateSchema(StudentScheduleOverrideBaseSchema):
    pass


class StudentScheduleOverrideUpdateSchema(BaseModel):
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[str] = None
    note: Optional[str] = None


class StudentScheduleOverrideSchema(StudentScheduleOverrideBaseSchema):
    override_id: int

    model_config = ConfigDict(from_attributes=True)
