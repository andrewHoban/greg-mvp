from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class NLQueryRequest(BaseModel):
    """Request model for natural language query."""
    question: str = Field(..., description="Natural language question")
    context: Optional[str] = Field(None, description="Additional context for the query")


class ProposedQueryResponse(BaseModel):
    """Response model for proposed SQL query."""
    proposed_sql: str = Field(..., description="Generated SQL query")
    explanation: str = Field(..., description="Explanation of what the query does")
    referenced_domains: List[str] = Field(default=[], description="Domains referenced in the query")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score for the query")


class ExecuteQueryRequest(BaseModel):
    """Request model for executing SQL query."""
    sql: str = Field(..., description="SQL query to execute")
    limit: Optional[int] = Field(100, ge=1, le=1000, description="Maximum number of rows to return")


class ExecuteQueryResponse(BaseModel):
    """Response model for query execution results."""
    rows: List[Dict[str, Any]] = Field(..., description="Query result rows")
    columns: List[str] = Field(..., description="Column names")
    row_count: int = Field(..., description="Number of rows returned")
    execution_time_ms: int = Field(..., description="Query execution time in milliseconds")
    warning: Optional[str] = Field(None, description="Warning message if applicable")


class VisualizationRequest(BaseModel):
    """Request model for visualization suggestions."""
    data: ExecuteQueryResponse = Field(..., description="Query result data to visualize")
    preferred_chart_types: Optional[List[str]] = Field(None, description="Preferred chart types")


class VisualizationSuggestion(BaseModel):
    """Model for a single visualization suggestion."""
    chart_type: str = Field(..., description="Type of chart (bar, line, scatter, etc.)")
    title: str = Field(..., description="Suggested title for the chart")
    description: str = Field(..., description="Description of when to use this chart type")
    recommended: bool = Field(default=False, description="Whether this is the recommended chart type")


class VisualizationResponse(BaseModel):
    """Response model for visualization suggestions."""
    suggestions: List[VisualizationSuggestion] = Field(..., description="List of visualization suggestions")
    sample_figure: Dict[str, Any] = Field(..., description="Sample Plotly figure JSON")
    total_suggestions: int = Field(..., description="Total number of suggestions")


class FieldDoc(BaseModel):
    """Documentation for a database field."""
    name: str = Field(..., description="Field name")
    type: str = Field(..., description="Field data type")
    description: str = Field(..., description="Field description")
    example_values: Optional[List[str]] = Field(None, description="Example values for this field")
    nullable: bool = Field(default=True, description="Whether the field can be null")


class JoinRule(BaseModel):
    """Rule for joining tables."""
    target_table: str = Field(..., description="Target table to join with")
    join_condition: str = Field(..., description="SQL join condition")
    join_type: str = Field(default="INNER", description="Type of join (INNER, LEFT, RIGHT, FULL)")
    description: str = Field(..., description="Description of the relationship")


class KnowledgeDomain(BaseModel):
    """Model for a knowledge domain containing table and field information."""
    name: str = Field(..., description="Domain name")
    description: str = Field(..., description="Domain description")
    tables: Dict[str, Any] = Field(..., description="Tables in this domain")
    common_questions: Optional[List[str]] = Field(None, description="Common questions for this domain")
    caveats: Optional[List[str]] = Field(None, description="Important caveats or limitations")
    sample_queries: Optional[List[str]] = Field(None, description="Sample SQL queries for this domain")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(..., description="Service health status")
    timestamp: Optional[str] = Field(None, description="Response timestamp")
    version: Optional[str] = Field(None, description="Application version")


class AppMetadata(BaseModel):
    """Application metadata response."""
    name: str = Field(..., description="Application name")
    version: str = Field(..., description="Application version")
    description: str = Field(..., description="Application description")
    environment: str = Field(..., description="Current environment")
    features: List[str] = Field(default=[], description="Available features")
