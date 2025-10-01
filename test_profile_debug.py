#!/usr/bin/env python3
"""
Test profile update with debug logging
"""


def test_profile_update_debug():
    """Test profile update to see debug output"""

    # Test data from frontend log
    profile_data = {
        "student_id": None,
        "first_name": None,
        "last_name": None,
        "email": None,
        "phone_number": None,
        "profile_image_url": "http://10.0.2.2:8000/uploads/images/8a478c49-509e-47d5-9f71-e9eece245b86.jpg",
        "faculty": None,
        "department": None,
        "major": None,
        "curriculum": None,
        "education_level": None,
        "campus": None
    }

    print("🧪 Testing Profile Update with TestClient")
    print("📋 Profile data:", profile_data)

    # Since we can't easily login through TestClient due to DB init issues,
    # let's test the schema validation first
    from unisphere.schemas.user_schema import UserUpdate

    try:
        print("\n🔍 Testing UserUpdate schema validation...")
        user_update = UserUpdate(**profile_data)
        print("✅ Schema validation passed")
        print(
            f"📋 Validated data: {user_update.model_dump(exclude_unset=True)}")

        # Check which fields are actually set
        all_fields = user_update.model_dump(exclude_unset=True)
        non_none_fields = user_update.model_dump(
            exclude_unset=True, exclude_none=True)

        print(f"📊 All fields (exclude_unset=True): {list(all_fields.keys())}")
        print(
            f"📊 Non-None fields (exclude_unset=True, exclude_none=True): {list(non_none_fields.keys())}")

        if 'profile_image_url' in non_none_fields:
            print(
                f"✅ profile_image_url will be updated to: {non_none_fields['profile_image_url']}")
        else:
            print("❌ profile_image_url is not in non-None update data")

    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    test_profile_update_debug()
