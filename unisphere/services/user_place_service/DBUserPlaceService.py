from datetime import datetime
from typing import List, Tuple

from sqlalchemy import desc
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models.user_place_model import UserPlace
from unisphere.schemas.user_place_schema import (UserPlaceCreate,
                                                 UserPlaceResponse)


class DBUserPlaceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_place(self, data: UserPlaceCreate, user_id: int) -> UserPlaceResponse:
        place = UserPlace(
            user_id=user_id,
            name=data.name,
            description=data.description,
            latitude=data.latitude,
            longitude=data.longitude,
            category=data.category,
            image_url=data.image_url,
            additional_info=data.additional_info,
            is_favorite=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.add(place)
        await self.db.commit()
        await self.db.refresh(place)
        return UserPlaceResponse.model_validate(place)

    async def list_my_places(self, user_id: int, limit: int, offset: int) -> Tuple[List[UserPlaceResponse], int]:
        result = await self.db.exec(
            select(UserPlace)
            .where(UserPlace.user_id == user_id)
            .order_by(desc(UserPlace.updated_at))  # type: ignore[arg-type]
            .offset(offset)
            .limit(limit)
        )
        rows = result.all()

        count_result = await self.db.exec(
            select(UserPlace).where(UserPlace.user_id == user_id)
        )
        total = len(count_result.all())
        return [UserPlaceResponse.model_validate(r) for r in rows], total

    async def delete_place(self, place_id: int, user_id: int) -> bool:
        result = await self.db.exec(
            select(UserPlace).where(UserPlace.id ==
                                    place_id, UserPlace.user_id == user_id)
        )
        place = result.first()
        if not place:
            return False
        await self.db.delete(place)
        await self.db.commit()
        return True
