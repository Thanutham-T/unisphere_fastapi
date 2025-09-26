import pytest
import pytest_asyncio

from tests.conftest import client

# ------------------------ Fixtures ------------------------


@pytest_asyncio.fixture
async def greeting_data():
    return {
        "message": "Hello Test",
        "language": "en",
        "recipient_name": "Alice"
    }


# ------------------------ Tests ------------------------

@pytest.mark.asyncio
async def test_create_greeting(client, greeting_data):
    response = await client.post("/v1/greetings/", json=greeting_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == greeting_data["message"]
    assert data["language"] == greeting_data["language"]
    assert data["recipient_name"] == greeting_data["recipient_name"]
