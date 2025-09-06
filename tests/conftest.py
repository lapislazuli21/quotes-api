from typing import AsyncGenerator

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.quotes_api.core.cache import get_cache
from src.quotes_api.core.config import TestSettings
from src.quotes_api.db.session import Base, get_db
from src.quotes_api.main import app

# from sqlalchemy.pool import StaticPool

# Creating a test-specific db engine
test_settings = TestSettings()
engine = create_async_engine(test_settings.database_url)

# Creating a test-specific session factory
TestingSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Mocking the cache dependency
async def override_get_cache():
    return None

# Overriding get_db dependency for tests

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency override to use the test database session.
    """
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_cache] = override_get_cache

@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncGenerator[TestClient, None]:
    """
    The main fixture for testing. It creates the database tables before tests,
    yields a TestClient, and then drops the tables after tests are done.
    """
    # Create all tables in the in-memory database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    with TestClient(app) as c:
        yield c

    # Drop all tables after the tests have finished
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="module")
async def authorized_client(client: TestClient):
    """
    A TestClient that includes the API key in its headers for authorized requests.
    """
    async for c in client:
        api_key = test_settings.api_key
        c.headers = {"X-API-Key": api_key, **c.headers}
        yield c