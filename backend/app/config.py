"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./regtech.db"

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Resend (Email)
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "RegTech Radar <noreply@regtechradar.com>"

    # JWT Auth
    JWT_SECRET: str = "change-me-to-a-random-string"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080  # 7 days

    # App
    APP_URL: str = "http://localhost:3000"
    ENV: str = "development"

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
