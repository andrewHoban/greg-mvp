from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """System health monitoring endpoint."""
    return {"status": "ok"}