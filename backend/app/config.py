"""
Configuration management using Pydantic BaseSettings.
"""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "Greg MVP"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Okta Configuration (Placeholders)
    okta_domain: Optional[str] = None
    okta_client_id: Optional[str] = None
    okta_client_secret: Optional[str] = None
    okta_redirect_uri: Optional[str] = None
    
    # BigQuery Configuration (Placeholders)
    bigquery_project: Optional[str] = None
    bigquery_credentials_path: Optional[str] = None
    bigquery_dataset: Optional[str] = None
    
    # Database (Future)
    database_url: str = "sqlite:///./greg_mvp.db"
    
    # External APIs (Future)
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()