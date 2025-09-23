from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.dependencies import Base
import enum


class EventCategory(enum.Enum):
    ACADEMIC = "academic"
    SOCIAL = "social"
    SPORTS = "sports"
    CULTURAL = "cultural"
    WORKSHOP = "workshop"
    CONFERENCE = "conference"
    OTHER = "other"


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), default=EventCategory.OTHER.value)
    start_datetime = Column(DateTime(timezone=True), nullable=False)
    end_datetime = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(200), nullable=True)
    organizer = Column(String(100), nullable=True)
    max_participants = Column(Integer, nullable=True)
    registration_deadline = Column(DateTime(timezone=True), nullable=True)
    is_registration_required = Column(Boolean, default=False)
    image_url = Column(String(500), nullable=True)
    contact_info = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    participants = relationship("User", secondary="user_events", back_populates="events")


class StudyGroup(Base):
    __tablename__ = "study_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=False)
    course_code = Column(String(20), nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    max_members = Column(Integer, default=10)
    meeting_location = Column(String(200), nullable=True)
    meeting_time = Column(String(100), nullable=True)  # Flexible time description
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    creator = relationship("User", back_populates="created_study_groups")
    members = relationship("User", secondary="user_study_groups", back_populates="study_groups")
    messages = relationship("StudyGroupMessage", back_populates="study_group")


class StudyGroupMessage(Base):
    __tablename__ = "study_group_messages"

    id = Column(Integer, primary_key=True, index=True)
    study_group_id = Column(Integer, ForeignKey("study_groups.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    study_group = relationship("StudyGroup", back_populates="messages")
    sender = relationship("User")