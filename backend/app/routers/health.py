from fastapi import APIRouter
from ..version import APP_NAME, APP_VERSION

router = APIRouter(tags=["health"])

@router.get("/health")
def health() -> dict:
    return {"status": "ok", "app": APP_NAME, "version": APP_VERSION}
