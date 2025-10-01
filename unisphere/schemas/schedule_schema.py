from datetime import time
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SectionScheduleBaseSchema(BaseModel):
    section_id: int
    day_id: int
    start_time: time
    end_time: time
    note: Optional[str] = None


class SectionScheduleCreateSchema(SectionScheduleBaseSchema):
    pass


class SectionScheduleUpdateSchema(BaseModel):
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    note: Optional[str] = None


class SectionScheduleSchema(SectionScheduleBaseSchema):
    schedule_id: int

    model_config = ConfigDict(from_attributes=True)
