from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class BranchBaseModel(SQLModel):
    faculty_id: int = Field(foreign_key="faculties.faculty_id")
    branch_code: str = Field(max_length=20, unique=True)
    status: str = Field(default="active", max_length=20)
    archived_at: Optional[datetime] = None


class BranchModel(BranchBaseModel, table=True):
    __tablename__ = "branchs"
    branch_id: Optional[int] = Field(default=None, primary_key=True)


class BranchTranslationBaseModel(SQLModel):
    branch_id: int = Field(foreign_key="branchs.branch_id")
    language_code: str = Field(max_length=10)
    name: str = Field(max_length=255)
    description: Optional[str] = None


class BranchTranslationModel(BranchTranslationBaseModel, table=True):
    __tablename__ = "branch_translations"
    branch_id: int = Field(foreign_key="branchs.branch_id", primary_key=True)
    language_code: str = Field(primary_key=True, max_length=10)
