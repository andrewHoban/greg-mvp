"""
Pydantic models for API requests and responses
"""

from typing import List, Optional, Any, Dict

from pydantic import BaseModel, Field


# Query-related models
class NLQueryRequest(BaseModel):
    """Natural language query request."""
    question: str = Field(..., description="Natural language question", min_length=1)


class ProposedQueryResponse(BaseModel):
    """Response for prepared query."""
    proposed_sql: str = Field(..., description="Generated SQL query")
    explanation: str = Field(..., description="Human-readable explanation")
    referenced_domains: List[str] = Field(..., description="List of domain names referenced")


class ExecuteQueryRequest(BaseModel):
    """Request to execute SQL query."""
    sql: str = Field(..., description="SQL query to execute")
    limit: int = Field(default=100, description="Maximum number of rows to return", ge=1, le=1000)


class ExecuteQueryResponse(BaseModel):
    """Response from query execution."""
    columns: List[str] = Field(..., description="Column names")
    rows: List[List[Any]] = Field(..., description="Query result rows")
    row_count: int = Field(..., description="Number of rows returned")
    is_mock: bool = Field(default=True, description="Whether this is mock/synthetic data")
    warning: Optional[str] = Field(None, description="Warning message if applicable")


# Visualization models
class FieldMetadata(BaseModel):
    """Metadata about a data field."""
    name: str = Field(..., description="Field name")
    type: str = Field(..., description="Data type (e.g., STRING, NUMERIC, DATE)")
    semantic_role: Optional[str] = Field(None, description="Semantic role (key, metric, dimension)")


class VisualizationRequest(BaseModel):
    """Request for visualization suggestions."""
    fields: List[FieldMetadata] = Field(..., description="Field metadata for the dataset")
    context: Optional[str] = Field(None, description="Additional context about the data")


class ChartSpec(BaseModel):
    """Simple Plotly chart specification."""
    chart_type: str = Field(..., description="Chart type (bar, line, pie, scatter, etc.)")
    x_axis: Optional[str] = Field(None, description="X-axis field name")
    y_axis: Optional[str] = Field(None, description="Y-axis field name")
    color: Optional[str] = Field(None, description="Color grouping field")
    config: Dict[str, Any] = Field(default_factory=dict, description="Additional chart configuration")


class VisualizationSuggestion(BaseModel):
    """Visualization suggestion response."""
    suggestions: List[ChartSpec] = Field(..., description="List of suggested chart configurations")
    reasoning: str = Field(..., description="Explanation for the suggestions")


# Knowledge base models
class FieldDoc(BaseModel):
    """Documentation for a database field."""
    name: str = Field(..., description="Field name")
    type: str = Field(..., description="Data type")
    description: str = Field(..., description="Field description")
    semantic_role: Optional[str] = Field(None, description="Semantic role (key, metric, dimension)")


class TableDoc(BaseModel):
    """Documentation for a database table."""
    name: str = Field(..., description="Table name")
    description: str = Field(..., description="Table description")
    fields: List[FieldDoc] = Field(..., description="List of fields in the table")


class JoinRule(BaseModel):
    """Documentation for table joins."""
    target: str = Field(..., description="Target table name")
    condition: str = Field(..., description="Join condition")
    type: str = Field(..., description="Join type (left, inner, right, etc.)")
    description: str = Field(..., description="Human-readable join description")


class KnowledgeDomain(BaseModel):
    """Knowledge domain containing tables, joins, and documentation."""
    name: str = Field(..., description="Domain name")
    description: str = Field(..., description="Domain description")
    tables: List[TableDoc] = Field(..., description="Tables in this domain")
    joins: List[JoinRule] = Field(default_factory=list, description="Join rules between tables")
    caveats: List[str] = Field(default_factory=list, description="Important caveats or limitations")
    sample_questions: List[str] = Field(default_factory=list, description="Sample questions for this domain")