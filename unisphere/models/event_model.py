from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from unisphere.models.user_model import User


# Event Models
class EventBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    category: Optional[str] = Field(default=None, max_length=100)
    image_url: Optional[str] = Field(default=None, max_length=500)
    location: Optional[str] = Field(default=None, max_length=255)
    # upcoming, ongoing, completed
    status: str = Field(default="upcoming", max_length=50)
    date: datetime
    # Maximum number of participants (null = unlimited)
    max_capacity: Optional[int] = Field(default=None, ge=1)
    # Current number of registered participants
    registration_count: int = Field(default=0, ge=0)


class Event(EventBase, table=True):
    __tablename__ = "events"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_by: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    creator: Optional["User"] = Relationship(back_populates="created_events")
    registrations: List["EventRegistration"] = Relationship(
        back_populates="event")


# Event Registration Models
class EventRegistrationBase(SQLModel):
    notes: Optional[str] = Field(default=None)


class EventRegistration(EventRegistrationBase, table=True):
    __tablename__ = "event_registrations"

    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="events.id")
    user_id: int = Field(foreign_key="users.id")
    registered_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    event: Optional[Event] = Relationship(back_populates="registrations")
