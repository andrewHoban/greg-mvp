from fastapi import APIRouter, Depends
from ..models.query_models import QueryRequest, QueryResponse
from ..dependencies import get_kb
from ..services.nl_sql_pipeline import NLToSQLPipeline
from ..services.sql_executor import SQLExecutor

router = APIRouter(prefix="/query", tags=["query"])

@router.post("/", response_model=QueryResponse)
def prepare_or_execute(req: QueryRequest, kb=Depends(get_kb)) -> QueryResponse:
    pipeline = NLToSQLPipeline(kb)
    plan = pipeline.build_plan(req.question)
    if req.preview_only:
        return QueryResponse(plan=plan, executed=False)
    rows = SQLExecutor().execute(plan.sql)
    return QueryResponse(plan=plan, executed=True, rows=rows)
