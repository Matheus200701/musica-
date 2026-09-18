from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    discord_token: str = Field(alias="DISCORD_TOKEN")
    database_path: str = Field(default="data/music.db", alias="DATABASE_PATH")
    default_volume: int = Field(default=70, alias="DEFAULT_VOLUME", ge=1, le=100)
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

@lru_cache
def get_settings() -> Settings:
    return Settings()
