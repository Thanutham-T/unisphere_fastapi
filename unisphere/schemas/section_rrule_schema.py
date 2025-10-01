from pydantic import BaseModel, ConfigDict


class SectionRRuleBaseSchema(BaseModel):
    section_id: int
    rrule: str


class SectionRRuleCreateSchema(SectionRRuleBaseSchema):
    pass


class SectionRRuleUpdateSchema(BaseModel):
    rrule: str


class SectionRRuleSchema(SectionRRuleBaseSchema):
    rrule_id: int

    model_config = ConfigDict(from_attributes=True)
