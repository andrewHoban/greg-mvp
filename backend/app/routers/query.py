"""
Query preparation and execution endpoints
"""

from fastapi import APIRouter

from ..dependencies import SQLExecutorDep
from ..logging import get_logger
from ..models.query_models import (
    NLQueryRequest,
    ProposedQueryResponse,
    ExecuteQueryRequest,
    ExecuteQueryResponse,
)
from ..services.nl_sql_pipeline import NLToSQLPipeline

logger = get_logger(__name__)

router = APIRouter(prefix="/query", tags=["query"])

# Initialize NL-to-SQL pipeline
nl_sql_pipeline = NLToSQLPipeline()


@router.post("/prepare", response_model=ProposedQueryResponse)
async def prepare_query(request: NLQueryRequest) -> ProposedQueryResponse:
    """
    Convert natural language question to SQL query with explanation.
    
    Args:
        request: Natural language query request
        
    Returns:
        Proposed SQL query with explanation and referenced domains
    """
    logger.info(f"Preparing query for question: {request.question}")
    
    # Generate SQL using the NL-to-SQL pipeline
    sql_query, explanation, referenced_domains = nl_sql_pipeline.generate(
        request.question
    )
    
    response = ProposedQueryResponse(
        proposed_sql=sql_query,
        explanation=explanation,
        referenced_domains=referenced_domains
    )
    
    logger.info(f"Query prepared with {len(referenced_domains)} referenced domains")
    
    return response


@router.post("/execute", response_model=ExecuteQueryResponse)
async def execute_query(
    request: ExecuteQueryRequest,
    executor: SQLExecutorDep
) -> ExecuteQueryResponse:
    """
    Execute SQL query and return results.
    
    Args:
        request: SQL execution request with query and limit
        executor: SQL executor dependency
        
    Returns:
        Query results with columns and rows
    """
    logger.info(f"Executing SQL query with limit {request.limit}")
    
    # Execute the query using the SQL executor
    columns, rows, warning = executor.execute(request.sql, request.limit)
    
    response = ExecuteQueryResponse(
        columns=columns,
        rows=rows,
        row_count=len(rows),
        is_mock=True,  # Always true for stub implementation
        warning=warning
    )
    
    logger.info(f"Query executed, returning {len(rows)} rows")
    
    return response