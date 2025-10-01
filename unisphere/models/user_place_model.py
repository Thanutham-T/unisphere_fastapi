from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class UserPlace(SQLModel, table=True):
    """A place saved by a specific user into their collection (คลัง)."""

    __tablename__ = "user_places"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Owner
    user_id: int = Field(foreign_key="users.id", index=True)

    # Place core
    name: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    latitude: float
    longitude: float
    category: str = Field(max_length=100)
    image_url: Optional[str] = Field(default=None, max_length=500)

    # Extra metadata from frontend (tags, address, amenity, etc.)
    additional_info: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=Column(JSON)
    )

    # Flags and timestamps
    is_favorite: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
