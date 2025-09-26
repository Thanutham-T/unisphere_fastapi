from abc import ABC, abstractmethod
from typing import List, Optional

from unisphere.schemas import greeting_schema


class GreetingServiceInterface(ABC):
    """Greeting service interface"""

    @abstractmethod
    async def list_greetings(self) -> List[greeting_schema.Greeting]:
        """List all greetings."""
        pass

    @abstractmethod
    async def get_greeting(self, greeting_id: int) -> Optional[greeting_schema.Greeting]:
        """Get a specific greeting by ID."""
        pass

    @abstractmethod
    async def create_greeting(
        self, greeting: greeting_schema.GreetingCreate
    ) -> greeting_schema.Greeting:
        """Create a new greeting."""
        pass

    @abstractmethod
    async def update_greeting(
        self, greeting_id: int, greeting: greeting_schema.GreetingUpdate
    ) -> Optional[greeting_schema.Greeting]:
        """Update an existing greeting."""
        pass

    @abstractmethod
    async def remove_greeting(self, greeting_id: int) -> Optional[greeting_schema.Greeting]:
        """Remove an existing greeting."""
        pass
