from fastapi import APIRouter, Depends
from backend.app.dependencies import get_nl_sql_pipeline, get_sql_executor
from backend.app.services.nl_sql_pipeline import NLToSQLPipeline
from backend.app.services.sql_executor import SQLExecutor
from backend.app.models.query_models import NLQueryRequest, ExecuteQueryRequest, ProposedQueryResponse, ExecuteQueryResponse

router = APIRouter(prefix="/query")


@router.post("/prepare", response_model=ProposedQueryResponse)
async def prepare_query(
    request: NLQueryRequest,
    pipeline: NLToSQLPipeline = Depends(get_nl_sql_pipeline)
):
    """Prepare SQL query from natural language question."""
    result = pipeline.generate(request.question)
    return ProposedQueryResponse(**result)


@router.post("/execute", response_model=ExecuteQueryResponse)
async def execute_query(
    request: ExecuteQueryRequest,
    executor: SQLExecutor = Depends(get_sql_executor)
):
    """Execute SQL query and return results."""
    result = executor.execute(request.sql, request.limit)
    return ExecuteQueryResponse(**result)