from fastapi import FastAPI
from backend.app.routers import health, knowledge, query, viz
from backend.app.logging import setup_loguru
from backend.app.dependencies import get_settings

# Setup logging
logger = setup_loguru()

# Create FastAPI app
app = FastAPI(
    title="Greg MVP", 
    version="0.1.0",
    description="MVP FastAPI backend with domain knowledge and NL->SQL stubs"
)

# Include routers
app.include_router(health.router)
app.include_router(knowledge.router) 
app.include_router(query.router)
app.include_router(viz.router)


@app.get("/")
async def root():
    """Root endpoint."""
    settings = get_settings()
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "docs_url": "/docs"
    }