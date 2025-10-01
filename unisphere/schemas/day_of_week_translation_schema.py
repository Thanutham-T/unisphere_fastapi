from pydantic import BaseModel, ConfigDict


class DayTranslationBaseSchema(BaseModel):
    day_id: int
    language_code: str
    day_name: str


class DayTranslationCreateSchema(DayTranslationBaseSchema):
    pass


class DayTranslationUpdateSchema(BaseModel):
    day_name: str


class DayTranslationSchema(DayTranslationBaseSchema):
    model_config = ConfigDict(from_attributes=True)
