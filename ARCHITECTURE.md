# Architecture Overview

This document describes the system architecture for the Greg MVP - AI Product Manager Assistant backend.

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Data Layer    │
│   Client        │────│   Backend       │────│   (Future)      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                       ┌───────┴───────┐
                       │               │
                  ┌────▼────┐    ┌────▼────┐
                  │ Stub    │    │ YAML    │
                  │ Services│    │ Knowledge│
                  │         │    │ Base    │
                  └─────────┘    └─────────┘
```

## Layer Architecture

### 1. API Layer (`backend/app/routers/`)

FastAPI routers that define HTTP endpoints and handle request/response serialization.

**Components:**
- `health.py`: Health check endpoints
- `knowledge.py`: Knowledge base access endpoints  
- `query.py`: Natural language query processing endpoints
- `viz.py`: Visualization suggestion endpoints

**Responsibilities:**
- HTTP request/response handling
- Input validation using Pydantic models
- API documentation generation
- Error handling and status codes

### 2. Service Layer (`backend/app/services/`)

Business logic implementation with clear separation of concerns.

**Components:**
- `nl_sql_pipeline.py`: Natural language to SQL conversion
- `sql_executor.py`: SQL query execution (currently mock)
- `knowledge_base.py`: Domain knowledge management
- `viz_suggester.py`: Visualization recommendation engine

**Responsibilities:**
- Core business logic
- Data transformation and processing
- Integration with external services (planned)
- Stub implementations for MVP

### 3. Model Layer (`backend/app/models/`)

Pydantic models for data validation and serialization.

**Components:**
- `query_models.py`: Request/response models for all API endpoints

**Responsibilities:**
- Data validation and type checking
- Serialization/deserialization
- API documentation schema generation
- Type safety across the application

### 4. Configuration Layer

Application configuration and dependency management.

**Components:**
- `config.py`: Pydantic Settings for environment variables
- `dependencies.py`: FastAPI dependency injection
- `logging.py`: Loguru logging configuration

**Responsibilities:**
- Environment-based configuration
- Dependency injection and lifecycle management
- Structured logging setup
- Settings validation

## Data Flow

### Natural Language Query Processing

```
1. Client Request
   └── POST /query/prepare
       └── {"question": "What was revenue last quarter?"}

2. API Layer (routers/query.py)
   └── Validates NLQueryRequest
   └── Calls NLToSQLPipeline.generate()

3. Service Layer (services/nl_sql_pipeline.py)
   └── Processes question (currently stub)
   └── Returns (sql, explanation, domains)

4. Response
   └── ProposedQueryResponse with SQL + explanation
```

### Query Execution Flow

```
1. Client Request  
   └── POST /query/execute
       └── {"sql": "SELECT ...", "limit": 100}

2. API Layer (routers/query.py)
   └── Validates ExecuteQueryRequest
   └── Calls SQLExecutor.execute()

3. Service Layer (services/sql_executor.py) 
   └── Analyzes SQL (currently stub)
   └── Generates synthetic data
   └── Returns (columns, rows, warning)

4. Response
   └── ExecuteQueryResponse with mock data
```

### Knowledge Base Access

```
1. Client Request
   └── GET /knowledge/domains/financials

2. API Layer (routers/knowledge.py)
   └── Calls KnowledgeBase.get_domain()

3. Service Layer (services/knowledge_base.py)
   └── Reads YAML from domain_data/
   └── Parses into KnowledgeDomain model

4. Response
   └── Complete domain documentation
```

## Extension Points for Future Features

### 1. Authentication & Authorization

**Current State**: OKTA configuration placeholders in `config.py`

**Future Implementation**:
- Add FastAPI security dependencies
- Implement JWT token validation
- Role-based access control
- Session management

**Integration Points**:
```python
# In dependencies.py
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validate OKTA token
    pass

# In routers
@router.post("/query/prepare")
async def prepare_query(
    request: NLQueryRequest,
    user: User = Depends(get_current_user)  # Add auth
):
```

### 2. BigQuery Integration  

**Current State**: Mock data in `SQLExecutor`

**Future Implementation**:
- Replace `SQLExecutor` with real BigQuery client
- Add connection pooling and query optimization
- Implement query result caching
- Add query cost estimation

**Integration Points**:
```python
# In services/sql_executor.py
from google.cloud import bigquery

class SQLExecutor:
    def __init__(self):
        self.client = bigquery.Client(project=settings.bigquery_project)
    
    async def execute(self, sql: str, limit: int):
        # Real BigQuery execution
        pass
