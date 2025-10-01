#!/usr/bin/env python3
"""
Database Schema Update Script: Add Event Capacity Fields

This script adds the capacity management fields to existing events table:
- max_capacity: Optional[int] (null = unlimited)
- registration_count: int (default 0)

Uses SQLAlchemy to add columns safely to existing database.
"""

from unisphere.models import get_session, init_db
import asyncio
import sys
from pathlib import Path

from sqlalchemy import text

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


async def add_capacity_columns():
    """Add capacity management columns to events table"""
    print("🔧 Adding capacity management columns to events table...")

    # Initialize database
    await init_db()

    async for session in get_session():
        try:
            # Check if columns already exist
            check_max_capacity = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'events' AND column_name = 'max_capacity'
            """)

            check_registration_count = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'events' AND column_name = 'registration_count'
            """)

            max_cap_exists = await session.exec(check_max_capacity)
            reg_count_exists = await session.exec(check_registration_count)

            # Add max_capacity column if not exists
            if not max_cap_exists.first():
                print("➕ Adding max_capacity column...")
                add_max_capacity = text("""
                    ALTER TABLE events 
                    ADD COLUMN max_capacity INTEGER NULL DEFAULT NULL
                """)
                await session.exec(add_max_capacity)
                print("✅ max_capacity column added")
            else:
                print("ℹ️  max_capacity column already exists")

            # Add registration_count column if not exists
            if not reg_count_exists.first():
                print("➕ Adding registration_count column...")
                add_registration_count = text("""
                    ALTER TABLE events 
                    ADD COLUMN registration_count INTEGER NOT NULL DEFAULT 0
                """)
                await session.exec(add_registration_count)
                print("✅ registration_count column added")
            else:
                print("ℹ️  registration_count column already exists")

            # Commit changes
            await session.commit()
            print("💾 Schema changes committed")

        except Exception as e:
            print(f"❌ Schema update failed: {e}")
            await session.rollback()
            raise

        break  # Exit the async generator


async def populate_registration_counts():
    """Initialize registration_count based on actual registrations"""
    print("\n📊 Populating registration_count fields...")

    async for session in get_session():
        try:
            # Get all events using raw SQL first
            events_query = text("SELECT id, title FROM events")
            events_result = await session.exec(events_query)
            events_data = events_result.all()

            updated_count = 0

            for event_data in events_data:
                event_id, event_title = event_data

                # Count actual registrations
                count_query = text(f"""
                    SELECT COUNT(*) as count 
                    FROM event_registrations 
                    WHERE event_id = {event_id}
                """)
                count_result = await session.exec(count_query)
                actual_count = count_result.first()[0]

                # Update registration_count
                update_query = text(f"""
                    UPDATE events 
                    SET registration_count = {actual_count} 
                    WHERE id = {event_id}
                """)
                await session.exec(update_query)

                updated_count += 1
                print(f"📈 Event '{event_title}' (ID: {event_id}): "
                      f"Set registration_count to {actual_count}")

            # Commit all changes
            await session.commit()

            print("\n✅ Population completed successfully!")
            print(f"📈 Updated {updated_count} events")

        except Exception as e:
            print(f"❌ Population failed: {e}")
            await session.rollback()
            raise

        break  # Exit the async generator


async def verify_schema():
    """Verify that the schema was updated correctly"""
    print("\n🔍 Verifying schema updates...")

    async for session in get_session():
        try:
            # Check columns exist
            columns_query = text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'events' 
                AND column_name IN ('max_capacity', 'registration_count')
                ORDER BY column_name
            """)

            columns_result = await session.exec(columns_query)
            columns = columns_result.all()

            if len(columns) == 2:
                print("✅ Schema verification successful!")
                for col_name, data_type, nullable, default in columns:
                    print(
                        f"  • {col_name}: {data_type}, nullable={nullable}, default={default}")
            else:
                print(
                    f"❌ Schema verification failed. Found {len(columns)} columns, expected 2")

            # Check sample data
            sample_query = text("""
                SELECT id, title, max_capacity, registration_count 
                FROM events 
                LIMIT 3
            """)
            sample_result = await session.exec(sample_query)
            sample_data = sample_result.all()

            if sample_data:
                print("\n📋 Sample event data:")
                for event_id, title, max_cap, reg_count in sample_data:
                    cap_display = max_cap if max_cap is not None else "unlimited"
                    print(
                        f"  • {title}: {reg_count} registered, capacity: {cap_display}")

        except Exception as e:
            print(f"❌ Verification failed: {e}")
            raise

        break  # Exit the async generator


async def main():
    """Main schema update function"""
    print("🎯 Event Capacity Schema Update")
    print("=" * 50)

    try:
        # Step 1: Add columns
        await add_capacity_columns()

        # Step 2: Populate data
        await populate_registration_counts()

        # Step 3: Verify
        await verify_schema()

        print("\n🎉 Schema update completed successfully!")
        print("📝 Next steps:")
        print("  1. Test API endpoints with new fields")
        print("  2. Run the migration script to verify consistency")
        print("  3. Deploy updated application")

    except Exception as e:
        print(f"\n❌ Schema update failed: {e}")
        print("🔄 Database should be in a consistent state (rollback applied)")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
