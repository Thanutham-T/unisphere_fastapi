from typing import AsyncIterator

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import (AsyncEngine, async_sessionmaker,
                                    create_async_engine)
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.core.config import get_settings

from . import greeting_model  # noqa: F401
from . import group_chat_model  # noqa: F401  Ensure models are imported
from . import user_model  # noqa: F401
from . import user_place_model  # noqa: F401

engine: AsyncEngine | None = None
redis_client: redis.Redis | None = None
settings = get_settings()


async def init_db():
    """Initialize the database engine and create tables."""
    global engine

    # Use configured DATABASE_URL; ensure it's an async driver URL
    db_url = settings.DATABASE_URL or ""
    if db_url.startswith("postgresql://"):
        # Upgrade to async driver if plain psycopg-style URL provided
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)

    # Fallback to local SQLite file for developer convenience
    if not db_url:
        db_url = "sqlite+aiosqlite:///./unisphere.db"

    engine = create_async_engine(
        db_url,
        echo=False,
        future=True,
    )

    await create_db_and_tables()


async def create_db_and_tables():
    """Create database tables."""
    if engine is None:
        raise RuntimeError(
            "Database engine is not initialized. Call init_db() first.")

    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Get async database session."""
    if engine is None:
        raise RuntimeError(
            "Database engine is not initialized. Call init_db() first.")

    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False)
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
    if redis_client is None:
        redis_client = redis.from_url(
            settings.REDIS_URL, decode_responses=True
        )
    try:
        yield redis_client
    finally:
        pass


async def close_redis():
    """Close Redis connection if initialized."""
    global redis_client
    if redis_client is not None:
        try:
            await redis_client.close()
        finally:
            try:
                await redis_client.connection_pool.disconnect()
            finally:
                redis_client = None
