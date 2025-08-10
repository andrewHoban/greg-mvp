"""
Configuration management using Pydantic Settings
"""

from typing import Optional

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # BigQuery settings
    bigquery_project: str = Field(default="your-gcp-project", description="GCP project ID")
    
    # OKTA authentication settings (placeholder for future use)
    okta_issuer_url: str = Field(
        default="https://your-okta-domain/oauth2/default",
        description="OKTA issuer URL"
    )
    okta_audience: str = Field(
        default="api://default", 
        description="OKTA audience"
    )
    
    # Application environment
    app_env: str = Field(default="dev", description="Application environment")
    
    # API settings
    api_host: str = Field(default="127.0.0.1", description="API host")
    api_port: int = Field(default=8000, description="API port")
    
    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")


# Global settings instance
settings = Settings()