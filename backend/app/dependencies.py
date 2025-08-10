from functools import lru_cache

from backend.app.config import AppSettings
from backend.app.services.knowledge_base import KnowledgeBase
from backend.app.services.nl_sql_pipeline import NLToSQLPipeline
from backend.app.services.sql_executor import SQLExecutor


@lru_cache
def get_settings() -> AppSettings:
    """Get cached application settings."""
    from backend.app.config import get_settings
    return get_settings()


@lru_cache
def get_knowledge_base() -> KnowledgeBase:
    """Get cached knowledge base instance."""
    return KnowledgeBase()


@lru_cache
def get_sql_executor() -> SQLExecutor:
    """Get cached SQL executor instance."""
    return SQLExecutor()


@lru_cache
def get_pipeline() -> NLToSQLPipeline:
    """Get cached NL to SQL pipeline instance."""
    return NLToSQLPipeline()
