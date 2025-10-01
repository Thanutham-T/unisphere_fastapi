from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BranchBaseSchema(BaseModel):
    faculty_id: int
    branch_code: str
    status: str = "active"


class BranchCreateSchema(BranchBaseSchema):
    pass


class BranchUpdateSchema(BaseModel):
    faculty_id: Optional[int] = None
    branch_code: Optional[str] = None
    status: Optional[str] = None
    archived_at: Optional[datetime] = None


class BranchSchema(BranchBaseSchema):
    branch_id: int
    archived_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
