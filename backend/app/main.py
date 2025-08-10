from fastapi import Depends, FastAPI

from backend.app.config import AppSettings, get_settings
from backend.app.logging import configure_logging
from backend.app.models.query_models import AppMetadata
from backend.app.routers import health, knowledge, query, viz

# Configure logging
configure_logging()

# Create FastAPI application
app = FastAPI(
    title="Greg MVP - AI Product Manager Assistant",
    description="FastAPI backend for AI-powered product management queries",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(health.router)
app.include_router(knowledge.router)
app.include_router(query.router)
app.include_router(viz.router)


@app.get("/", response_model=AppMetadata)
async def root(settings: AppSettings = Depends(get_settings)) -> AppMetadata:
    """Root endpoint that returns application metadata."""
    return AppMetadata(
        name=settings.app_name,
        version="0.1.0",
        description="AI Product Manager Assistant - FastAPI Backend",
        environment=settings.app_env,
        features=[
            "Natural Language to SQL conversion",
            "SQL query execution (mock data)",
            "Knowledge base management",
            "Visualization suggestions",
            "Health monitoring"
        ]
    )


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    settings = get_settings()
    print(f"🚀 Starting {settings.app_name} in {settings.app_env} environment")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    print("👋 Shutting down Greg MVP")
