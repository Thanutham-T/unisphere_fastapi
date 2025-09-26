from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models.greeting_model import Greeting
from unisphere.schemas import greeting_schema

from .GreetingServiceInterface import GreetingServiceInterface


class DBGreetingService(GreetingServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_greetings(self) -> List[Greeting]:
        result = await self.session.exec(select(Greeting))
        return result.all()

    async def get_greeting(self, greeting_id: int) -> Optional[Greeting]:
        result = await self.session.exec(select(Greeting).where(Greeting.id == greeting_id))
        greeting = result.first()
        if not greeting:
            raise HTTPException(status_code=404, detail="Greeting not found")
        return greeting

    async def create_greeting(self, greeting: greeting_schema.GreetingCreate) -> Greeting:
        new_greeting = Greeting(
            message=greeting.message,
            language=greeting.language,
            recipient_name=greeting.recipient_name,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.session.add(new_greeting)
        await self.session.commit()
        await self.session.refresh(new_greeting)
        return new_greeting

    async def update_greeting(self, greeting_id: int, greeting: greeting_schema.GreetingUpdate) -> Greeting:
        result = await self.session.exec(select(Greeting).where(Greeting.id == greeting_id))
        db_greeting = result.first()
        if not db_greeting:
            raise HTTPException(status_code=404, detail="Greeting not found")

        update_data = greeting.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_greeting, field, value)
        db_greeting.updated_at = datetime.now()

        self.session.add(db_greeting)
        await self.session.commit()
        await self.session.refresh(db_greeting)
        return db_greeting

    async def remove_greeting(self, greeting_id: int) -> Greeting:
        result = await self.session.exec(select(Greeting).where(Greeting.id == greeting_id))
        db_greeting = result.first()
        if not db_greeting:
            raise HTTPException(status_code=404, detail="Greeting not found")

        await self.session.delete(db_greeting)
        await self.session.commit()
        return db_greeting
