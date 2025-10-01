from datetime import datetime
from typing import List, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models.event_model import Event, EventRegistration
from unisphere.schemas.event_schema import EventCreate, EventUpdate


class EventService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_events(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Event]:
        """Get all events with filters"""
        query = select(Event)

        if category:
            query = query.where(Event.category == category)
        if status:
            query = query.where(Event.status == status)

        query = query.offset(skip).limit(limit)
        result = await self.session.exec(query)
        return list(result.all())

    async def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """Get event by ID"""
        statement = select(Event).where(Event.id == event_id)
        result = await self.session.exec(statement)
        return result.first()

    async def create_event(self, event_data: EventCreate, created_by: int) -> Event:
        """Create a new event"""
        event = Event(**event_data.model_dump(), created_by=created_by)
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def update_event(self, event_id: int, event_data: EventUpdate) -> Optional[Event]:
        """Update an existing event"""
        statement = select(Event).where(Event.id == event_id)
        result = await self.session.exec(statement)
        event = result.first()

        if not event:
            return None

        update_data = event_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(event, field, value)

        event.updated_at = datetime.now()
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def delete_event(self, event_id: int) -> bool:
        """Delete an event and its registrations"""
        # First delete all registrations
        reg_statement = select(EventRegistration).where(
            EventRegistration.event_id == event_id)
        reg_result = await self.session.exec(reg_statement)
        registrations = reg_result.all()

        for registration in registrations:
            await self.session.delete(registration)

        # Then delete the event
        statement = select(Event).where(Event.id == event_id)
        result = await self.session.exec(statement)
        event = result.first()

        if not event:
            return False

        await self.session.delete(event)
        await self.session.commit()
        return True

    async def get_event_registration_count(self, event_id: int) -> int:
        """Get registration count for an event"""
        statement = select(EventRegistration).where(
            EventRegistration.event_id == event_id)
        result = await self.session.exec(statement)
        registrations = result.all()
        return len(registrations)

    async def is_user_registered(self, event_id: int, user_id: int) -> bool:
        """Check if user is registered for an event"""
        statement = select(EventRegistration).where(
            EventRegistration.event_id == event_id,
            EventRegistration.user_id == user_id
        )
        result = await self.session.exec(statement)
        registration = result.first()
        return registration is not None

    async def register_user_for_event(
        self,
        event_id: int,
        user_id: int,
        notes: Optional[str] = None
    ) -> Optional[EventRegistration]:
        """Register a user for an event"""
        # Get event to check capacity
        event = await self.get_event_by_id(event_id)
        if not event:
            return None

        # Check if already registered
        if await self.is_user_registered(event_id, user_id):
            return None

        # Check if event is full
        if event.max_capacity and event.registration_count >= event.max_capacity:
            return None

        registration = EventRegistration(
            event_id=event_id,
            user_id=user_id,
            notes=notes
        )

        # Update registration count
        event.registration_count += 1

        self.session.add(registration)
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(registration)
        return registration

    async def unregister_user_from_event(self, event_id: int, user_id: int) -> bool:
        """Unregister a user from an event"""
        # Get event to update count
        event = await self.get_event_by_id(event_id)
        if not event:
            return False

        statement = select(EventRegistration).where(
            EventRegistration.event_id == event_id,
            EventRegistration.user_id == user_id
        )
        result = await self.session.exec(statement)
        registration = result.first()

        if not registration:
            return False

        # Update registration count
        event.registration_count = max(0, event.registration_count - 1)

        await self.session.delete(registration)
        self.session.add(event)
        await self.session.commit()
        return True

    async def is_event_full(self, event_id: int) -> bool:
        """Check if event has reached maximum capacity"""
        event = await self.get_event_by_id(event_id)
        if not event or not event.max_capacity:
            return False
        return event.registration_count >= event.max_capacity

    async def get_available_spots(self, event_id: int) -> Optional[int]:
        """Get number of available spots for an event"""
        event = await self.get_event_by_id(event_id)
        if not event:
            return None
        if not event.max_capacity:
            return None  # Unlimited capacity
        return max(0, event.max_capacity - event.registration_count)

    async def sync_registration_count(self, event_id: int) -> bool:
        """Sync registration_count field with actual registrations"""
        event = await self.get_event_by_id(event_id)
        if not event:
            return False

        # Count actual registrations
        statement = select(EventRegistration).where(
            EventRegistration.event_id == event_id)
        result = await self.session.exec(statement)
        actual_count = len(result.all())

        # Update if different
        if event.registration_count != actual_count:
            event.registration_count = actual_count
            self.session.add(event)
            await self.session.commit()
            await self.session.refresh(event)

        return True

    async def sync_all_registration_counts(self) -> int:
        """Sync registration_count for all events"""
        events = await self.get_events(skip=0, limit=1000)  # Get all events
        synced_count = 0

        for event in events:
            if event.id:
                await self.sync_registration_count(event.id)
                synced_count += 1

        return synced_count
