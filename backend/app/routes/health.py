"""Health check and utility routes."""
from fastapi import APIRouter


router = APIRouter()


@router.get("/ping")
async def health_check():
    """Health check endpoint for smoke testing."""
    return {"pong": True}