from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    project_name: str = "Quotes API"
    version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    env: str = Field(default="dev", description="Environment: dev, prod, test")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    """
    Load settings
    Cached so it's only created once per app lifecycle.
    """
    return Settings()

class TestSettings(Settings):
    """
    For tests, we override with a dedicated TestSettings class
    """
    model_config = SettingsConfigDict(env_file=".env.test", extra="ignore")
