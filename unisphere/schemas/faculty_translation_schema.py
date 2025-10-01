from typing import Optional

from pydantic import BaseModel, ConfigDict


class FacultyTranslationBaseSchema(BaseModel):
    faculty_id: int
    language_code: str
    name: str
    description: Optional[str] = None


class FacultyTranslationCreateSchema(FacultyTranslationBaseSchema):
    pass


class FacultyTranslationUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class FacultyTranslationSchema(FacultyTranslationBaseSchema):
    model_config = ConfigDict(from_attributes=True)
