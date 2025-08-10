from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application settings using Pydantic BaseSettings for environment variable management."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = Field(default="Greg MVP", description="Application name")
    app_env: str = Field(default="dev", description="Application environment")
    bigquery_project: Optional[str] = Field(
        default=None, description="Google Cloud BigQuery project ID"
    )
    okta_issuer_url: Optional[str] = Field(
        default=None, description="Okta issuer URL for authentication"
    )
    okta_audience: Optional[str] = Field(
        default=None, description="Okta audience for token validation"
    )
    app_log_level: str = Field(default="INFO", description="Application log level")


@lru_cache
def get_settings() -> AppSettings:
    """Get cached application settings."""
    return AppSettings()
