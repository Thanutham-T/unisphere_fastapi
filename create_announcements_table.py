#!/usr/bin/env python3
"""
Database Schema Update Script: Add Announcements Table

This script creates the announcements table with the following structure:
- id: primary key
- title: varchar
- content: text
- category: varchar (academic, cultural, general, etc.)
- priority: varchar (low, medium, high)
- date: timestamp
- created_by: integer (FK to users.id)
- created_at: timestamp
- updated_at: timestamp

Uses SQLAlchemy to create table safely.
"""

from unisphere.models import get_session, init_db
import asyncio
import sys
from pathlib import Path

from sqlalchemy import text

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


async def create_announcements_table():
    """Create announcements table if not exists"""
    print("🔧 Creating announcements table...")

    # Initialize database
    await init_db()

    async for session in get_session():
        try:
            # Check if table already exists
            check_table = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'announcements'
            """)

            table_exists = await session.exec(check_table)

            if table_exists.first():
                print("ℹ️  announcements table already exists")
            else:
                print("➕ Creating announcements table...")
                create_table = text("""
                    CREATE TABLE announcements (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        content TEXT NOT NULL,
                        category VARCHAR(100) NOT NULL,
                        priority VARCHAR(50) NOT NULL DEFAULT 'medium',
                        date TIMESTAMP NOT NULL,
                        created_by INTEGER NOT NULL REFERENCES users(id),
                        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMP NOT NULL DEFAULT NOW()
                    )
                """)
                await session.exec(create_table)
                print("✅ announcements table created")

            # Create indexes for better performance
            print("🔍 Creating indexes...")

            # Index for category filtering
            create_category_index = text("""
                CREATE INDEX IF NOT EXISTS idx_announcements_category 
                ON announcements(category)
            """)
            await session.exec(create_category_index)

            # Index for priority filtering
            create_priority_index = text("""
                CREATE INDEX IF NOT EXISTS idx_announcements_priority 
                ON announcements(priority)
            """)
            await session.exec(create_priority_index)

            # Index for date ordering
            create_date_index = text("""
                CREATE INDEX IF NOT EXISTS idx_announcements_date 
                ON announcements(date DESC)
            """)
            await session.exec(create_date_index)

            # Index for created_by (foreign key)
            create_creator_index = text("""
                CREATE INDEX IF NOT EXISTS idx_announcements_created_by 
                ON announcements(created_by)
            """)
            await session.exec(create_creator_index)

            print("✅ Indexes created")

            # Commit changes
            await session.commit()
            print("💾 Schema changes committed")

        except Exception as e:
            print(f"❌ Schema creation failed: {e}")
            await session.rollback()
            raise

        break  # Exit the async generator


async def create_sample_announcements():
    """Create sample announcements for testing"""
    print("\n📋 Creating sample announcements...")

    async for session in get_session():
        try:
            # Check if we already have announcements
            count_query = text("SELECT COUNT(*) FROM announcements")
            count_result = await session.exec(count_query)
            existing_count = count_result.first()[0]

            if existing_count > 0:
                print(
                    f"ℹ️  Found {existing_count} existing announcements, skipping sample creation")
                break

            # Get an admin user (assuming user id 1 exists)
            admin_check = text(
                "SELECT id FROM users WHERE role = 'admin' LIMIT 1")
            admin_result = await session.exec(admin_check)
            admin_user = admin_result.first()

            if not admin_user:
                print("⚠️  No admin user found, skipping sample announcements")
                break

            admin_id = admin_user[0]

            # Sample announcements
            sample_announcements = [
                {
                    "title": "🎓 ประกาศรับสมัครทุนการศึกษา ประจำปี 2025",
                    "content": "มหาวิทยาลัยเปิดรับสมัครทุนการศึกษาสำหรับนักศึกษาที่มีผลการเรียนดีเยี่ยม สามารถสมัครได้ตั้งแต่วันที่ 1-31 มกราคม 2025 ผ่านระบบออนไลน์ของมหาวิทยาลัย",
                    "category": "academic",
                    "priority": "high"
                },
                {
                    "title": "🎭 งานเทศกาลวัฒนธรรมนานาชาติ",
                    "content": "ขอเชิญชวนนักศึกษาร่วมงานเทศกาลวัฒนธรรมนานาชาติ ในวันที่ 15 กุมภาพันธ์ 2025 ณ อาคารกิจกรรมนักศึกษา จะมีการแสดงทางวัฒนธรรมจากหลากหลายประเทศ",
                    "category": "cultural",
                    "priority": "medium"
                },
                {
                    "title": "📚 ปิดปรับปรุงห้องสมุดกลาง",
                    "content": "ห้องสมุดกลางจะปิดให้บริการชั่วคราว เพื่อปรับปรุงระบบและเพิ่มพื้นที่การเรียนรู้ ในระหว่างวันที่ 20-25 มกราคม 2025 ขออภัยในความไม่สะดวก",
                    "category": "general",
                    "priority": "high"
                },
                {
                    "title": "🏆 การแข่งขันกีฬาสีภายใน",
                    "content": "เปิดรับสมัครนักกีฬาเข้าร่วมการแข่งขันกีฬาสีประจำปี ในวันที่ 10-12 มีนาคม 2025 สามารถสมัครได้ที่งานกิจการนักศึกษา",
                    "category": "general",
                    "priority": "medium"
                },
                {
                    "title": "⚠️ ประกาศเปลี่ยนแปลงตารางสอบ",
                    "content": "มีการเปลี่ยนแปลงตารางสอบกลางภาค สำหรับรายวิชา CS101 และ CS102 ขอให้นักศึกษาตรวจสอบตารางสอบใหม่ในระบบลงทะเบียน",
                    "category": "academic",
                    "priority": "high"
                }
            ]

            # Insert sample announcements
            for i, announcement in enumerate(sample_announcements, 1):
                insert_query = text(f"""
                    INSERT INTO announcements (title, content, category, priority, date, created_by, created_at, updated_at)
                    VALUES (
                        '{announcement['title']}',
                        '{announcement['content']}',
                        '{announcement['category']}',
                        '{announcement['priority']}',
                        NOW() + INTERVAL '{i} day',
                        {admin_id},
                        NOW(),
                        NOW()
                    )
                """)
                await session.exec(insert_query)
                print(f"📝 Created: {announcement['title']}")

            # Commit all changes
            await session.commit()

            print("✅ Sample announcements created successfully!")
            print(f"📈 Created {len(sample_announcements)} announcements")

        except Exception as e:
            print(f"❌ Sample creation failed: {e}")
            await session.rollback()
            raise

        break  # Exit the async generator


async def verify_announcements_schema():
    """Verify that the announcements schema was created correctly"""
    print("\n🔍 Verifying announcements schema...")

    async for session in get_session():
        try:
            # Check table structure
            structure_query = text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'announcements'
                ORDER BY ordinal_position
            """)

            structure_result = await session.exec(structure_query)
            columns = structure_result.all()

            print("✅ Announcements table structure:")
            for col_name, data_type, nullable, default in columns:
                print(
                    f"  • {col_name}: {data_type}, nullable={nullable}, default={default}")

            # Check indexes
            indexes_query = text("""
                SELECT indexname, indexdef
                FROM pg_indexes 
                WHERE tablename = 'announcements'
                ORDER BY indexname
            """)

            indexes_result = await session.exec(indexes_query)
            indexes = indexes_result.all()

            print("\n🔍 Indexes:")
            for index_name, index_def in indexes:
                print(f"  • {index_name}")

            # Check sample data
            sample_query = text("""
                SELECT id, title, category, priority 
                FROM announcements 
                ORDER BY date DESC
                LIMIT 3
            """)
            sample_result = await session.exec(sample_query)
            sample_data = sample_result.all()

            if sample_data:
                print("\n📋 Sample announcements:")
                for ann_id, title, category, priority in sample_data:
                    print(f"  • {title} [{category}] - {priority} priority")

        except Exception as e:
            print(f"❌ Verification failed: {e}")
            raise

        break  # Exit the async generator


async def main():
    """Main schema creation function"""
    print("🎯 Announcements Schema Creation")
    print("=" * 50)

    try:
        # Step 1: Create table
        await create_announcements_table()

        # Step 2: Add sample data
        await create_sample_announcements()

        # Step 3: Verify
        await verify_announcements_schema()

        print("\n🎉 Announcements schema setup completed successfully!")
        print("📝 Next steps:")
        print("  1. Test announcement API endpoints")
        print("  2. Verify frontend integration")
        print("  3. Create more announcements via admin interface")

    except Exception as e:
        print(f"\n❌ Schema setup failed: {e}")
        print("🔄 Database should be in a consistent state (rollback applied)")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
