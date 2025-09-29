from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class UserPlaceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    category: str
    image_url: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None


class UserPlaceUpdate(BaseModel):
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    is_favorite: Optional[bool] = None
    additional_info: Optional[Dict[str, Any]] = None


class UserPlaceResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    category: str
    image_url: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None
    is_favorite: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserPlaceListResponse(BaseModel):
    places: List[UserPlaceResponse]
    total: int
    limit: int
    offset: int
