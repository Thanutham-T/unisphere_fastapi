from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AnnouncementBase(BaseModel):
    title: str
    content: str
    category: str  # academic, cultural, general, etc.
    priority: str = "medium"  # low, medium, high
    date: datetime


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    date: Optional[datetime] = None


class Announcement(AnnouncementBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnnouncementResponse(Announcement):
    creator_name: Optional[str] = None  # Full name of the creator
