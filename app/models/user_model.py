from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.dependencies import Base
import enum


class UserRole(enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"
    FACULTY = "faculty"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    faculty = Column(String(100), nullable=True)
    year = Column(Integer, nullable=True)
    profile_image_url = Column(String(500), nullable=True)
    role = Column(String(20), default=UserRole.STUDENT.value)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    courses = relationship("Course", back_populates="user")
    events = relationship("Event", secondary="user_events", back_populates="participants")
    study_groups = relationship("StudyGroup", secondary="user_study_groups", back_populates="members")
    announcements = relationship("Announcement", back_populates="author")
    created_study_groups = relationship("StudyGroup", back_populates="creator")


# Association tables for many-to-many relationships
user_events = Table(
    'user_events',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('rsvp_status', String(20), default='pending'),  # pending, confirmed, declined
    Column('joined_at', DateTime(timezone=True), server_default=func.now())
)

user_study_groups = Table(
    'user_study_groups',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('study_group_id', Integer, ForeignKey('study_groups.id'), primary_key=True),
    Column('joined_at', DateTime(timezone=True), server_default=func.now())
)