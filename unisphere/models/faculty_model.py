from typing import Optional

from sqlmodel import Field, SQLModel


class FacultyBaseModel(SQLModel):
    faculty_code: str = Field(unique=True, max_length=20)
    status: str = Field(default="active", max_length=20)
    archived_at: Optional[str] = None


class FacultyModel(FacultyBaseModel, table=True):
    __tablename__ = "faculties"
    faculty_id: Optional[int] = Field(default=None, primary_key=True)


class FacultyTranslationBaseModel(SQLModel):
    faculty_id: int = Field(foreign_key="faculties.faculty_id")
    language_code: str = Field(max_length=10)
    name: str = Field(max_length=255)
    description: Optional[str] = None


class FacultyTranslationModel(FacultyTranslationBaseModel, table=True):
    __tablename__ = "faculty_translations"
    faculty_id: int = Field(foreign_key="faculties.faculty_id", primary_key=True)
    language_code: str = Field(primary_key=True, max_length=10)
