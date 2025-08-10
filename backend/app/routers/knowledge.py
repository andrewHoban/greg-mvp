"""
Knowledge base endpoints for domain information
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException

from ..dependencies import KnowledgeBaseDep
from ..logging import get_logger
from ..models.query_models import KnowledgeDomain

logger = get_logger(__name__)

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("/domains", response_model=List[str])
async def list_domains(kb: KnowledgeBaseDep) -> List[str]:
    """
    Get list of all available knowledge domain names.
    
    Returns:
        List of domain names
    """
    logger.info("Listing all knowledge domains")
    
    domain_names = kb.get_domain_names()
    
    logger.info(f"Returning {len(domain_names)} domains")
    
    return domain_names


@router.get("/domains/{domain_name}", response_model=KnowledgeDomain)
async def get_domain(domain_name: str, kb: KnowledgeBaseDep) -> KnowledgeDomain:
    """
    Get full documentation for a specific knowledge domain.
    
    Args:
        domain_name: Name of the domain to retrieve
        
    Returns:
        Complete domain documentation including tables, joins, and caveats
        
    Raises:
        HTTPException: If domain is not found
    """
    logger.info(f"Retrieving domain: {domain_name}")
    
    domain = kb.get_domain(domain_name)
    
    if domain is None:
        logger.warning(f"Domain not found: {domain_name}")
        raise HTTPException(
            status_code=404,
            detail=f"Domain '{domain_name}' not found"
        )
    
    logger.info(f"Returning domain {domain_name} with {len(domain.tables)} tables")
    
    return domain


@router.get("/search/tables")
async def search_tables(q: str, kb: KnowledgeBaseDep) -> List[str]:
    """
    Search for tables across all domains.
    
    Args:
        q: Search query string
        
    Returns:
        List of matching table names in format "domain.table"
    """
    logger.info(f"Searching tables with query: {q}")
    
    results = kb.search_tables(q)
    
    logger.info(f"Found {len(results)} matching tables")
    
    return results