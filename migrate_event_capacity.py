#!/usr/bin/env python3
"""
Database Migration Script: Initialize Event Capacity Management

This script updates existing events to include capacity management fields:
- Initializes registration_count based on actual registrations
- Sets max_capacity to NULL (unlimited) for existing events
- Ensures data consistency

Run this script after updating the Event model to include capacity fields.
"""

from unisphere.models.event_model import Event, EventRegistration
from unisphere.models import get_session, init_db
import asyncio
import sys
from pathlib import Path

from sqlmodel import select

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


async def migrate_event_capacity():
    """Initialize capacity management for existing events"""
    print("🚀 Starting Event Capacity Migration...")

    # Initialize database
    await init_db()

    async for session in get_session():
        try:
            # Get all events
            events_query = select(Event)
            events_result = await session.exec(events_query)
            events = events_result.all()

            updated_count = 0

            for event in events:
                if event.id is None:
                    continue

                # Count actual registrations
                registrations_query = select(EventRegistration).where(
                    EventRegistration.event_id == event.id
                )
                registrations_result = await session.exec(registrations_query)
                actual_count = len(registrations_result.all())

                # Update registration_count if different
                if event.registration_count != actual_count:
                    event.registration_count = actual_count
                    session.add(event)
                    updated_count += 1
                    print(f"📊 Event '{event.title}' (ID: {event.id}): "
                          f"Updated registration_count to {actual_count}")

            # Commit all changes
            await session.commit()

            print("✅ Migration completed successfully!")
            print(f"📈 Updated {updated_count} events")
            print(f"📋 Total events processed: {len(events)}")

            # Summary report
            print("\n📊 Event Capacity Summary:")
            for event in events:
                capacity_info = "unlimited" if event.max_capacity is None else str(
                    event.max_capacity)
                print(f"  • {event.title}: {event.registration_count} registered, "
                      f"capacity: {capacity_info}")

        except Exception as e:
            print(f"❌ Migration failed: {e}")
            await session.rollback()
            raise

        break  # Exit the async generator


async def verify_capacity_consistency():
    """Verify that registration_count matches actual registrations"""
    print("\n🔍 Verifying capacity consistency...")

    async for session in get_session():
        events_query = select(Event)
        events_result = await session.exec(events_query)
        events = events_result.all()

        inconsistent_events = []

        for event in events:
            if event.id is None:
                continue

            # Count actual registrations
            registrations_query = select(EventRegistration).where(
                EventRegistration.event_id == event.id
            )
            registrations_result = await session.exec(registrations_query)
            actual_count = len(registrations_result.all())

            if event.registration_count != actual_count:
                inconsistent_events.append({
                    'event': event,
                    'stored_count': event.registration_count,
                    'actual_count': actual_count
                })

        if inconsistent_events:
            print(f"⚠️  Found {len(inconsistent_events)} inconsistent events:")
            for item in inconsistent_events:
                event = item['event']
                print(f"  • {event.title} (ID: {event.id}): "
                      f"stored={item['stored_count']}, actual={item['actual_count']}")
        else:
            print("✅ All events have consistent registration counts!")

        break  # Exit the async generator


async def main():
    """Main migration function"""
    print("🎯 Event Capacity Management Migration")
    print("=" * 50)

    try:
        # Run migration
        await migrate_event_capacity()

        # Verify consistency
        await verify_capacity_consistency()

        print("\n🎉 Migration completed successfully!")
        print("📝 Next steps:")
        print("  1. Test the API endpoints with capacity management")
        print("  2. Verify frontend integration")
        print("  3. Monitor capacity validation in production")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
