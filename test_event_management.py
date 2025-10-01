#!/usr/bin/env python3
"""
Test script for Event Management functionality
"""
import asyncio
from datetime import datetime, timedelta

import aiohttp


async def test_event_management():
    """Test the event management system"""
    base_url = "http://localhost:8000/v1"

    # Admin credentials
    admin_email = "admin@unisphere.com"
    admin_password = "admin123"

    # Regular user credentials
    user_email = "user@unisphere.com"
    user_password = "user123"

    async with aiohttp.ClientSession() as session:
        print("🎪 Testing Event Management System")
        print("=" * 50)

        # 1. Register Admin User
        print("1. Setting up admin user...")
        admin_register_data = {
            "personal_info": {
                "first_name": "Admin",
                "last_name": "User",
                "email": admin_email,
                "phone_number": "0812345678"
            },
            "education_info": {
                "student_id": "ADMIN001",
                "faculty": "คณะบริหารธุรกิจ",
                "department": "การจัดการ",
                "major": "บริหารธุรกิจ",
                "curriculum": "ปกติ",
                "education_level": "ปริญญาตรี",
                "campus": "บางเขน"
            },
            "account_info": {
                "email": admin_email,
                "password": admin_password,
                "confirm_password": admin_password
            }
        }

        try:
            async with session.post(f"{base_url}/auth/register", json=admin_register_data) as resp:
                if resp.status in [201, 400]:  # 400 if already exists
                    print("✅ Admin user ready")
                else:
                    print(f"❌ Admin registration failed: {resp.status}")
                    return
        except (aiohttp.ClientError, ValueError) as e:
            print(f"❌ Admin registration error: {e}")
            return

        # 2. Login as Admin
        print("2. Logging in as admin...")
        admin_login_data = {
            "email": admin_email,
            "password": admin_password
        }

        try:
            async with session.post(f"{base_url}/auth/login", json=admin_login_data) as resp:
                if resp.status == 200:
                    login_response = await resp.json()
                    admin_token = login_response["token"]["access_token"]
                    print("✅ Admin login successful")
                else:
                    error_data = await resp.json()
                    print(f"❌ Admin login failed: {error_data}")
                    return
        except (aiohttp.ClientError, ValueError) as e:
            print(f"❌ Admin login error: {e}")
            return

        # 3. Update Admin Role (if needed)
        print("3. Checking admin role...")
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # First get current user info
        try:
            async with session.get(f"{base_url}/auth/me", headers=admin_headers) as resp:
                if resp.status == 200:
                    user_info = await resp.json()
                    if user_info["role"] != "admin":
                        # Update role to admin
                        update_data = {"role": "admin"}
                        async with session.put(f"{base_url}/auth/profile",
                                               json=update_data,
                                               headers=admin_headers) as update_resp:
                            if update_resp.status == 200:
                                print("✅ Admin role updated")
                            else:
                                print(
                                    "⚠️ Could not update admin role, continuing...")
                    else:
                        print("✅ Admin role confirmed")
        except (aiohttp.ClientError, ValueError) as e:
            print(f"⚠️ Admin role check error: {e}")

        # 4. Create Events as Admin
        print("4. Creating events...")
        future_date = datetime.now() + timedelta(days=7)

        events_to_create = [
            {
                "title": "Tech Workshop: FastAPI & Python",
                "description": "เรียนรู้การพัฒนา API ด้วย FastAPI และ Python สำหรับการพัฒนาเว็บแอปพลิเคชัน",
                "category": "workshop",
                "location": "ห้องคอมพิวเตอร์ 301",
                "date": future_date.isoformat()
            },
            {
                "title": "University Sports Day",
                "description": "กิจกรรมกีฬาประจำปีของมหาวิทยาลัย ร่วมสนุกกับกิจกรรมกีฬาหลากหลายชนิด",
                "category": "sports",
                "location": "สนามกีฬามหาวิทยาลัย",
                "date": (future_date + timedelta(days=3)).isoformat()
            },
            {
                "title": "Career Fair 2025",
                "description": "งานแสดงอาชีพและการจ้างงาน พบกับบริษัทชั้นนำมากมาย",
                "category": "career",
                "location": "หอประชุมใหญ่",
                "date": (future_date + timedelta(days=14)).isoformat()
            }
        ]

        created_events = []
        for event_data in events_to_create:
            try:
                async with session.post(f"{base_url}/events",
                                        json=event_data,
                                        headers=admin_headers) as resp:
                    if resp.status == 200:
                        created_event = await resp.json()
                        created_events.append(created_event)
                        print(f"✅ Created event: {event_data['title']}")
                    else:
                        error_data = await resp.json()
                        print(
                            f"❌ Failed to create event {event_data['title']}: {error_data}")
            except (aiohttp.ClientError, aiohttp.ClientResponseError, KeyError) as e:
                print(f"❌ Event creation error: {e}")

        if not created_events:
            print("❌ No events created, stopping test")
            return

        # 5. Get All Events
        print("5. Retrieving all events...")
        try:
            async with session.get(f"{base_url}/events", headers=admin_headers) as resp:
                if resp.status == 200:
                    events = await resp.json()
                    print(f"✅ Retrieved {len(events)} events")
                    for event in events:
                        print(
                            f"   - {event['title']} ({event['status']}) - Registrations: {event['registration_count']}")
                else:
                    error_data = await resp.json()
                    print(f"❌ Failed to get events: {error_data}")
        except (aiohttp.ClientError, aiohttp.ClientResponseError, OSError, ValueError, KeyError) as e:  # noqa: BLE001
            print(f"❌ Error: {e}")

        # 6. Register Regular User
        print("6. Setting up regular user...")
        user_register_data = {
            "personal_info": {
                "first_name": "Regular",
                "last_name": "User",
                "email": user_email,
                "phone_number": "0887654321"
            },
            "education_info": {
                "student_id": "65010123",
                "faculty": "คณะวิทยาศาสตร์",
                "department": "วิทยาการคอมพิวเตอร์",
                "major": "วิทยาการคอมพิวเตอร์",
                "curriculum": "ปกติ",
                "education_level": "ปริญญาตรี",
                "campus": "บางเขน"
            },
            "account_info": {
                "email": user_email,
                "password": user_password,
                "confirm_password": user_password
            }
        }

        try:
            async with session.post(f"{base_url}/auth/register", json=user_register_data) as resp:
                if resp.status in [201, 400]:  # 400 if already exists
                    print("✅ Regular user ready")
                else:
                    print(f"❌ User registration failed: {resp.status}")
                    return
        except (aiohttp.ClientError, aiohttp.ClientResponseError, OSError, ValueError, KeyError) as e:  # noqa: BLE001
            print(f"❌ Error: {e}")
            return

        # 7. Login as Regular User
        print("7. Logging in as regular user...")
        user_login_data = {
            "email": user_email,
            "password": user_password
        }

        try:
            async with session.post(f"{base_url}/auth/login", json=user_login_data) as resp:
                if resp.status == 200:
                    login_response = await resp.json()
                    user_token = login_response["token"]["access_token"]
                    print("✅ User login successful")
                else:
                    error_data = await resp.json()
                    print(f"❌ User login failed: {error_data}")
                    return
        except (aiohttp.ClientError, aiohttp.ClientResponseError, OSError, ValueError, KeyError) as e:  # noqa: BLE001
            print(f"❌ Error: {e}")
            return

        user_headers = {"Authorization": f"Bearer {user_token}"}

        # 8. User Views Events
        print("8. User viewing events...")
        try:
            async with session.get(f"{base_url}/events", headers=user_headers) as resp:
                if resp.status == 200:
                    user_events = await resp.json()
                    print(f"✅ User can see {len(user_events)} events")
                else:
                    print(f"❌ User cannot view events: {resp.status}")
        except (aiohttp.ClientError, aiohttp.ClientResponseError, OSError, ValueError, KeyError) as e:  # noqa: BLE001
            print(f"❌ Error: {e}")

        # 9. User Registers for Event
        if created_events:
            event_id = created_events[0]["id"]
            print(
                f"9. User registering for event: {created_events[0]['title']}...")

            registration_data = {
                "notes": "Looking forward to this event!"
            }

            try:
                async with session.post(f"{base_url}/events/{event_id}/register",
                                        json=registration_data,
                                        headers=user_headers) as resp:
                    if resp.status == 200:
                        registration = await resp.json()
                        print("✅ User registered for event successfully")
                        print(f"   Registration ID: {registration['id']}")
                    else:
                        error_data = await resp.json()
                        print(f"❌ Registration failed: {error_data}")
            except (aiohttp.ClientError, aiohttp.ClientResponseError, OSError, ValueError, KeyError) as e:  # noqa: BLE001
                print(f"❌ Error: {e}")

        # 10. Verify Registration
        print("10. Verifying registration...")
        try:
            async with session.get(f"{base_url}/events", headers=user_headers) as resp:
                if resp.status == 200:
                    events_after_registration = await resp.json()
                    for event in events_after_registration:
                        if event["id"] == event_id:
                            print(
                                f"✅ Registration confirmed - Count: {event['registration_count']}, User registered: {event['is_registered']}")
                            break
        except (aiohttp.ClientError, aiohttp.ClientResponseError, OSError, ValueError, KeyError) as e:  # noqa: BLE001
            print(f"❌ Error: {e}")

        print("\n🎉 Event Management System Test Completed!")


if __name__ == "__main__":
    print("🚀 Starting Event Management Tests")
    print("Make sure the server is running on http://localhost:8000")
    print()

    try:
        asyncio.run(test_event_management())
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except (RuntimeError, OSError) as e:
        print(f"❌ Test failed with error: {e}")

    print("\n✨ Test completed!")
