from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserEnrollBaseSchema(BaseModel):
    user_id: int
    section_id: int


class UserEnrollCreateSchema(UserEnrollBaseSchema):
    pass


class UserEnrollUpdateSchema(BaseModel):
    pass


class UserEnrollSchema(UserEnrollBaseSchema):
    enroll_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
