"""
FastAPI application entry point for Greg MVP.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .logging import setup_logging
from .routers import health, knowledge, query, viz


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    setup_logging()
    yield
    # Shutdown - cleanup if needed


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Internal data exploration and knowledge platform MVP",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health.router, tags=["Health"])
    app.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge"])
    app.include_router(query.router, prefix="/query", tags=["Query"])
    app.include_router(viz.router, prefix="/viz", tags=["Visualization"])
    
    return app


# Create the app instance
app = create_app()