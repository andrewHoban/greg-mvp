"""
Dependency injection for FastAPI
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from .config import Settings, settings
from .services.knowledge_base import KnowledgeBase
from .services.sql_executor import SQLExecutor


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached)."""
    return settings


@lru_cache()
def get_knowledge_base() -> KnowledgeBase:
    """Get knowledge base instance (cached)."""
    return KnowledgeBase()


@lru_cache()
def get_sql_executor() -> SQLExecutor:
    """Get SQL executor instance (cached)."""
    return SQLExecutor()


# Type aliases for dependency injection
SettingsDep = Annotated[Settings, Depends(get_settings)]
KnowledgeBaseDep = Annotated[KnowledgeBase, Depends(get_knowledge_base)]
SQLExecutorDep = Annotated[SQLExecutor, Depends(get_sql_executor)]