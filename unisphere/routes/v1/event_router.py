from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models import get_session
from unisphere.routes.v1.auth_router import get_current_user
from unisphere.schemas.event_schema import (
    EventCreate,
    EventRegistration,
    EventRegistrationCreate,
    EventResponse,
    EventUpdate,
)
from unisphere.schemas.user_schema import User as SchemaUser
from unisphere.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["events"])


def get_event_service(session: AsyncSession = Depends(get_session)) -> EventService:
    return EventService(session)


@router.get("", response_model=List[EventResponse])
async def get_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    event_status: Optional[str] = None,
    current_user: SchemaUser = Depends(get_current_user),
    event_service: EventService = Depends(get_event_service)
):
    """Get all events (public access for logged in users)"""
    events = await event_service.get_events(skip, limit, category, event_status)

    # Add registration info for each event
    result = []
    for event in events:
        if event.id is None:
            continue
        is_registered = await event_service.is_user_registered(event.id, current_user.id)
        is_full = await event_service.is_event_full(event.id)

        event_response = EventResponse(
            **event.model_dump(),
            is_registered=is_registered,
            is_full=is_full
        )
        result.append(event_response)

    return result


@router.post("", response_model=EventResponse)
async def create_event(
    event: EventCreate,
    current_user: SchemaUser = Depends(get_current_user),
    event_service: EventService = Depends(get_event_service)
):
    """Create a new event (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create events"
        )

    created_event = await event_service.create_event(event, current_user.id)

    return EventResponse(
        **created_event.model_dump(),
        is_registered=False,
        is_full=False
    )


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    current_user: SchemaUser = Depends(get_current_user),
    event_service: EventService = Depends(get_event_service)
):
    """Get event details"""
    event = await event_service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    is_registered = await event_service.is_user_registered(event_id, current_user.id)
    is_full = await event_service.is_event_full(event_id)

    return EventResponse(
        **event.model_dump(),
        is_registered=is_registered,
        is_full=is_full
    )


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    current_user: SchemaUser = Depends(get_current_user),
    event_service: EventService = Depends(get_event_service)
):
    """Update an event (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update events"
        )

    updated_event = await event_service.update_event(event_id, event_update)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    is_full = await event_service.is_event_full(event_id)

    return EventResponse(
        **updated_event.model_dump(),
        is_registered=False,
        is_full=is_full
    )


@router.post("/{event_id}/register", response_model=EventRegistration)
async def register_for_event(
    event_id: int,
    registration: EventRegistrationCreate,
    current_user: SchemaUser = Depends(get_current_user),
    event_service: EventService = Depends(get_event_service)
):
    """Register for an event"""
    # Check if event exists
    event = await event_service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    # Sync registration count to ensure accuracy
    await event_service.sync_registration_count(event_id)

    # Re-fetch event after sync
    event = await event_service.get_event_by_id(event_id)

    # Check if event is full
    if await event_service.is_event_full(event_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is full"
        )

    registration_result = await event_service.register_user_for_event(
        event_id, current_user.id, registration.notes
    )

    if not registration_result:
        # Could be already registered or became full during registration
        if await event_service.is_user_registered(event_id, current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already registered for this event"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event is full"
            )

    return EventRegistration.model_validate(registration_result)


@router.delete("/{event_id}/register")
async def unregister_from_event(
    event_id: int,
    current_user: SchemaUser = Depends(get_current_user),
    event_service: EventService = Depends(get_event_service)
):
    """Unregister from an event"""
    success = await event_service.unregister_user_from_event(event_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not registered for this event"
        )

    return {"message": "Unregistered successfully"}


@router.delete("/{event_id}")
async def delete_event(
    event_id: int,
    current_user: SchemaUser = Depends(get_current_user),
    event_service: EventService = Depends(get_event_service)
):
    """Delete an event (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete events"
        )

    success = await event_service.delete_event(event_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return {"message": "Event deleted successfully"}


@router.post("/{event_id}/sync-registration-count")
async def sync_event_registration_count(
    event_id: int,
    current_user: SchemaUser = Depends(get_current_user),
    event_service: EventService = Depends(get_event_service)
):
    """Sync registration count for an event (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can sync registration counts"
        )

    success = await event_service.sync_registration_count(event_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    # Return updated event
    event = await event_service.get_event_by_id(event_id)
    is_full = await event_service.is_event_full(event_id)

    return {
        "message": "Registration count synced successfully",
        "event": {
            "id": event.id,
            "title": event.title,
            "max_capacity": event.max_capacity,
            "registration_count": event.registration_count,
            "is_full": is_full,
            "available_spots": await event_service.get_available_spots(event_id)
        }
    }


@router.post("/sync-all-registration-counts")
async def sync_all_registration_counts(
    current_user: SchemaUser = Depends(get_current_user),
    event_service: EventService = Depends(get_event_service)
):
    """Sync registration counts for all events (Admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can sync registration counts"
        )

    synced_count = await event_service.sync_all_registration_counts()

    return {
        "message": f"Synced registration counts for {synced_count} events",
        "synced_events": synced_count
    }
