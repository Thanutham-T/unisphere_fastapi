import datetime
from typing import List, Optional

from unisphere.schemas import greeting_schema

from .GreetingServiceInterface import GreetingServiceInterface

# ---------------- Mock Data ---------------- #
mock_greetings: List[greeting_schema.Greeting] = [
    greeting_schema.Greeting(
        id=1,
        message="Hello, world!",
        language="en",
        recipient_name="Alice",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    ),
    greeting_schema.Greeting(
        id=2,
        message="สวัสดี",
        language="th",
        recipient_name="Bob",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    ),
]

mock_greeting_id = 3


# ---------------- Mock Service ---------------- #
class MockGreetingService(GreetingServiceInterface):
    async def list_greetings(self) -> List[greeting_schema.Greeting]:
        return mock_greetings

    async def get_greeting(self, greeting_id: int) -> Optional[greeting_schema.Greeting]:
        for greeting in mock_greetings:
            if greeting.id == greeting_id:
                return greeting
        return None

    async def create_greeting(self, greeting: greeting_schema.GreetingCreate) -> greeting_schema.Greeting:
        global mock_greeting_id
        new_greeting = greeting_schema.Greeting(
            id=mock_greeting_id,
            message=greeting.message,
            language=greeting.language,
            recipient_name=greeting.recipient_name,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        mock_greetings.append(new_greeting)
        mock_greeting_id += 1
        return new_greeting

    async def update_greeting(
        self, greeting_id: int, greeting: greeting_schema.GreetingUpdate
    ) -> Optional[greeting_schema.Greeting]:
        for g in mock_greetings:
            if g.id == greeting_id:
                update_data = greeting.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(g, field, value)
                g.updated_at = datetime.datetime.now()
                return g
        return None

    async def remove_greeting(self, greeting_id: int) -> Optional[greeting_schema.Greeting]:
        for g in mock_greetings:
            if g.id == greeting_id:
                mock_greetings.remove(g)
                return g
        return None
        return None
