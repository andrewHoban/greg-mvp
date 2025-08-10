"""Main FastAPI application entry point."""

import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from backend.app.routers import health, knowledge, query, viz
from backend.app.services.knowledge_base import KnowledgeBase


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Greg MVP FastAPI application")

    # Initialize knowledge base
    knowledge_base = KnowledgeBase()
    knowledge_base.load_domains()
    app.state.knowledge_base = knowledge_base

    logger.info("Application startup complete")
    yield

    # Shutdown
    logger.info("Shutting down Greg MVP FastAPI application")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Greg MVP - AI Product Manager Assistant",
        description="FastAPI backend for natural language to SQL queries and data visualization",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Configure properly for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
    app.include_router(query.router, prefix="/query", tags=["query"])
    app.include_router(viz.router, prefix="/viz", tags=["visualization"])

    # Configure logging
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
    )

    return app


# Create the app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
