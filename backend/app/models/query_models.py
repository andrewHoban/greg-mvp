from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str = Field(..., examples=["Show me total sales by month for 2024"])
    preview_only: bool = False

class QueryPlan(BaseModel):
    tables: List[str]
    filters: List[str]
    group_by: List[str]
    metrics: List[str]
    sql: str

class QueryResponse(BaseModel):
    plan: QueryPlan
    executed: bool
    rows: Optional[list[dict]] = None

class VisualizationSuggestion(BaseModel):
    title: str
    chart_type: str
    x: str
    y: List[str]

class VisualizationSuggestions(BaseModel):
    suggestions: List[VisualizationSuggestion]
