"""Health endpoint router."""

from datetime import datetime

from fastapi import APIRouter

from backend.app.models import HealthResponse, HealthStatus

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status=HealthStatus.HEALTHY,
        timestamp=datetime.now(),
        version="0.1.0",
        services={
            "database": "healthy",
            "ai_service": "healthy",
        },
    )
