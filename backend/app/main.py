"""
FastAPI main application
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .logging import configure_logging, get_logger
from .routers import health, knowledge, query, viz


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    configure_logging()
    logger = get_logger(__name__)
    logger.info("Starting Greg MVP Backend API")
    logger.info(f"Environment: {settings.app_env}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Greg MVP Backend API")


# Create FastAPI application
app = FastAPI(
    title="Greg MVP - AI Product Manager Assistant",
    description="Backend API for natural language query processing and data visualization",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(knowledge.router)
app.include_router(query.router)
app.include_router(viz.router)


@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {
        "message": "Greg MVP - AI Product Manager Assistant API",
        "version": "0.1.0",
        "docs_url": "/docs",
        "health_url": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )