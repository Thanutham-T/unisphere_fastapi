import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration"""
    registration_data = {
        "personal_info": {
            "first_name": "สมชาย",
            "last_name": "ใจดี",
            "phone_number": "0812345678"
        },
        "education_info": {
            "student_id": "6404010001",
            "education_level": "ปริญญาตรี",
            "campus": "วิทยาเขตรังสิต",
            "faculty": "คณะวิศวกรรมศาสตร์",
            "major": "วิศวกรรมคอมพิวเตอร์",
            "curriculum": "หลักสูตรวิศวกรรมคอมพิวเตอร์ 2564",
            "department": "ภาควิชาวิศวกรรมคอมพิวเตอร์"
        },
        "account_info": {
            "email": "somchai@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }
    }

    response = await client.post("/v1/auth/register", json=registration_data)
    assert response.status_code == 201

    data = response.json()
    assert "user" in data
    assert "token" in data
    assert data["user"]["email"] == "somchai@example.com"
    assert data["user"]["first_name"] == "สมชาย"
    assert data["user"]["last_name"] == "ใจดี"


@pytest.mark.asyncio
async def test_register_user_password_mismatch(client: AsyncClient):
    """Test user registration with password mismatch"""
    registration_data = {
        "personal_info": {
            "first_name": "สมชาย",
            "last_name": "ใจดี",
            "phone_number": "0812345678"
        },
        "education_info": {
            "student_id": "6404010001",
            "education_level": "ปริญญาตรี",
            "campus": "วิทยาเขตรังสิต",
            "faculty": "คณะวิศวกรรมศาสตร์",
            "major": "วิศวกรรมคอมพิวเตอร์"
        },
        "account_info": {
            "email": "somchai@example.com",
            "password": "password123",
            "confirm_password": "password456"  # Different password
        }
    }

    response = await client.post("/v1/auth/register", json=registration_data)
    assert response.status_code == 400
    assert "Password and confirm password do not match" in response.json()[
        "detail"]


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    """Test user login"""
    # First register a user
    registration_data = {
        "personal_info": {
            "first_name": "สมหญิง",
            "last_name": "รักเรียน",
            "phone_number": "0887654321"
        },
        "education_info": {
            "student_id": "6404010002",
            "education_level": "ปริญญาตรี",
            "campus": "วิทยาเขตรังสิต",
            "faculty": "คณะแพทยศาสตร์",
            "major": "แพทยศาสตร์"
        },
        "account_info": {
            "email": "somying@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }
    }

    await client.post("/v1/auth/register", json=registration_data)

    # Now login
    login_data = {
        "email": "somying@example.com",
        "password": "password123"
    }

    response = await client.post("/v1/auth/login", json=login_data)
    assert response.status_code == 200

    data = response.json()
    assert "user" in data
    assert "token" in data
    assert data["user"]["email"] == "somying@example.com"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials"""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }

    response = await client.post("/v1/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient):
    """Test getting current user info"""
    # First register and get token
    registration_data = {
        "personal_info": {
            "first_name": "สมศักดิ์",
            "last_name": "ขยัน",
            "phone_number": "0819876543"
        },
        "education_info": {
            "student_id": "6404010003",
            "education_level": "ปริญญาตรี",
            "campus": "วิทยาเขตรังสิต",
            "faculty": "คณะบริหารธุรกิจ",
            "major": "การบัญชี"
        },
        "account_info": {
            "email": "somsak@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }
    }

    response = await client.post("/v1/auth/register", json=registration_data)
    token = response.json()["token"]["access_token"]

    # Get current user info
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/v1/auth/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "somsak@example.com"
    assert data["first_name"] == "สมศักดิ์"


@pytest.mark.asyncio
async def test_get_me_invalid_token(client: AsyncClient):
    """Test getting current user with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.get("/v1/auth/me", headers=headers)

    assert response.status_code == 401
    assert "Invalid or expired token" in response.json()["detail"]


@pytest.mark.asyncio
async def test_logout(client: AsyncClient):
    """Test user logout"""
    # Register and get token
    registration_data = {
        "personal_info": {
            "first_name": "สมปอง",
            "last_name": "มานะ",
            "phone_number": "0856789012"
        },
        "education_info": {
            "student_id": "6404010004",
            "education_level": "ปริญญาตรี",
            "campus": "วิทยาเขตรังสิต",
            "faculty": "คณะวิทยาศาสตร์",
            "major": "วิทยาศาสตร์คอมพิวเตอร์"
        },
        "account_info": {
            "email": "sompong@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }
    }

    response = await client.post("/v1/auth/register", json=registration_data)
    token = response.json()["token"]["access_token"]

    # Logout
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/v1/auth/logout", headers=headers)

    assert response.status_code == 200
    assert "Successfully logged out" in response.json()["message"]


@pytest.mark.asyncio
async def test_get_education_options(client: AsyncClient):
    """Test getting education options for dropdowns"""
    response = await client.get("/v1/auth/education-options")

    assert response.status_code == 200
    data = response.json()

    assert "education_levels" in data
    assert "campuses" in data
    assert "faculties" in data
    assert "majors" in data

    assert "ปริญญาตรี" in data["education_levels"]
    assert "วิทยาเขตรังสิต" in data["campuses"]
    assert "คณะวิศวกรรมศาสตร์" in data["faculties"]
