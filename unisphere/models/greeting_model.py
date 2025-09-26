from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


# Greeting schema
class GreetingBase(SQLModel):
    message: str = Field(min_length=1, max_length=255)
    language: str = Field(default="en")  # e.g., "en", "th", "jp"
    recipient_name: Optional[str] = Field(default=None)


class Greeting(GreetingBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
