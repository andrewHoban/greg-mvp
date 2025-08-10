from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_env: str = "dev"
    llm_provider: str = "mock"
    llm_api_key: str | None = None
    bigquery_project: str | None = None
    bigquery_use_mock: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
