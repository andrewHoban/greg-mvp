from pydantic import BaseModel
from typing import List, Any

class NLQRequest(BaseModel):
    question: str
    conversation_id: str | None = None

class NLQResponse(BaseModel):
    sql: str
    explanation: str
    conversation_id: str

class SQLRequest(BaseModel):
    sql: str

class SQLResult(BaseModel):
    columns: List[str]
    rows: List[List[Any]]

class PRDRequest(BaseModel):
    title: str
    body: str

class PRDResponse(BaseModel):
    title: str
    body: str
    status: str = "draft"

class KnowledgeDomain(BaseModel):
    name: str
    description: str
    key_fields: list[str]
    notes: str | None = None

class KnowledgeResponse(BaseModel):
    domains: list[KnowledgeDomain]
