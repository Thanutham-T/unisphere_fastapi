from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime, time
from enum import Enum


# Course Schemas
class CourseBase(BaseModel):
    course_code: str
    course_name: str
    instructor: Optional[str] = None
    location: Optional[str] = None
    day_of_week: str
    start_time: time
    end_time: time
    credits: int = 3
    color: str = "#3B82F6"
    notes: Optional[str] = None


class CourseCreate(CourseBase):
    @validator('day_of_week')
    def validate_day_of_week(cls, v):
        valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if v.lower() not in valid_days:
            raise ValueError('Invalid day of week')
        return v.lower()


class CourseUpdate(BaseModel):
    course_code: Optional[str] = None
    course_name: Optional[str] = None
    instructor: Optional[str] = None
    location: Optional[str] = None
    day_of_week: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    credits: Optional[int] = None
    color: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class CourseResponse(CourseBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Attendance Schemas
class AttendanceRecordBase(BaseModel):
    date: datetime
    status: str = "present"
    notes: Optional[str] = None


class AttendanceRecordCreate(AttendanceRecordBase):
    course_id: int

    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['present', 'absent', 'late']
        if v.lower() not in valid_statuses:
            raise ValueError('Invalid attendance status')
        return v.lower()


class AttendanceRecordResponse(AttendanceRecordBase):
    id: int
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Course with attendance
class CourseWithAttendance(CourseResponse):
    attendance_records: List[AttendanceRecordResponse] = []