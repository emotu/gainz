import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    API_NAME: str = "Gainz Fitness AI Training Assistant"
    API_VERSION: str = "v1.0.0"
    API_AUTHOR: str = "Emotu Balogun"
    OPENAI_API_KEY: str | None = None
    DATABASE_URI: str | None = None
    DATABASE_NAME: str | None = None
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRES_IN_HOURS: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Using lru_cache to prevent settings from getting reinitialized on every call.
@lru_cache
def get_settings():
    _settings = Settings()
    return _settings


# initialize settings so it is available from config
settings = get_settings()
