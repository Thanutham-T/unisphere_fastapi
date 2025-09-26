from datetime import datetime
from typing import Optional

from pydantic import BaseModel, config


# Greeting schema
class GreetingBase(BaseModel):
    message: str
    language: str = "en"
    recipient_name: Optional[str] = None


class GreetingCreate(GreetingBase):
    pass


class GreetingUpdate(BaseModel):
    message: Optional[str] = None
    language: Optional[str] = None
    recipient_name: Optional[str] = None


class Greeting(GreetingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = config.ConfigDict(from_attributes=True)
