"""Main FastAPI application for Greg MVP."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import health, knowledge, query, visualization

app = FastAPI(
    title="Greg MVP - AI Product Manager Assistant",
    description="AI-powered assistant for product managers to query data",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(knowledge.router, prefix="/api", tags=["knowledge"])
app.include_router(query.router, prefix="/api", tags=["query"])
app.include_router(visualization.router, prefix="/api", tags=["visualization"])


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Greg MVP - AI Product Manager Assistant"}
