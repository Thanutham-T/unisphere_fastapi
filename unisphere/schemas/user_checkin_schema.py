from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserCheckinBaseSchema(BaseModel):
    user_id: int
    section_id: int
    schedule_date: date
    status: str = "present"
    source: Optional[str] = None
    note: Optional[str] = None


class UserCheckinCreateSchema(UserCheckinBaseSchema):
    pass


class UserCheckinUpdateSchema(BaseModel):
    status: Optional[str] = None
    source: Optional[str] = None
    note: Optional[str] = None


class UserCheckinSchema(UserCheckinBaseSchema):
    checkin_id: int
    checkin_time: datetime

    model_config = ConfigDict(from_attributes=True)
