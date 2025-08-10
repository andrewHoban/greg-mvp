from fastapi import APIRouter, Depends
from backend.app.dependencies import get_knowledge_base
from backend.app.services.knowledge_base import KnowledgeBase

router = APIRouter(prefix="/knowledge")


@router.get("/domains")
async def list_domains(kb: KnowledgeBase = Depends(get_knowledge_base)):
    """List all available knowledge domains."""
    return kb.list_domains()


@router.get("/domains/{name}")
async def get_domain(name: str, kb: KnowledgeBase = Depends(get_knowledge_base)):
    """Get knowledge domain by name."""
    domain = kb.get_domain(name)
    if domain is None:
        return {"error": f"Domain '{name}' not found"}
    return domain