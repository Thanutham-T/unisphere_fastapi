from typing import AsyncIterator

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import (AsyncEngine, async_sessionmaker,
                                    create_async_engine)
from sqlmodel import SQLModel, select, text
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.core.config import get_settings
from unisphere.models.announcement_model import Announcement  # noqa: F401
from unisphere.models.event_model import Event, EventRegistration  # noqa: F401
from unisphere.models.greeting_model import Greeting  # noqa: F401

# Import all models so they are registered with SQLModel
from unisphere.models.user_model import User, UserBase  # noqa: F401

from .branch_model import *
from .checkin_model import *
from .course_model import *
from .day_of_week_model import *
from .faculty_model import *
from .notification_model import *
from .schedule_model import *
from .section_instructor import *
from .section_model import *
from .semester_model import *
from .user_enroll_model import *
from .user_model import *
from .user_place_model import *

engine: AsyncEngine | None = None
redis_client: redis.Redis | None = None
settings = get_settings()


async def init_db():
    """Initialize the database engine and create tables."""
    global engine  # noqa: PLW0603,RUF100

    # Use configured DATABASE_URL; must be an async driver URL (e.g., sqlite+aiosqlite, postgresql+asyncpg)
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        future=True,
    )
    await create_db_and_tables()

async def create_db_and_tables():
    """Create database tables."""
    if engine is None:
        raise RuntimeError("Database engine is not initialized. Call init_db() first.")

    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        # for table in reversed(SQLModel.metadata.sorted_tables):
        #     await conn.execute(text(f'DROP TABLE IF EXISTS "{table.name}" CASCADE'))
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Get async database session."""
    if engine is None:
        raise RuntimeError("Database engine is not initialized. Call init_db() first.")

    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async def close_db():
    """Close database connection."""
    global engine  # noqa: PLW0603,RUF100
    if engine is not None:
        await engine.dispose()
        engine = None


async def get_redis() -> AsyncIterator[redis.Redis]:
    """
    Dependency to get Redis client.
    Yields a shared async Redis instance.
    """
    global redis_client  # noqa: PLW0603,RUF100
    if redis_client is None:
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        yield redis_client
    finally:
        pass


async def close_redis():
    """Close Redis connection if initialized."""
    global redis_client  # noqa: PLW0603,RUF100
    if redis_client is not None:
        await redis_client.close()
        await redis_client.connection_pool.disconnect()
        redis_client = None
