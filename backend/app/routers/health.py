"""
Health check endpoint
"""

from fastapi import APIRouter

from ..logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check() -> dict:
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Status information
    """
    logger.info("Health check requested")
    
    return {
        "status": "ok",
        "service": "greg-mvp-backend",
        "version": "0.1.0"
    }