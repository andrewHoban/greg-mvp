"""Knowledge base router."""

from fastapi import APIRouter, HTTPException, Request

from backend.app.models import DomainDetailResponse, DomainsListResponse

router = APIRouter()


@router.get("", response_model=DomainsListResponse)
async def list_domains(request: Request) -> DomainsListResponse:
    """List all available knowledge domains."""
    knowledge_base = request.app.state.knowledge_base
    domains = knowledge_base.list_domains()
    return DomainsListResponse(domains=domains)


@router.get("/{domain_name}", response_model=DomainDetailResponse)
async def get_domain_details(
    domain_name: str, request: Request
) -> DomainDetailResponse:
    """Get detailed information about a specific domain."""
    knowledge_base = request.app.state.knowledge_base
    domain = knowledge_base.get_domain(domain_name)

    if not domain:
        raise HTTPException(status_code=404, detail=f"Domain '{domain_name}' not found")

    schema = knowledge_base.get_domain_schema(domain_name)
    return DomainDetailResponse(domain=domain, schema=schema)
