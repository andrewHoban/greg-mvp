"""
Knowledge domain endpoints for accessing domain dataset knowledge.
"""
from typing import Dict, List
from fastapi import APIRouter, Depends

from ..dependencies import get_knowledge_base, get_current_user
from ..models.query_models import KnowledgeDomain
from ..services.knowledge_base import KnowledgeBase

router = APIRouter()


@router.get("/domains", response_model=List[str])
async def list_domains(
    knowledge_base: KnowledgeBase = Depends(get_knowledge_base),
    current_user: str = Depends(get_current_user)
) -> List[str]:
    """Get list of available knowledge domains."""
    return knowledge_base.get_available_domains()


@router.get("/domains/{domain_name}", response_model=KnowledgeDomain)
async def get_domain_knowledge(
    domain_name: str,
    knowledge_base: KnowledgeBase = Depends(get_knowledge_base),
    current_user: str = Depends(get_current_user)
) -> KnowledgeDomain:
    """Get detailed knowledge for a specific domain."""
    return knowledge_base.get_domain(domain_name)


@router.get("/schema-context")
async def get_schema_context(
    knowledge_base: KnowledgeBase = Depends(get_knowledge_base),
    current_user: str = Depends(get_current_user)
) -> Dict[str, str]:
    """Get formatted schema context for all domains."""
    return {
        "schema_context": knowledge_base.get_schema_context()
    }