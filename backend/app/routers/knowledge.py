from fastapi import APIRouter, Depends
from ..dependencies import get_kb
from ..services.knowledge_base import KnowledgeBase

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

@router.get("/tables")
def list_tables(kb: KnowledgeBase = Depends(get_kb)) -> dict:
    return {"tables": kb.list_tables()}

@router.get("/schema")
def schema(kb: KnowledgeBase = Depends(get_kb)) -> dict:
    return {"schema": kb.describe()}
