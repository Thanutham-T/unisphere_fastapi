from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class UserNotificationSettingBaseModel(SQLModel):
    user_id: int = Field(foreign_key="users.id")
    section_id: int = Field(foreign_key="sections.section_id")
    notify_before_minutes: int = Field(default=15)
    status: str = Field(default="active", max_length=20)
    created_at: datetime = Field(
        default_factory=datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None


class UserNotificationSettingModel(UserNotificationSettingBaseModel, table=True):
    __tablename__ = "user_notification_settings"
    setting_id: Optional[int] = Field(default=None, primary_key=True)


class UserNotificationChannelBaseModel(SQLModel):
    setting_id: int = Field(
        foreign_key="user_notification_settings.setting_id")
    channel: str = Field(max_length=20)


class UserNotificationChannelModel(UserNotificationChannelBaseModel, table=True):
    __tablename__ = "user_notification_channels"
    setting_id: int = Field(primary_key=True)
    channel: str = Field(primary_key=True, max_length=20)
