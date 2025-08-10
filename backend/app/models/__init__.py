"""Pydantic models for API requests and responses."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Application status")
    version: str = Field(..., description="Application version")
    timestamp: str = Field(..., description="Current timestamp")


class QueryPrepareRequest(BaseModel):
    """Request model for query preparation."""

    question: str = Field(..., description="Natural language question", min_length=1)


class QueryPrepareResponse(BaseModel):
    """Response model for query preparation."""

    proposed_sql: str = Field(..., description="Generated SQL query")
    explanation: str = Field(..., description="Explanation of the query logic")
    referenced_domains: list[str] = Field(
        default_factory=list, description="Domain knowledge areas referenced"
    )


class QueryExecuteRequest(BaseModel):
    """Request model for query execution."""

    sql: str = Field(..., description="SQL query to execute", min_length=1)
    limit: int | None = Field(
        default=100, description="Maximum number of rows to return", ge=1, le=1000
    )


class QueryExecuteResponse(BaseModel):
    """Response model for query execution."""

    data: list[dict[str, Any]] = Field(
        default_factory=list, description="Query result rows"
    )
    row_count: int = Field(..., description="Number of rows returned")
    warning: str | None = Field(None, description="Warning message if applicable")


class DomainInfo(BaseModel):
    """Domain information model."""

    name: str = Field(..., description="Domain name")
    description: str = Field(..., description="Domain description")
    tables: list[str] = Field(
        default_factory=list, description="Available tables in this domain"
    )
    sample_questions: list[str] = Field(
        default_factory=list, description="Sample questions for this domain"
    )


class DomainsListResponse(BaseModel):
    """Response model for domains list."""

    domains: list[DomainInfo] = Field(
        default_factory=list, description="Available knowledge domains"
    )


class DomainDetailResponse(BaseModel):
    """Response model for domain details."""

    domain: DomainInfo = Field(..., description="Domain information")
    domain_schema: dict[str, Any] = Field(
        default_factory=dict, description="Detailed schema information", alias="schema"
    )


class VisualizationRequest(BaseModel):
    """Request model for visualization suggestions."""

    sql: str = Field(..., description="SQL query to analyze")
    data_sample: list[dict[str, Any]] | None = Field(
        None, description="Optional sample data"
    )


class ChartRecommendation(BaseModel):
    """Chart recommendation model."""

    chart_type: str = Field(..., description="Recommended chart type")
    reasoning: str = Field(..., description="Why this chart type is recommended")
    priority: int = Field(..., description="Priority ranking (1 = highest)")


class VisualizationResponse(BaseModel):
    """Response model for visualization suggestions."""

    recommendations: list[ChartRecommendation] = Field(
        default_factory=list, description="Chart type recommendations"
    )
    plotly_config: dict[str, Any] = Field(
        default_factory=dict, description="Sample Plotly configuration"
    )
