"""Pydantic models for the Greg MVP application."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class HealthStatus(str, Enum):
    """Health status enumeration."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthResponse(BaseModel):
    """Health endpoint response model."""

    status: HealthStatus
    timestamp: datetime
    version: str
    services: dict[str, str] = Field(default_factory=dict)


class QueryRequest(BaseModel):
    """Query request model."""

    question: str = Field(..., description="Natural language question", min_length=1)
    context: dict[str, Any] | None = Field(None, description="Additional context")


class QueryResponse(BaseModel):
    """Query response model."""

    sql: str = Field(..., description="Generated SQL query")
    explanation: str = Field(..., description="Human-readable explanation")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    suggested_visualizations: list[str] = Field(default_factory=list)


class KnowledgeItem(BaseModel):
    """Knowledge base item model."""

    id: str
    title: str
    content: str
    category: str
    tags: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class KnowledgeResponse(BaseModel):
    """Knowledge endpoint response model."""

    items: list[KnowledgeItem]
    total: int
    page: int
    per_page: int


class VisualizationRequest(BaseModel):
    """Visualization suggestion request model."""

    query: str = Field(..., description="SQL query or natural language description")
    data_preview: list[dict[str, Any]] | None = Field(None, description="Sample data")


class VisualizationType(str, Enum):
    """Visualization type enumeration."""

    BAR_CHART = "bar_chart"
    LINE_CHART = "line_chart"
    PIE_CHART = "pie_chart"
    SCATTER_PLOT = "scatter_plot"
    TABLE = "table"
    HEAT_MAP = "heat_map"


class VisualizationSuggestion(BaseModel):
    """Visualization suggestion model."""

    type: VisualizationType
    title: str
    description: str
    config: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(..., ge=0.0, le=1.0)


class VisualizationResponse(BaseModel):
    """Visualization suggestions response model."""

    suggestions: list[VisualizationSuggestion]
