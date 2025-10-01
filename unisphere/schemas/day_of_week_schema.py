from pydantic import BaseModel, ConfigDict


class DayOfWeekBaseSchema(BaseModel):
    day_code: str


class DayOfWeekCreateSchema(DayOfWeekBaseSchema):
    pass


class DayOfWeekUpdateSchema(BaseModel):
    day_code: str


class DayOfWeekSchema(DayOfWeekBaseSchema):
    day_id: int

    model_config = ConfigDict(from_attributes=True)
