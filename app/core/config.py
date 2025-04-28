from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Глобальные настройки проекта (подтягиваются из .env)."""

    DATABASE_URL: str
    TOKEN: str
    OPENAI_API_KEY: str
    REPLICATE_API_TOKEN: str

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
