from typing import List

from fastapi import APIRouter, Depends, HTTPException

from backend.app.dependencies import get_knowledge_base
from backend.app.services.knowledge_base import KnowledgeBase

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])


@router.get("/domains", response_model=List[str])
async def list_domains(
    kb: KnowledgeBase = Depends(get_knowledge_base)
) -> List[str]:
    """Get list of available knowledge domains."""
    return kb.list_domains()


@router.get("/domains/{domain_name}")
async def get_domain(
    domain_name: str,
    kb: KnowledgeBase = Depends(get_knowledge_base)
) -> dict:
    """Get detailed information about a specific knowledge domain."""
    domain_data = kb.get_domain(domain_name)

    if domain_data is None:
        raise HTTPException(
            status_code=404,
            detail=f"Domain '{domain_name}' not found"
        )

    return domain_data
