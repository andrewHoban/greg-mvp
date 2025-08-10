from datetime import datetime

from fastapi import APIRouter

from backend.app.models.query_models import HealthResponse

router = APIRouter(prefix="", tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint to verify the service is running."""
    return HealthResponse(
        status="ok",
        timestamp=datetime.utcnow().isoformat(),
        version="0.1.0"
    )
