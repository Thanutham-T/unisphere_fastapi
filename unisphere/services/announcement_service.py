from datetime import datetime
from typing import List, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models.announcement_model import Announcement
from unisphere.models.user_model import User
from unisphere.schemas.announcement_schema import AnnouncementCreate, AnnouncementUpdate


class AnnouncementService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_announcements(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[Announcement]:
        """Get all announcements with filters"""
        query = select(Announcement).order_by(Announcement.date.desc())

        if category:
            query = query.where(Announcement.category == category)
        if priority:
            query = query.where(Announcement.priority == priority)

        query = query.offset(skip).limit(limit)
        result = await self.session.exec(query)
        return list(result.all())

    async def get_announcement_by_id(self, announcement_id: int) -> Optional[Announcement]:
        """Get announcement by ID"""
        statement = select(Announcement).where(
            Announcement.id == announcement_id)
        result = await self.session.exec(statement)
        return result.first()

    async def create_announcement(self, announcement_data: AnnouncementCreate, created_by: int) -> Announcement:
        """Create a new announcement"""
        announcement = Announcement(
            **announcement_data.model_dump(), created_by=created_by)
        self.session.add(announcement)
        await self.session.commit()
        await self.session.refresh(announcement)
        return announcement

    async def update_announcement(self, announcement_id: int, announcement_data: AnnouncementUpdate) -> Optional[Announcement]:
        """Update an existing announcement"""
        statement = select(Announcement).where(
            Announcement.id == announcement_id)
        result = await self.session.exec(statement)
        announcement = result.first()

        if not announcement:
            return None

        update_data = announcement_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(announcement, field, value)

        announcement.updated_at = datetime.now()
        self.session.add(announcement)
        await self.session.commit()
        await self.session.refresh(announcement)
        return announcement

    async def delete_announcement(self, announcement_id: int) -> bool:
        """Delete an announcement"""
        statement = select(Announcement).where(
            Announcement.id == announcement_id)
        result = await self.session.exec(statement)
        announcement = result.first()

        if not announcement:
            return False

        await self.session.delete(announcement)
        await self.session.commit()
        return True

    async def get_announcements_by_category(self, category: str, limit: int = 50) -> List[Announcement]:
        """Get announcements by specific category"""
        statement = (
            select(Announcement)
            .where(Announcement.category == category)
            .order_by(Announcement.date.desc())
            .limit(limit)
        )
        result = await self.session.exec(statement)
        return list(result.all())

    async def get_high_priority_announcements(self, limit: int = 10) -> List[Announcement]:
        """Get high priority announcements"""
        statement = (
            select(Announcement)
            .where(Announcement.priority == "high")
            .order_by(Announcement.date.desc())
            .limit(limit)
        )
        result = await self.session.exec(statement)
        return list(result.all())

    async def get_announcement_with_creator(self, announcement_id: int) -> Optional[tuple[Announcement, User]]:
        """Get announcement with creator information"""
        statement = (
            select(Announcement, User)
            .join(User, Announcement.created_by == User.id)
            .where(Announcement.id == announcement_id)
        )
        result = await self.session.exec(statement)
        return result.first()

    async def get_announcements_with_creators(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[tuple[Announcement, User]]:
        """Get announcements with creator information"""
        query = (
            select(Announcement, User)
            .join(User, Announcement.created_by == User.id)
            .order_by(Announcement.date.desc())
        )

        if category:
            query = query.where(Announcement.category == category)
        if priority:
            query = query.where(Announcement.priority == priority)

        query = query.offset(skip).limit(limit)
        result = await self.session.exec(query)
        return list(result.all())
