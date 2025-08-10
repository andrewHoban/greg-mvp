"""Application configuration settings."""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    app_name: str = "AI Product Manager Assistant"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # API Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # External API Keys
    gemini_api_key: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()