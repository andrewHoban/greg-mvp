"""
Pydantic models for query operations and responses.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class NLQueryRequest(BaseModel):
    """Request model for natural language query."""
    question: str = Field(..., description="Natural language question")
    context: Optional[str] = Field(None, description="Additional context for the query")


class ProposedQuery(BaseModel):
    """Model for a proposed SQL query before execution."""
    sql: str = Field(..., description="Generated SQL query")
    explanation: str = Field(..., description="Human-readable explanation of the query")
    tables_used: List[str] = Field(default_factory=list, description="Tables referenced in the query")
    estimated_cost: Optional[str] = Field(None, description="Estimated query cost")
    warnings: List[str] = Field(default_factory=list, description="Any warnings about the query")


class ExecutedQueryResult(BaseModel):
    """Model for executed query results."""
    columns: List[str] = Field(..., description="Column names in the result set")
    rows: List[List[Any]] = Field(..., description="Result rows")
    row_count: int = Field(..., description="Number of rows returned")
    execution_time_ms: float = Field(..., description="Query execution time in milliseconds")
    bytes_processed: Optional[int] = Field(None, description="Bytes processed by the query")


class VisualizationRequest(BaseModel):
    """Request model for visualization suggestions."""
    data_summary: Dict[str, Any] = Field(..., description="Summary of the data to visualize")
    chart_types: Optional[List[str]] = Field(None, description="Preferred chart types")


class ChartSpec(BaseModel):
    """Plotly chart specification."""
    type: str = Field(..., description="Chart type (bar, scatter, line, etc.)")
    title: str = Field(..., description="Chart title")
    x_axis: str = Field(..., description="X-axis field")
    y_axis: str = Field(..., description="Y-axis field")
    config: Dict[str, Any] = Field(default_factory=dict, description="Additional chart configuration")


class VisualizationSpec(BaseModel):
    """Visualization specification response."""
    suggested_charts: List[str] = Field(..., description="Suggested chart types")
    plotly_spec: Optional[Dict[str, Any]] = Field(None, description="Plotly figure specification")
    reasoning: str = Field(..., description="Reasoning for chart suggestions")


class FieldDoc(BaseModel):
    """Documentation for a database field."""
    name: str = Field(..., description="Field name")
    type: str = Field(..., description="Data type")
    description: str = Field(..., description="Field description")
    semantic_role: Optional[str] = Field(None, description="Semantic role (dimension, metric, etc.)")
    sample_values: Optional[List[str]] = Field(None, description="Sample values")


class JoinRule(BaseModel):
    """Join rule between tables."""
    left_table: str = Field(..., description="Left table name")
    right_table: str = Field(..., description="Right table name")
    join_condition: str = Field(..., description="Join condition")
    join_type: str = Field(default="INNER", description="Type of join")


class KnowledgeDomain(BaseModel):
    """Domain knowledge structure."""
    domain: str = Field(..., description="Domain name")
    description: str = Field(..., description="Domain description")
    tables: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Table schemas")
    joins: List[JoinRule] = Field(default_factory=list, description="Available joins")
    business_rules: List[str] = Field(default_factory=list, description="Business rules and caveats")
    sample_questions: List[str] = Field(default_factory=list, description="Sample questions for this domain")