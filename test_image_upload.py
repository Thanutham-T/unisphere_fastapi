#!/usr/bin/env python3
"""
Test script fo                    error_data = await resp.json()
                    print(f"❌ Login failed: {error_data}")
                    return
        except (aiohttp.ClientError, aiohttp.ClientResponseError, KeyError) as e:
            print(f"❌ Login error: {str(e)}")
            returne Upload functionality
"""
import asyncio
import io

import aiohttp

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    print("PIL (Pillow) not available for testing")
    HAS_PIL = False
    Image = None  # type: ignore[assignment]


async def test_image_upload():
    """Test the image upload system"""
    base_url = "http://localhost:8000/v1"
    uploaded_filename = None  # Initialize to use later

    # Test credentials
    test_email = "admin@unisphere.com"
    test_password = "admin123"

    async with aiohttp.ClientSession() as session:
        print("📷 Testing Image Upload System")
        print("=" * 50)

        # 1. Login to get token
        print("1. Logging in...")
        login_data = {
            "email": test_email,
            "password": test_password
        }

        try:
            async with session.post(f"{base_url}/auth/login", json=login_data) as resp:
                if resp.status == 200:
                    login_response = await resp.json()
                    token = login_response["token"]["access_token"]
                    print("✅ Login successful")
                else:
                    error_data = await resp.json()
                    print(f"❌ Login failed: {error_data}")
                    return
        except (aiohttp.ClientError, aiohttp.ClientResponseError, OSError, ValueError, KeyError) as e:  # noqa: BLE001
            print(f"❌ Error: {e}")
            return

        headers = {"Authorization": f"Bearer {token}"}

        # 2. Get upload info
        print("2. Getting upload information...")
        try:
            async with session.get(f"{base_url}/upload/info", headers=headers) as resp:
                if resp.status == 200:
                    upload_info = await resp.json()
                    print("✅ Upload info retrieved")
                    print(
                        f"   Max file size: {upload_info['max_file_size_mb']}MB")
                    print(
                        f"   Allowed extensions: {', '.join(upload_info['allowed_extensions'])}")
                else:
                    print(f"❌ Failed to get upload info: {resp.status}")
        except (aiohttp.ClientError, aiohttp.ClientResponseError, KeyError) as e:
            print(f"❌ Upload info error: {e}")

        # 3. Create a test image
        print("3. Creating test image...")
        try:
            # Create a simple test image using PIL
            img = Image.new('RGB', (200, 200), color='red')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            print("✅ Test image created")
        except Exception as e:  # noqa: BLE001
            print(f"❌ Failed to create test image: {e}")
            return

        # 4. Upload the image
        print("4. Uploading image...")
        try:
            data = aiohttp.FormData()
            data.add_field('file',
                           img_bytes.getvalue(),
                           filename='test_image.png',
                           content_type='image/png')

            async with session.post(f"{base_url}/upload/image",
                                    data=data,
                                    headers=headers) as resp:
                if resp.status == 200:
                    upload_response = await resp.json()
                    print("✅ Image uploaded successfully")
                    print(f"   URL: {upload_response['url']}")
                    print(
                        f"   Filename: {upload_response.get('filename', 'N/A')}")

                    # Extract filename from URL for later tests
                    uploaded_url = upload_response['url']
                    # Update the function-scope variable
                    uploaded_filename = uploaded_url.split('/')[-1]
                    print(f"   Extracted filename: {uploaded_filename}")
                else:
                    error_data = await resp.json()
                    print(f"❌ Upload failed: {error_data}")
                    return
        except (aiohttp.ClientError, aiohttp.ClientResponseError) as e:
            print(f"❌ Upload error: {e}")
            return

        # 5. Test accessing the uploaded image
        print("5. Testing image access...")
        try:
            image_url = upload_response['url']
            async with session.get(image_url) as resp:
                if resp.status == 200:
                    print("✅ Image is accessible via URL")
                    print(
                        f"   Content-Type: {resp.headers.get('content-type')}")
                else:
                    print(f"❌ Cannot access image: {resp.status}")
        except (aiohttp.ClientError, aiohttp.ClientResponseError, OSError, ValueError, KeyError) as e:  # noqa: BLE001
            print(f"❌ Error: {e}")

        # 6. Test creating event with image
        print("6. Testing event creation with image...")
        try:
            event_data = {
                "title": "Test Event with Image",
                "description": "This event has an uploaded image",
                "category": "test",
                "image_url": upload_response['url'],
                "location": "Test Location",
                "date": "2025-10-15T10:00:00"
            }

            async with session.post(f"{base_url}/events",
                                    json=event_data,
                                    headers=headers) as resp:
                if resp.status == 200:
                    event_response = await resp.json()
                    print("✅ Event with image created successfully")
                    print(f"   Event ID: {event_response['id']}")
                    print(f"   Image URL: {event_response['image_url']}")
                else:
                    error_data = await resp.json()
                    print(f"❌ Event creation failed: {error_data}")
        except (aiohttp.ClientError, aiohttp.ClientResponseError, OSError, ValueError, KeyError) as e:  # noqa: BLE001
            print(f"❌ Error: {e}")

        # 7. Test image deletion (optional)
        print("7. Testing image deletion...")
        if uploaded_filename:
            try:
                # Use the filename from uploaded image for deletion
                async with session.delete(f"{base_url}/upload/image/{uploaded_filename}",
                                          headers=headers) as resp:
                    if resp.status == 200:
                        delete_response = await resp.json()
                        print("✅ Image deleted successfully")
                        print(f"   Message: {delete_response['message']}")
                    else:
                        error_data = await resp.json()
                        print(f"⚠️ Image deletion failed: {error_data}")
            except Exception as e:  # noqa: BLE001
                print(f"⚠️ Image deletion error: {e}")
        else:
            print("⚠️ No uploaded filename available for deletion")

        print("\n🎉 Image Upload System Test Completed!")


if __name__ == "__main__":
    print("🚀 Starting Image Upload Tests")
    print("Make sure the server is running on http://localhost:8000")
    print("Installing required dependencies...")

    if not HAS_PIL:
        print("❌ PIL not available. Install with: pip install Pillow")
        exit(1)
    else:
        print("✅ PIL available")

    print()

    try:
        asyncio.run(test_image_upload())
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except (RuntimeError, OSError) as e:
        print(f"❌ Test failed with error: {e}")

    print("\n✨ Test completed!")
