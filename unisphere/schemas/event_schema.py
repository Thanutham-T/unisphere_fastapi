from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[str] = None
    date: datetime
    # Maximum number of participants (null = unlimited)
    max_capacity: Optional[int] = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    date: Optional[datetime] = None
    max_capacity: Optional[int] = None


class Event(EventBase):
    id: int
    status: str
    created_by: int
    created_at: datetime
    updated_at: datetime
    registration_count: int = 0  # Current number of registered participants

    model_config = ConfigDict(from_attributes=True)


class EventResponse(Event):
    is_registered: bool = False
    is_full: bool = False  # Whether the event has reached max capacity


class EventRegistrationCreate(BaseModel):
    notes: Optional[str] = None


class EventRegistration(BaseModel):
    id: int
    event_id: int
    user_id: int
    notes: Optional[str] = None
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)
