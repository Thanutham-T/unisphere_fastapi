from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from unisphere.models.user_model import User

# Announcement Models


class AnnouncementBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    category: str = Field(max_length=100)  # academic, cultural, general, etc.
    priority: str = Field(default="medium", max_length=50)  # low, medium, high
    date: datetime


class Announcement(AnnouncementBase, table=True):
    __tablename__ = "announcements"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_by: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    creator: Optional["User"] = Relationship(
        back_populates="created_announcements")
