import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_list_user_places(client: AsyncClient):
    # Register and login to get token
    registration_data = {
        "personal_info": {
            "first_name": "Ploy",
            "last_name": "Mapuser",
            "phone_number": "0800000000"
        },
        "education_info": {
            "student_id": "6404019999",
            "education_level": "ปริญญาตรี",
            "campus": "วิทยาเขตรังสิต",
            "faculty": "คณะวิทยาศาสตร์",
            "major": "วิทยาการคอมพิวเตอร์"
        },
        "account_info": {
            "email": "ploy@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }
    }

    r = await client.post("/v1/auth/register", json=registration_data)
    assert r.status_code == 201
    token = r.json()["token"]["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Create a place
    payload = {
        "name": "Central Library",
        "description": "Main university library",
        "latitude": 13.7563,
        "longitude": 100.5018,
        "category": "library",
        "image_url": "https://example.com/library.jpg",
        "additional_info": {"tags": ["library", "study", "quiet"]}
    }

    r = await client.post("/v1/user-places/", json=payload, headers=headers)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == payload["name"]
    assert data["category"] == payload["category"]
    additional_info = data.get("additional_info") or {}
    assert isinstance(additional_info, dict)  # type: ignore[arg-type]
    expected_tags = ["library", "study", "quiet"]
    assert additional_info.get("tags") == expected_tags

    # List my places
    r = await client.get("/v1/user-places/?limit=10&offset=0", headers=headers)
    assert r.status_code == 200
    list_response = r.json()
    assert list_response["total"] >= 1
    names = [p["name"] for p in list_response["places"]]
    assert payload["name"] in names


@pytest.mark.asyncio
async def test_places_are_user_scoped(client: AsyncClient):
    # Register user 1
    reg1 = {
        "personal_info": {"first_name": "A", "last_name": "One"},
        "education_info": {"student_id": "1"},
        "account_info": {"email": "one@example.com", "password": "pass1234", "confirm_password": "pass1234"}
    }
    r1 = await client.post("/v1/auth/register", json=reg1)
    t1 = r1.json()["token"]["access_token"]

    # Register user 2
    reg2 = {
        "personal_info": {"first_name": "B", "last_name": "Two"},
        "education_info": {"student_id": "2"},
        "account_info": {"email": "two@example.com", "password": "pass1234", "confirm_password": "pass1234"}
    }
    r2 = await client.post("/v1/auth/register", json=reg2)
    t2 = r2.json()["token"]["access_token"]

    h1 = {"Authorization": f"Bearer {t1}"}
    h2 = {"Authorization": f"Bearer {t2}"}

    # User 1 creates a place
    p1 = {"name": "Eng Building", "latitude": 13.0,
          "longitude": 100.0, "category": "building"}
    r = await client.post("/v1/user-places/", json=p1, headers=h1)
    assert r.status_code == 201

    # User 2 should not see user 1's place
    r = await client.get("/v1/user-places/", headers=h2)
    assert r.status_code == 200
    l2 = r.json()
    names2 = [p["name"] for p in l2["places"]]
    assert p1["name"] not in names2


@pytest.mark.asyncio
async def test_delete_place(client: AsyncClient):
    reg = {
        "personal_info": {"first_name": "C", "last_name": "Three"},
        "education_info": {"student_id": "3"},
        "account_info": {"email": "three@example.com", "password": "pass1234", "confirm_password": "pass1234"}
    }
    r = await client.post("/v1/auth/register", json=reg)
    token = r.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    p = {"name": "Art Building", "latitude": 13.1,
         "longitude": 100.2, "category": "building"}
    r = await client.post("/v1/user-places/", json=p, headers=headers)
    place_id = r.json()["id"]

    r = await client.delete(f"/v1/user-places/{place_id}", headers=headers)
    assert r.status_code == 200

    # Confirm it is gone
    r = await client.get("/v1/user-places/", headers=headers)
    names = [x["name"] for x in r.json()["places"]]
    assert p["name"] not in names
