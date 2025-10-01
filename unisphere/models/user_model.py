from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from unisphere.models.announcement_model import Announcement
    from unisphere.models.event_model import Event


# User schema
class UserBase(SQLModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str = Field(unique=True, index=True, max_length=255)
    phone_number: Optional[str] = Field(default=None, max_length=20)
    profile_image_url: Optional[str] = Field(default=None, max_length=500)
    role: str = Field(default="user", max_length=50)

    # Student information
    student_id: Optional[str] = Field(default=None, max_length=20)

    # Education information
    faculty: Optional[str] = Field(default=None, max_length=100)
    department: Optional[str] = Field(default=None, max_length=100)
    major: Optional[str] = Field(default=None, max_length=100)
    curriculum: Optional[str] = Field(default=None, max_length=100)
    education_level: Optional[str] = Field(default=None, max_length=50)
    campus: Optional[str] = Field(default=None, max_length=100)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    password_hash: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    created_events: List["Event"] = Relationship(back_populates="creator")
    created_announcements: List["Announcement"] = Relationship(
        back_populates="creator")
