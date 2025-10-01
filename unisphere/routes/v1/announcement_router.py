from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models import get_session
from unisphere.routes.v1.auth_router import get_current_user
from unisphere.schemas.announcement_schema import (
    AnnouncementCreate,
    AnnouncementResponse,
    AnnouncementUpdate,
)
from unisphere.schemas.user_schema import User as SchemaUser
from unisphere.services.announcement_service import AnnouncementService

router = APIRouter(prefix="/announcements", tags=["announcements"])


def get_announcement_service(session: AsyncSession = Depends(get_session)) -> AnnouncementService:
    return AnnouncementService(session)


@router.get("", response_model=List[AnnouncementResponse])
async def get_announcements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    priority: Optional[str] = None,
    current_user: SchemaUser = Depends(get_current_user),
    announcement_service: AnnouncementService = Depends(
        get_announcement_service)
):
    """Get all announcements (public access for logged in users)"""
    announcements_with_creators = await announcement_service.get_announcements_with_creators(
        skip, limit, category, priority
    )

    result = []
    for announcement, creator in announcements_with_creators:
        creator_name = f"{creator.first_name} {creator.last_name}" if creator else None
        announcement_response = AnnouncementResponse(
            **announcement.model_dump(),
            creator_name=creator_name
        )
        result.append(announcement_response)

    return result


@router.post("", response_model=AnnouncementResponse)
async def create_announcement(
    announcement: AnnouncementCreate,
    current_user: SchemaUser = Depends(get_current_user),
    announcement_service: AnnouncementService = Depends(
        get_announcement_service)
):
    """Create a new announcement (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create announcements"
        )

    created_announcement = await announcement_service.create_announcement(announcement, current_user.id)

    return AnnouncementResponse(
        **created_announcement.model_dump(),
        creator_name=f"{current_user.first_name} {current_user.last_name}"
    )


@router.get("/{announcement_id}", response_model=AnnouncementResponse)
async def get_announcement(
    announcement_id: int,
    current_user: SchemaUser = Depends(get_current_user),
    announcement_service: AnnouncementService = Depends(
        get_announcement_service)
):
    """Get announcement details"""
    announcement_with_creator = await announcement_service.get_announcement_with_creator(announcement_id)
    if not announcement_with_creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )

    announcement, creator = announcement_with_creator
    creator_name = f"{creator.first_name} {creator.last_name}" if creator else None

    return AnnouncementResponse(
        **announcement.model_dump(),
        creator_name=creator_name
    )


@router.put("/{announcement_id}", response_model=AnnouncementResponse)
async def update_announcement(
    announcement_id: int,
    announcement_update: AnnouncementUpdate,
    current_user: SchemaUser = Depends(get_current_user),
    announcement_service: AnnouncementService = Depends(
        get_announcement_service)
):
    """Update an announcement (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update announcements"
        )

    updated_announcement = await announcement_service.update_announcement(announcement_id, announcement_update)
    if not updated_announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )

    return AnnouncementResponse(
        **updated_announcement.model_dump(),
        creator_name=f"{current_user.first_name} {current_user.last_name}"
    )


@router.delete("/{announcement_id}")
async def delete_announcement(
    announcement_id: int,
    current_user: SchemaUser = Depends(get_current_user),
    announcement_service: AnnouncementService = Depends(
        get_announcement_service)
):
    """Delete an announcement (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete announcements"
        )

    success = await announcement_service.delete_announcement(announcement_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )

    return {"message": "Announcement deleted successfully"}


@router.get("/category/{category}", response_model=List[AnnouncementResponse])
async def get_announcements_by_category(
    category: str,
    limit: int = Query(50, ge=1, le=100),
    current_user: SchemaUser = Depends(get_current_user),
    announcement_service: AnnouncementService = Depends(
        get_announcement_service)
):
    """Get announcements by category"""
    announcements = await announcement_service.get_announcements_by_category(category, limit)

    result = []
    for announcement in announcements:
        # Get creator info for each announcement
        announcement_with_creator = await announcement_service.get_announcement_with_creator(announcement.id)
        creator_name = None
        if announcement_with_creator:
            _, creator = announcement_with_creator
            creator_name = f"{creator.first_name} {creator.last_name}" if creator else None

        announcement_response = AnnouncementResponse(
            **announcement.model_dump(),
            creator_name=creator_name
        )
        result.append(announcement_response)

    return result


@router.get("/priority/high", response_model=List[AnnouncementResponse])
async def get_high_priority_announcements(
    limit: int = Query(10, ge=1, le=50),
    current_user: SchemaUser = Depends(get_current_user),
    announcement_service: AnnouncementService = Depends(
        get_announcement_service)
):
    """Get high priority announcements"""
    announcements = await announcement_service.get_high_priority_announcements(limit)

    result = []
    for announcement in announcements:
        # Get creator info for each announcement
        announcement_with_creator = await announcement_service.get_announcement_with_creator(announcement.id)
        creator_name = None
        if announcement_with_creator:
            _, creator = announcement_with_creator
            creator_name = f"{creator.first_name} {creator.last_name}" if creator else None

        announcement_response = AnnouncementResponse(
            **announcement.model_dump(),
            creator_name=creator_name
        )
        result.append(announcement_response)

    return result
