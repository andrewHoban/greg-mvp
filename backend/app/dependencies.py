"""
Common dependency injection for FastAPI endpoints.
"""
from functools import lru_cache
from typing import Optional

from fastapi import Header, HTTPException

from .config import Settings, get_settings
from .services.knowledge_base import KnowledgeBase


@lru_cache()
def get_knowledge_base() -> KnowledgeBase:
    """Get cached knowledge base instance."""
    return KnowledgeBase()


def get_bigquery_client():
    """
    Get BigQuery client instance.
    
    Currently returns None as a placeholder.
    In the future, this will return an authenticated BigQuery client.
    """
    # TODO: Implement actual BigQuery client creation
    # from google.cloud import bigquery
    # settings = get_settings()
    # if settings.bigquery_credentials_path:
    #     return bigquery.Client.from_service_account_json(
    #         settings.bigquery_credentials_path,
    #         project=settings.bigquery_project
    #     )
    return None


def get_current_user(x_user_email: Optional[str] = Header(None)) -> str:
    """
    Get current user from authentication.
    
    This is a placeholder implementation that falls back to a demo user.
    In production, this should validate Okta tokens and extract user info.
    """
    # TODO: Implement actual Okta token validation
    # For now, use header fallback or demo user
    if x_user_email:
        return x_user_email
    return "demo@example.com"