# Import all models to register them with SQLAlchemy
from .user_model import User, UserRole, user_events, user_study_groups
from .course_model import Course, AttendanceRecord, DayOfWeek
from .event_model import Event, StudyGroup, StudyGroupMessage, EventCategory
from .announcement_model import Announcement, AnnouncementBookmark, Location, AnnouncementCategory

__all__ = [
    "User", "UserRole", "user_events", "user_study_groups",
    "Course", "AttendanceRecord", "DayOfWeek", 
    "Event", "StudyGroup", "StudyGroupMessage", "EventCategory",
    "Announcement", "AnnouncementBookmark", "Location", "AnnouncementCategory"
]