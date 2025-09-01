import pytest
from fastapi.testclient import TestClient
from src.quotes_api.main import app
from src.quotes_api.core.config import get_settings, Settings, TestSettings

def get_test_settings() -> Settings:
    """Returns a TestSettings instance."""
    return TestSettings()


# Override the dependency
app.dependency_overrides[get_settings] = get_test_settings


@pytest.fixture
def client() -> TestClient:
    """
    Get a TestClient instance that uses the special test settings.
    """
    return TestClient(app)