from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.dependencies import Base
import enum


class DayOfWeek(enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_code = Column(String(20), nullable=False)
    course_name = Column(String(200), nullable=False)
    instructor = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    day_of_week = Column(String(20), nullable=False)  # Store as string for flexibility
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    credits = Column(Integer, default=3)
    color = Column(String(7), default="#3B82F6")  # Hex color for UI
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="courses")
    attendance_records = relationship("AttendanceRecord", back_populates="course")


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), default="present")  # present, absent, late
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    course = relationship("Course", back_populates="attendance_records")