"""Application settings (pydantic-settings)."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Collector/API settings."""

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env", "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database (varsayılan: docker-compose'taki postgres — user regtech)
    database_url: str = "postgresql://regtech:regtech@localhost:5432/regtechradar"
    redis_url: str = "redis://localhost:6379/0"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Crawler
    crawler_user_agent: str = "RegTechRadar/1.0 (+https://regtechradar.com/bot)"
    crawler_respect_robots_txt: bool = True
    crawler_max_concurrent: int = 3
    crawler_request_delay_ms: int = 2000


settings = Settings()
