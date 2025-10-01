from datetime import time
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserScheduleTemplateBaseSchema(BaseModel):
    user_id: int
    section_id: int
    day_id: int
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: str = "active"
    note: Optional[str] = None


class UserScheduleTemplateCreateSchema(UserScheduleTemplateBaseSchema):
    pass


class UserScheduleTemplateUpdateSchema(BaseModel):
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[str] = None
    note: Optional[str] = None


class UserScheduleTemplateSchema(UserScheduleTemplateBaseSchema):
    template_id: int

    model_config = ConfigDict(from_attributes=True)
