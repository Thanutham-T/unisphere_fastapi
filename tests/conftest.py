import os

import httpx
import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.main import app
from unisphere.models import get_redis, get_session


@pytest_asyncio.fixture
async def engine():
    """Create test database engine."""
    load_dotenv(dotenv_path=".env.test")
    database_url = os.getenv("TEST_DATABASE_URL")
    engine = create_async_engine(
        database_url,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
    """Create test database session."""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def client(session):
    """Create test client with dependency override."""

    async def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://localhost:8000"
    ) as client:
        yield client

    app.dependency_overrides.clear()
