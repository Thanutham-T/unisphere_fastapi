from typing import AsyncIterator

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.core.config import get_settings
from unisphere.models.greeting_model import Greeting, GreetingBase

engine: AsyncEngine = None
settings = get_settings()


async def init_db():
    """Initialize the database engine and create tables."""
    global engine

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        future=True,
    )

    await create_db_and_tables()


async def create_db_and_tables():
    """Create database tables."""
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Get async database session."""
    if engine is None:
        raise Exception(
            "Database engine is not initialized. Call init_db() first.")

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def close_db():
    """Close database connection."""
    global engine
    if engine is not None:
        await engine.dispose()
        engine = None


async def get_redis() -> AsyncIterator[redis.Redis]:
    """
    Dependency to get Redis client.
    Yields a shared async Redis instance.
    """
    global redis_client
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        yield redis_client
    finally:
        # Optionally, you can close the connection on app shutdown
        # but usually we keep a single client open during app lifetime
        pass


async def close_redis():
    """Close Redis connection."""
    await redis_client.close()
