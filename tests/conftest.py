from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.quotes_api.core.cache import get_cache
from src.quotes_api.core.config import TestSettings
from src.quotes_api.db.session import Base, get_db
from src.quotes_api.main import app

# Creating a test-specific db engine
test_settings = TestSettings()
engine = create_engine(test_settings.database_url, connect_args={'check_same_thread': False}, poolclass=StaticPool)

# Creating a test-specific session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Mocking the cache dependency
async def override_get_cache():
    return None

# Overriding get_db dependency for tests

def override_get_db():
    """
        Dependency override to use the test database session.
        """
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_cache] = override_get_cache

# def get_test_settings() -> Settings:
#     """Returns a TestSettings instance."""
#     return TestSettings()
#
#
# # Override the dependency
# app.dependency_overrides[get_settings] = get_test_settings


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """
    The main fixture for testing. It creates the database tables before tests,
    yields a TestClient, and then drops the tables after tests are done.
    """
    # Create all tables in the in-memory database
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as c:
        yield c

    # Drop all tables after the tests have finished
    Base.metadata.drop_all(bind=engine)