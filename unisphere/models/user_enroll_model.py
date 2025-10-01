from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class UserEnrollBaseModel(SQLModel):
    user_id: int = Field(foreign_key="users.id")
    section_id: int = Field(foreign_key="sections.section_id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class UserEnrollModel(UserEnrollBaseModel, table=True):
    __tablename__ = 'user_enrolls'
    enroll_id: Optional[int] = Field(default=None, primary_key=True)
