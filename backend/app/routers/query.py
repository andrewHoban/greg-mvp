"""
Query endpoints for natural language to SQL pipeline.
"""
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from ..dependencies import get_knowledge_base, get_bigquery_client, get_current_user
from ..models.query_models import (
    NLQueryRequest, 
    ProposedQuery, 
    ExecutedQueryResult
)
from ..services.knowledge_base import KnowledgeBase
from ..services.nl_sql_pipeline import NLSQLPipeline
from ..services.sql_executor import SQLExecutor

router = APIRouter()


@router.post("/prepare", response_model=ProposedQuery)
async def prepare_query(
    request: NLQueryRequest,
    knowledge_base: KnowledgeBase = Depends(get_knowledge_base),
    current_user: str = Depends(get_current_user)
) -> ProposedQuery:
    """
    Convert natural language question to structured SQL with explanation.
    
    This endpoint does NOT execute the query, only prepares it for review.
    """
    try:
        logger.info(f"Preparing query for user {current_user}: {request.question}")
        
        # Initialize NL-to-SQL pipeline
        pipeline = NLSQLPipeline(knowledge_base)
        
        # Generate proposed query
        proposed_query = await pipeline.generate_sql(request)
        
        logger.info(f"Generated SQL query with {len(proposed_query.tables_used)} tables")
        
        return proposed_query
        
    except Exception as e:
        logger.error(f"Error preparing query: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to prepare query: {str(e)}"
        )


@router.post("/execute", response_model=ExecutedQueryResult)
async def execute_query(
    proposed_query: ProposedQuery,
    dry_run: bool = False,
    bigquery_client = Depends(get_bigquery_client),
    current_user: str = Depends(get_current_user)
) -> ExecutedQueryResult:
    """
    Execute a previously approved SQL query.
    
    Currently returns mock data with synthetic response.
    The real BigQuery integration will be implemented here in the future.
    """
    try:
        logger.info(f"Executing query for user {current_user} (dry_run={dry_run})")
        
        # Initialize SQL executor
        executor = SQLExecutor(bigquery_client)
        
        # Execute the query (currently stubbed)
        result = await executor.execute_query(
            proposed_query.sql, 
            dry_run=dry_run
        )
        
        logger.info(f"Query execution completed: {result.row_count} rows returned")
        
        return result
        
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to execute query: {str(e)}"
        )