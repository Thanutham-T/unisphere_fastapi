from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.dependencies import Base
import enum


class AnnouncementCategory(enum.Enum):
    ACADEMIC = "academic"
    ADMINISTRATIVE = "administrative"
    EVENT = "event"
    GENERAL = "general"
    URGENT = "urgent"


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(50), default=AnnouncementCategory.GENERAL.value)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_faculty = Column(String(100), nullable=True)  # If null, for all
    target_year = Column(Integer, nullable=True)  # If null, for all years
    is_pinned = Column(Boolean, default=False)
    is_urgent = Column(Boolean, default=False)
    image_url = Column(String(500), nullable=True)
    attachment_url = Column(String(500), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    author = relationship("User", back_populates="announcements")
    bookmarks = relationship("AnnouncementBookmark", back_populates="announcement")


class AnnouncementBookmark(Base):
    __tablename__ = "announcement_bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    announcement_id = Column(Integer, ForeignKey("announcements.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    announcement = relationship("Announcement", back_populates="bookmarks")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    building = Column(String(100), nullable=True)
    floor = Column(String(10), nullable=True)
    room_number = Column(String(20), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    opening_hours = Column(Text, nullable=True)  # JSON string
    contact_info = Column(String(200), nullable=True)
    category = Column(String(50), nullable=True)  # classroom, library, cafeteria, etc.
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())