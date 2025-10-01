from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserNotificationSettingBaseSchema(BaseModel):
    user_id: int
    section_id: int
    notify_before_minutes: int = 15
    channels: str = "app"
    status: str = "active"


class UserNotificationSettingCreateSchema(UserNotificationSettingBaseSchema):
    pass


class UserNotificationSettingUpdateSchema(BaseModel):
    notify_before_minutes: Optional[int] = None
    channels: Optional[str] = None
    status: Optional[str] = None
    updated_at: Optional[datetime] = None


class UserNotificationSettingSchema(UserNotificationSettingBaseSchema):
    setting_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
