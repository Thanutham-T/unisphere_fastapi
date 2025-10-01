#!/usr/bin/env python3
"""
Manual server test for profile update
"""
import asyncio

import aiohttp


async def test_with_real_server():
    """Test profile update with running server"""
    base_url = "http://localhost:8000"

    # Create a test user first
    register_data = {
        "personal_info": {
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "0123456789"
        },
        "education_info": {
            "student_id": "test123",
            "education_level": "bachelor",
            "campus": "main",
            "faculty": "engineering",
            "major": "computer",
            "curriculum": "cs",
            "department": "computer"
        },
        "account_info": {
            "email": "testprofile@example.com",
            "password": "testpass123",
            "confirm_password": "testpass123"
        }
    }

    login_data = {
        "email": "testprofile@example.com",
        "password": "testpass123"
    }

    profile_update_data = {
        "profile_image_url": "http://localhost:8000/uploads/images/test-image.jpg"
    }

    async with aiohttp.ClientSession() as session:
        try:
            # 1. Register user
            print("1. 📝 Registering test user...")
            async with session.post(f"{base_url}/v1/auth/register", json=register_data) as resp:
                if resp.status == 200:
                    print("✅ User registered successfully")
                else:
                    print(f"⚠️ Registration status: {resp.status}")
                    print(f"Response: {await resp.text()}")

            # 2. Login
            print("\n2. 🔑 Logging in...")
            async with session.post(f"{base_url}/v1/auth/login", json=login_data) as resp:
                if resp.status == 200:
                    login_response = await resp.json()
                    token = login_response["access_token"]
                    print("✅ Login successful")
                else:
                    print(f"❌ Login failed: {resp.status}")
                    print(await resp.text())
                    return

            # 3. Update profile
            print("\n3. 🔄 Updating profile...")
            headers = {"Authorization": f"Bearer {token}"}
            async with session.put(f"{base_url}/v1/auth/profile",
                                   json=profile_update_data,
                                   headers=headers) as resp:
                print(f"📡 Response status: {resp.status}")
                response_text = await resp.text()
                print(f"📄 Response: {response_text}")

                if resp.status == 200:
                    print("✅ Profile update successful!")
                    response_data = await resp.json() if resp.content_type == 'application/json' else None
                    if response_data and 'profile_image_url' in response_data:
                        print(
                            f"🖼️ Updated profile_image_url: {response_data['profile_image_url']}")
                else:
                    print("❌ Profile update failed")

        except Exception as e:
            print(f"❌ Test error: {e}")

if __name__ == "__main__":
    print("🧪 Manual Server Test for Profile Update")
    print("🚨 Make sure server is running on localhost:8000")
    print("🚨 This will create a test user: testprofile@example.com")

    try:
        asyncio.run(test_with_real_server())
    except Exception as e:
        print(f"❌ Test failed: {e}")

    print("\n✨ Test completed!")
