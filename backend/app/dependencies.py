from functools import lru_cache
from backend.app.config import AppSettings
from backend.app.services.knowledge_base import KnowledgeBase
from backend.app.services.sql_executor import SQLExecutor
from backend.app.services.nl_sql_pipeline import NLToSQLPipeline


@lru_cache()
def get_settings():
    """Get cached application settings."""
    return AppSettings()


# Singletons for services
@lru_cache()
def get_knowledge_base():
    """Get cached knowledge base instance."""
    return KnowledgeBase()


@lru_cache()
def get_sql_executor():
    """Get cached SQL executor instance."""
    return SQLExecutor()


@lru_cache()
def get_nl_sql_pipeline():
    """Get cached NL-to-SQL pipeline instance."""
    return NLToSQLPipeline()