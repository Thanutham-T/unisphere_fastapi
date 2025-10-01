from typing import Optional

from pydantic import BaseModel, ConfigDict


class BranchTranslationBaseSchema(BaseModel):
    branch_id: int
    language_code: str
    name: str
    description: Optional[str] = None


class BranchTranslationCreateSchema(BranchTranslationBaseSchema):
    pass


class BranchTranslationUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class BranchTranslationSchema(BranchTranslationBaseSchema):
    model_config = ConfigDict(from_attributes=True)