```

### 3. LLM Integration

**Current State**: Deterministic stubs in `NLToSQLPipeline`

**Future Implementation**:
- Integration with OpenAI, Anthropic, or Google APIs
- Context-aware SQL generation
- Schema-aware query optimization
- Natural language explanations

**Integration Points**:
```python
# In services/nl_sql_pipeline.py
class NLToSQLPipeline:
    def __init__(self):
        self.llm_client = get_llm_client()
        self.knowledge_base = get_knowledge_base()
    
    async def generate(self, question: str):
        # Context from knowledge base
        context = self.knowledge_base.get_relevant_context(question)
        # LLM-powered generation
        return await self.llm_client.generate_sql(question, context)
```

### 4. PRD Generation

**Current State**: Placeholder templates in `templates/`

**Future Implementation**:
- Jinja2 template engine integration
- Dynamic template selection
- Multi-format output (PDF, Word, HTML)
- Template customization

**Integration Points**:
```python
# New service: services/prd_generator.py
class PRDGenerator:
    def generate_prd(self, query_results, visualizations, insights):
        template = self.template_env.get_template('base_prd.j2')
        return template.render(
            results=query_results,
            charts=visualizations,
            insights=insights
        )
```

### 5. PDF Search & Document Indexing

**Current State**: Not implemented

**Future Implementation**:
- Vector database integration (Pinecone, Weaviate)
- Document processing pipeline
- Semantic search capabilities
- Content summarization

**Integration Points**:
```python
# New service: services/document_search.py
class DocumentSearch:
    def __init__(self):
        self.vector_db = get_vector_database()
        
    async def search_documents(self, query: str):
        # Vector similarity search
        pass
        
    async def index_document(self, document_path: str):
        # Process and index new documents
        pass
```

## Scalability Considerations

### Current MVP Constraints

- Single-instance deployment
- In-memory knowledge base
- Synchronous request processing
- No caching layer

### Future Scaling Strategies

1. **Horizontal Scaling**
   - Containerization with Docker
   - Load balancing with multiple instances
   - Database connection pooling

2. **Caching**
   - Redis for query result caching
   - Knowledge base caching
   - LLM response caching

3. **Async Processing**
   - Background job queues (Celery, RQ)
   - Async database operations
   - Streaming responses for large datasets

4. **Monitoring & Observability**
   - Structured logging with correlation IDs
   - Metrics collection (Prometheus)
   - Distributed tracing
   - Health check endpoints

## Security Architecture

### Current Implementation

- CORS middleware (permissive for development)
- Input validation via Pydantic
- Basic error handling

### Production Considerations

1. **Authentication**
   - OKTA integration for SSO
   - JWT token validation
   - Session management

2. **Authorization**  
   - Role-based access control
   - Resource-level permissions
   - API rate limiting

3. **Data Security**
   - SQL injection prevention
   - Query result sanitization
   - Audit logging

4. **Network Security**
   - HTTPS enforcement
   - CORS policy refinement
   - API gateway integration

## Testing Strategy

### Current Test Coverage

- Unit tests for API endpoints
- Integration tests for service layer
- Deterministic behavior validation

### Comprehensive Testing Plan

1. **Unit Tests**
   - Service layer business logic
   - Model validation
   - Utility functions

2. **Integration Tests**
   - Database connectivity
   - External API integration
   - End-to-end request flows

3. **Performance Tests**
   - Load testing with realistic data volumes
   - Query execution performance
   - Memory usage profiling

4. **Security Tests**
   - Authentication bypass attempts
   - Input sanitization validation
   - Authorization boundary testing

## Deployment Architecture

### Development

- Local Poetry environment
- SQLite for development data
- Hot reloading with Uvicorn

### Staging/Production (Future)

```
┌─────────────────┐
│ Load Balancer   │
│ (nginx/AWS ALB) │
└────────┬────────┘
         │
    ┌────▼────┐
    │ FastAPI │
    │ App     │
    │ (Docker)│
    └────┬────┘
         │
    ┌────▼────┐    ┌─────────────┐
    │BigQuery │    │   Redis     │
    │         │    │  (Cache)    │
    └─────────┘    └─────────────┘
```

## Configuration Management

### Environment-Based Configuration

- Development: `.env` files
- Staging: Environment variables
- Production: Secret management (AWS Secrets Manager, etc.)

### Configuration Validation

- Pydantic Settings for type safety
- Required vs optional settings
- Environment-specific defaults

This architecture provides a solid foundation for the current MVP while enabling systematic enhancement as requirements evolve.