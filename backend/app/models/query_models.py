from pydantic import BaseModel
from typing import List, Dict, Any, Optional


# Request Models
class NLQueryRequest(BaseModel):
    question: str


class ExecuteQueryRequest(BaseModel):
    sql: str
    limit: int = 100


class VisualizationRequest(BaseModel):
    fields: List[str]


# Response Models  
class ProposedQueryResponse(BaseModel):
    proposed_sql: str
    explanation: str
    referenced_domains: List[str]


class ExecuteQueryResponse(BaseModel):
    columns: List[str]
    rows: List[List[Any]]
    warning: Optional[str] = None


class VisualizationSuggestion(BaseModel):
    chart_types: List[str]
    figure: Dict[str, Any]


# Knowledge Domain Models
class FieldDoc(BaseModel):
    name: str
    type: str
    description: str
    semantic_role: Optional[str] = None


class JoinRule(BaseModel):
    table: str
    condition: str
    type: str = "INNER"


class KnowledgeDomain(BaseModel):
    name: str
    description: str
    tables: Dict[str, List[FieldDoc]]
    joins: List[JoinRule]
    caveats: List[str]
    sample_questions: List[str]