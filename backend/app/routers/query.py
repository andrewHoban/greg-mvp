"""Query processing router."""

from fastapi import APIRouter, Request
from loguru import logger

from backend.app.models import (
    QueryExecuteRequest,
    QueryExecuteResponse,
    QueryPrepareRequest,
    QueryPrepareResponse,
)
from backend.app.services.nl_to_sql import NLToSQLService
from backend.app.services.sql_executor import SQLExecutorService

router = APIRouter()


@router.post("/prepare", response_model=QueryPrepareResponse)
async def prepare_query(
    request_data: QueryPrepareRequest, request: Request
) -> QueryPrepareResponse:
    """
    Convert natural language question to SQL query.

    This endpoint analyzes the natural language question and returns a proposed SQL query,
    explanation, and referenced knowledge domains.
    """
    logger.info(f"Preparing query for question: {request_data.question}")

    # Get knowledge base from app state
    knowledge_base = request.app.state.knowledge_base

    # Use NL to SQL service to generate query
    nl_to_sql_service = NLToSQLService(knowledge_base)
    result = nl_to_sql_service.process_question(request_data.question)

    logger.info(f"Generated SQL: {result.proposed_sql}")

    return QueryPrepareResponse(
        proposed_sql=result.proposed_sql,
        explanation=result.explanation,
        referenced_domains=result.referenced_domains,
    )


@router.post("/execute", response_model=QueryExecuteResponse)
async def execute_query(request_data: QueryExecuteRequest) -> QueryExecuteResponse:
    """
    Execute SQL query and return results.

    This is a stub implementation that returns synthetic data.
    In production, this would execute against the actual database.
    """
    logger.info(f"Executing SQL query with limit {request_data.limit}")
    logger.info(f"SQL: {request_data.sql}")

    # Use SQL executor service to run query
    sql_executor = SQLExecutorService()
    result = sql_executor.execute_query(request_data.sql, request_data.limit)

    return QueryExecuteResponse(
        data=result.data, row_count=len(result.data), warning=result.warning
    )
