"""Health check router."""

from datetime import UTC, datetime

from fastapi import APIRouter

from backend.app.models import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="ok", version="0.1.0", timestamp=datetime.now(UTC).isoformat()
    )
