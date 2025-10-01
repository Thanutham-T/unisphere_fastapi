#!/usr/bin/env python3
"""
Integration test for image upload functionality
"""
import io

from fastapi.testclient import TestClient
from PIL import Image

from unisphere.main import app


def test_image_upload_integration():
    """Test the complete image upload workflow"""
    client = TestClient(app)

    # First, we need to authenticate to get a token
    # Create a test user and login
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }

    # Register user
    register_response = client.post("/v1/auth/register", json=user_data)
    if register_response.status_code != 200:
        print(f"Registration failed: {register_response.text}")
        return

    # Login to get token
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }

    login_response = client.post("/v1/auth/login", json=login_data)
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a test image
    img = Image.new('RGB', (100, 100), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    # Test image upload
    files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
    upload_response = client.post(
        "/v1/upload/image", files=files, headers=headers)

    if upload_response.status_code == 200:
        result = upload_response.json()
        print("✅ Image upload successful!")
        print(f"   Filename: {result.get('filename', 'N/A')}")
        print(f"   URL: {result['url']}")

        # Extract filename from URL for testing retrieval
        filename = result['url'].split('/')[-1]

        # Test image retrieval
        get_response = client.get(f"/v1/upload/image/{filename}")
        if get_response.status_code == 200:
            print("✅ Image retrieval successful!")
            print(f"   Retrieved URL: {get_response.json()['url']}")
        else:
            print(f"❌ Image retrieval failed: {get_response.text}")

        # Test image deletion
        delete_response = client.delete(
            f"/v1/upload/image/{filename}", headers=headers)
        if delete_response.status_code == 200:
            print("✅ Image deletion successful!")
        else:
            print(f"❌ Image deletion failed: {delete_response.text}")
    else:
        print(f"❌ Image upload failed: {upload_response.text}")


if __name__ == "__main__":
    test_image_upload_integration()
