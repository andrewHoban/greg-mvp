"""
Health check endpoint.
"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str = "0.1.0"


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="ok")