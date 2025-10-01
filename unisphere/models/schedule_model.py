from datetime import time
from typing import Optional

from sqlmodel import Field, SQLModel


class SectionScheduleBaseModel(SQLModel):
    section_id: int = Field(foreign_key="sections.section_id")
    day_id: int = Field(foreign_key="day_of_weeks.day_id")
    start_time: time
    end_time: time
    note: Optional[str] = None


class SectionScheduleModel(SectionScheduleBaseModel, table=True):
    __tablename__ = 'section_schedules'
    schedule_id: Optional[int] = Field(default=None, primary_key=True)


class SectionRRuleBaseModel(SQLModel):
    section_id: int = Field(foreign_key="sections.section_id")
    rrule: str


class SectionRRuleModel(SectionRRuleBaseModel, table=True):
    __tablename__ = 'section_rrules'
    rrule_id: Optional[int] = Field(default=None, primary_key=True)
