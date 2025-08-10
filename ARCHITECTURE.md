# Architecture

Greg MVP follows a layered architecture pattern designed for scalability and maintainability.

## System Overview

```
┌─────────────────────────────────────────┐
│              API Layer                  │
│  ┌─────────────────────────────────────┐│
│  │   FastAPI Routers                   ││
│  │  • Health   • Query                 ││
│  │  • Knowledge • Visualization        ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│             Service Layer               │
│  ┌─────────────────────────────────────┐│
│  │   Business Logic Services           ││
│  │  • NL->SQL Pipeline                 ││
│  │  • SQL Executor                     ││
│  │  • Knowledge Base                   ││
│  │  • Visualization Suggester          ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│              Data Layer                 │
│  ┌─────────────────────────────────────┐│
│  │   Data Sources & Storage            ││
│  │  • YAML Domain Definitions          ││
│  │  • Mock Data Providers              ││
│  │  • BigQuery (Future)                ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

## Layer Descriptions

### API Layer (FastAPI Routers)
Handles HTTP requests and responses, input validation, and error handling.

**Components:**
- **Health Router**: Service health and status endpoints
- **Query Router**: Natural language query processing endpoints
- **Knowledge Router**: Domain knowledge management endpoints  
- **Visualization Router**: Chart and visualization suggestion endpoints

**Responsibilities:**
- Request/response handling
- Input validation using Pydantic models
- Authentication (future)
- Rate limiting (future)
- API documentation generation

### Service Layer (Business Logic)
Contains the core business logic and orchestrates data processing workflows.

**Components:**

#### NL to SQL Pipeline
Converts natural language questions into SQL queries.
- **Current**: Deterministic rule-based logic
- **Future**: LLM-powered conversion with context awareness

#### SQL Executor
Executes SQL queries and returns results.
- **Current**: Mock data generation based on query patterns
- **Future**: BigQuery integration with caching and optimization

#### Knowledge Base
Manages domain definitions and metadata.
- **Current**: YAML-based domain definitions loaded at startup
- **Future**: Dynamic loading, versioning, and user-defined schemas

#### Visualization Suggester
Suggests appropriate visualizations for query results.
- **Current**: Rule-based chart type suggestions with sample Plotly figures
- **Future**: ML-powered suggestions based on data patterns and user preferences

**Responsibilities:**
- Business logic implementation
- Data transformation
- External service integration
- Caching and optimization

### Data Layer (Storage & Sources)
Manages data persistence and retrieval from various sources.

**Current Components:**
- **YAML Domain Files**: Static domain definitions (financials, reads, customer_care)
- **Mock Data Providers**: Synthetic data generation for development

**Future Components:**
- **BigQuery Integration**: Production data source
- **Caching Layer**: Redis for query result caching
- **Metrics Storage**: Query performance and usage tracking

## Data Flow

1. **Request Processing**
   ```
   HTTP Request → FastAPI Router → Input Validation → Service Layer
   ```

2. **Query Processing**
   ```
   Natural Language → NL-SQL Pipeline → SQL Generation → Executor → Mock Data
   ```

3. **Knowledge Retrieval**
   ```
   Domain Request → Knowledge Base → YAML Files → Domain Data
   ```

4. **Visualization**
   ```
   Query Results → Viz Suggester → Chart Analysis → Plotly Figure
   ```

## Configuration Management

- **Environment Variables**: Loaded via Pydantic Settings
- **Logging**: Structured logging with Loguru
- **Dependency Injection**: FastAPI dependency system for service instances

## Authentication & Security (Future)

```
┌─────────────────────────────────────────┐
│          Authentication Flow            │
│                                         │
│  Client → Okta → JWT Token → API       │
│                     │                   │
│              Token Validation           │
│                     │                   │
│              Request Processing         │
└─────────────────────────────────────────┘
```

## Error Handling

- **API Level**: HTTP status codes and structured error responses
- **Service Level**: Custom exceptions with context
- **Data Level**: Validation errors and connection failures

## Monitoring & Observability (Future)

- **Health Checks**: Multiple levels (API, services, external dependencies)
- **Metrics**: Request rates, response times, error rates
- **Logging**: Structured logs with correlation IDs
- **Tracing**: Distributed tracing for request flows

## Scalability Considerations

### Current Architecture
- Suitable for development and small-scale deployments
- Stateless services enable horizontal scaling
- In-memory caching for knowledge base

### Future Enhancements
- Containerization with Docker
- Kubernetes deployment
- Database connection pooling
- Distributed caching with Redis
- Load balancing
- Auto-scaling based on metrics