"""
Test the NL-to-SQL pipeline stub functionality.
"""
import pytest

from backend.app.models.query_models import NLQueryRequest
from backend.app.services.knowledge_base import KnowledgeBase
from backend.app.services.nl_sql_pipeline import NLSQLPipeline


@pytest.fixture
def knowledge_base():
    """Create knowledge base fixture."""
    return KnowledgeBase()


@pytest.fixture
def pipeline(knowledge_base):
    """Create NL-SQL pipeline fixture."""
    return NLSQLPipeline(knowledge_base)


@pytest.mark.asyncio
async def test_pipeline_generates_finance_query(pipeline):
    """Test that financial queries generate appropriate SQL."""
    request = NLQueryRequest(question="Show total revenue by month")
    
    result = await pipeline.generate_sql(request)
    
    assert result.sql is not None
    assert len(result.sql) > 0
    assert "revenue" in result.sql.lower() or "amount" in result.sql.lower()
    assert result.explanation is not None
    assert len(result.tables_used) > 0
    assert "transactions" in result.tables_used or "subscriptions" in result.tables_used
    assert "This is a stub implementation" in result.warnings[0]


@pytest.mark.asyncio
async def test_pipeline_generates_reads_query(pipeline):
    """Test that reading queries generate appropriate SQL."""
    request = NLQueryRequest(question="What are the most popular articles?")
    
    result = await pipeline.generate_sql(request)
    
    assert result.sql is not None
    assert "read" in result.sql.lower() or "article" in result.sql.lower()
    assert result.explanation is not None
    assert "articles" in result.tables_used or "user_reads" in result.tables_used


@pytest.mark.asyncio
async def test_pipeline_generates_support_query(pipeline):
    """Test that support queries generate appropriate SQL."""
    request = NLQueryRequest(question="Show ticket resolution times by category")
    
    result = await pipeline.generate_sql(request)
    
    assert result.sql is not None
    assert "ticket" in result.sql.lower() or "support" in result.sql.lower()
    assert result.explanation is not None
    assert "support_tickets" in result.tables_used


@pytest.mark.asyncio
async def test_pipeline_generates_default_query(pipeline):
    """Test that unrecognized queries generate default response."""
    request = NLQueryRequest(question="Some random question about nothing specific")
    
    result = await pipeline.generate_sql(request)
    
    assert result.sql is not None
    assert result.explanation is not None
    assert "default" in result.explanation.lower()
    assert "Could not detect specific domain" in result.warnings[1]