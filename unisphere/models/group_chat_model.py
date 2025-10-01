from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Text
from sqlmodel import Field, Relationship, SQLModel


class StudyGroupBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, sa_type=Text)
    category: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)


class StudyGroup(StudyGroupBase, table=True):
    __tablename__ = "study_groups"  # type: ignore[assignment]

    id: int | None = Field(default=None, primary_key=True)
    created_by: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    members: List["StudyGroupMember"] = Relationship(back_populates="group")
    messages: List["StudyGroupMessage"] = Relationship(back_populates="group")


class StudyGroupMemberBase(SQLModel):
    role: Optional[str] = Field(default=None, max_length=50)


class StudyGroupMember(StudyGroupMemberBase, table=True):
    __tablename__ = "study_group_members"  # type: ignore[assignment]

    id: int | None = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="study_groups.id")
    user_id: int = Field(foreign_key="users.id")
    joined_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    group: Optional[StudyGroup] = Relationship(back_populates="members")


class StudyGroupMessageBase(SQLModel):
    message: str = Field(sa_type=Text)
    message_type: Optional[str] = Field(default=None, max_length=50)


class StudyGroupMessage(StudyGroupMessageBase, table=True):
    __tablename__ = "study_group_messages"  # type: ignore[assignment]

    id: int | None = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="study_groups.id")
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    group: Optional[StudyGroup] = Relationship(back_populates="messages")
