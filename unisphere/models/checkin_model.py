from datetime import date, datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class UserCheckinBaseModel(SQLModel):
    user_id: int = Field(foreign_key="users.id")
    section_id: int = Field(foreign_key="sections.section_id")
    schedule_date: date
    checkin_time: datetime = Field(
        default_factory=datetime.now(timezone.utc))
    # pending, present, absent
    status: str = Field(default="pending", max_length=20)
    source: Optional[str] = None
    note: Optional[str] = None


class UserCheckinModel(UserCheckinBaseModel, table=True):
    __tablename__ = "user_checkins"
    checkin_id: Optional[int] = Field(default=None, primary_key=True)
