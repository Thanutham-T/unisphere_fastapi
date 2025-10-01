from typing import Optional

from pydantic import BaseModel, ConfigDict


class CourseTranslationBaseSchema(BaseModel):
    course_id: int
    language_code: str
    subject_name: str
    description: Optional[str] = None


class CourseTranslationCreateSchema(CourseTranslationBaseSchema):
    pass


class CourseTranslationUpdateSchema(BaseModel):
    subject_name: Optional[str] = None
    description: Optional[str] = None


class CourseTranslationSchema(CourseTranslationBaseSchema):
    model_config = ConfigDict(from_attributes=True)
