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
from unisphere.models import get_session


@pytest_asyncio.fixture
async def engine_fixture():
    """Create test database engine."""
    load_dotenv(dotenv_path=".env.test")
    database_url = os.getenv("TEST_DATABASE_URL")
    engine_ = create_async_engine(
        database_url,
    )

    # Create tables
    async with engine_.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine_
    await engine_.dispose()


@pytest_asyncio.fixture
async def session_fixture(engine_fixture):
    """Create test database session."""
    session_factory = sessionmaker(
        engine_fixture, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as db_session:
        yield db_session


@pytest_asyncio.fixture
async def client(session_fixture):
    """Create test client with dependency override."""

    async def get_session_override():
        yield session_fixture

    # override get_session to use test session
    app.dependency_overrides[get_session] = get_session_override

    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://localhost:8000"
    ) as http_client:
        yield http_client

    app.dependency_overrides.clear()
