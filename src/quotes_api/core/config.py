import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

env_name = os.getenv("ENV", "dev")
env_file = f".env.{env_name}"

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    project_name: str = "Quotes API"
    version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    env: str = env_name
    database_url: str
    valkey_url: str

    model_config = SettingsConfigDict(env_file=env_file, extra = "ignore")

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
