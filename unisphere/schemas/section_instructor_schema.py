from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SectionInstructorBaseSchema(BaseModel):
    user_id: int
    section_id: int

class SectionInstructorCreateSchema(SectionInstructorBaseSchema):
    pass


class SectionInstructorUpdateSchema(BaseModel):
    pass


class SectionInstructorSchema(SectionInstructorBaseSchema):
    model_config = ConfigDict(from_attributes=True)
