from typing import Optional

from sqlmodel import Field, SQLModel


class DayBaseModel(SQLModel):
    day_code: str = Field(max_length=10, unique=True)


class DayModel(DayBaseModel, table=True):
    __tablename__ = "day_of_weeks"
    day_id: Optional[int] = Field(default=None, primary_key=True)


class DayTranslationBaseModel(SQLModel):
    day_id: int = Field(foreign_key="day_of_weeks.day_id")
    language_code: str = Field(max_length=10)
    day_name: str = Field(max_length=20)


class DayTranslationModel(DayTranslationBaseModel, table=True):
    __tablename__ = "day_of_week_translations"
    day_id: int = Field(foreign_key="day_of_weeks.day_id", primary_key=True)
    language_code: str = Field(primary_key=True, max_length=10)
