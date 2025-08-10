from fastapi import APIRouter, Depends

from backend.app.dependencies import get_pipeline, get_sql_executor
from backend.app.models.query_models import (
    ExecuteQueryRequest,
    ExecuteQueryResponse,
    NLQueryRequest,
    ProposedQueryResponse,
)
from backend.app.services.nl_sql_pipeline import NLToSQLPipeline
from backend.app.services.sql_executor import SQLExecutor

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/prepare", response_model=ProposedQueryResponse)
async def prepare_query(
    request: NLQueryRequest,
    pipeline: NLToSQLPipeline = Depends(get_pipeline)
) -> ProposedQueryResponse:
    """
    Convert natural language question to SQL query.
    
    This endpoint takes a natural language question and returns a proposed
    SQL query along with an explanation of what the query will do.
    """
    result = pipeline.generate(request.question)

    return ProposedQueryResponse(
        proposed_sql=result["proposed_sql"],
        explanation=result["explanation"],
        referenced_domains=result["referenced_domains"],
        confidence_score=result["confidence_score"]
    )


@router.post("/execute", response_model=ExecuteQueryResponse)
async def execute_query(
    request: ExecuteQueryRequest,
    executor: SQLExecutor = Depends(get_sql_executor)
) -> ExecuteQueryResponse:
    """
    Execute SQL query and return results.
    
    This endpoint executes the provided SQL query and returns the results
    along with metadata about the execution.
    """
    result = executor.execute(request.sql, request.limit)

    return ExecuteQueryResponse(
        rows=result["rows"],
        columns=result["columns"],
        row_count=result["row_count"],
        execution_time_ms=result["execution_time_ms"],
        warning=result.get("warning")
    )
