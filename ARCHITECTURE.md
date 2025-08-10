# Architecture Overview

This document describes the architecture and design decisions for the Greg MVP internal data exploration platform.

## High-Level Architecture

The platform follows a layered architecture pattern with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Future)                        │
│                   React/Vue/Angular                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Layer                               │
│  FastAPI Routers (health, knowledge, query, viz)           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Service Layer                             │
│  NL-SQL Pipeline │ SQL Executor │ Viz Suggester             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Layer                                │
│  Knowledge Base │ BigQuery │ Vector Store (Future)          │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### API Layer (`backend/app/routers/`)

**FastAPI routers** provide RESTful endpoints organized by domain:

- **Health Router**: System status and monitoring
- **Knowledge Router**: Domain knowledge access and schema information
- **Query Router**: Natural language to SQL pipeline
- **Viz Router**: Visualization suggestion and chart generation

### Service Layer (`backend/app/services/`)

**Business logic services** implement core functionality:

- **NL-SQL Pipeline**: Converts natural language to SQL queries
- **SQL Executor**: Executes queries against BigQuery (stubbed)
- **Knowledge Base**: Manages domain knowledge from YAML files
- **Viz Suggester**: Suggests appropriate visualizations

### Data Layer

**Data sources and storage**:

- **YAML Knowledge Base**: Domain schemas, joins, and business rules
- **BigQuery**: Data warehouse for query execution (future)
- **Vector Store**: Document embeddings for semantic search (future)
- **SQLAlchemy**: Metadata persistence and caching (future)

## Design Principles

### 1. Layered Architecture
- Clear separation between API, service, and data layers
- Dependency injection for loose coupling
- Interface-based design for easy testing and mocking

### 2. Domain-Driven Design
- Domain knowledge is explicitly modeled and versioned
- Business rules are captured alongside schema definitions
- Sample questions guide NL-to-SQL development

### 3. API-First Development
- FastAPI automatic OpenAPI documentation
- Pydantic models for request/response validation
- Clear API contracts for frontend integration

### 4. Extensibility by Design
- Placeholder interfaces for future LLM integration
- Modular service architecture
- Configuration-driven behavior

## Key Design Decisions

### Natural Language Processing Pipeline

The NL-to-SQL conversion follows a multi-stage pipeline:

```
Natural Language Question
         │
         ▼
   Keyword Analysis  ────► Domain Detection
         │                      │
         ▼                      ▼
  Intent Classification ──► Schema Context
         │                      │
         ▼                      ▼
   SQL Generation     ◄──── Query Template
         │
         ▼
   Query Validation
         │
         ▼
  Explanation Generation
```

**Current Implementation**: Deterministic keyword matching
**Future**: LLM-powered semantic understanding

### Domain Knowledge Management

Domain knowledge is stored in YAML files for:
- **Version Control**: Easy diff and collaboration
- **Human Readability**: Non-technical stakeholders can contribute
- **Structured Format**: Consistent schema across domains
- **Extensibility**: Easy to add new domains

```yaml
domain: "financials"
description: "Revenue and transaction data"
tables:
  transactions:
    fields:
      - name: "amount"
        type: "DECIMAL"
        semantic_role: "metric"
joins:
  - left_table: "transactions"
    right_table: "users"
    join_condition: "transactions.user_id = users.id"
```

### Query Safety and Review

Two-phase query execution ensures safety:

1. **Prepare Phase**: Generate SQL with explanation
2. **Execute Phase**: Run approved query with monitoring

This allows for:
- Human review of complex queries
- Cost estimation before execution
- Query optimization suggestions
- Audit trail for compliance

### Visualization Strategy

Chart suggestions use a rule-based heuristic system:

```python
# Example heuristic rules
if has_time_column and has_numeric_metrics:
    suggest("line_chart", "time_series")

if has_categories and has_single_metric:
    suggest("bar_chart", "comparison")

if has_two_numeric_columns:
    suggest("scatter_plot", "correlation")
```

**Current**: Simple heuristics based on column types
**Future**: ML-driven suggestions based on data patterns

## Data Flow

### Query Processing Flow

```
1. User submits natural language question
2. NL-SQL Pipeline analyzes question
3. Knowledge Base provides domain context
4. SQL query generated with explanation
5. User reviews proposed query
6. SQL Executor runs approved query
7. Results formatted and returned
8. Viz Suggester recommends charts
9. Frontend renders results and visualizations
```

### Authentication Flow (Future)

```
1. User accesses application
2. Redirect to Okta for authentication
3. Okta returns JWT token
4. Token validation on each API request
5. User permissions checked against domain access
6. Query execution with user context logging
```

## Scalability Considerations

### Performance
- **Caching**: Query results and schema metadata
- **Connection Pooling**: BigQuery connection management
- **Rate Limiting**: Per-user query limits
- **Async Processing**: Non-blocking query execution

### Security
- **Token Validation**: JWT-based authentication
- **Query Sanitization**: SQL injection prevention
- **Access Control**: Domain-based permissions
- **Audit Logging**: All queries and results logged

### Monitoring
- **Health Checks**: Application and dependency status
- **Metrics**: Query performance, error rates, usage patterns
- **Alerting**: Cost thresholds, error rates, performance degradation
- **Logging**: Structured logs for troubleshooting

## Technology Choices

### Backend Framework: FastAPI
- **Automatic Documentation**: OpenAPI/Swagger generation
- **Type Safety**: Pydantic model validation
- **Performance**: Async support and high throughput
- **Developer Experience**: Excellent IDE support

### Configuration: Pydantic Settings
- **Environment Variables**: 12-factor app compliance
- **Type Validation**: Runtime configuration validation
- **Documentation**: Self-documenting configuration schema

### Logging: Loguru
- **Structured Logging**: JSON format for monitoring
- **Performance**: Efficient async logging
- **Configuration**: Simple, readable setup

### Package Management: Poetry
- **Dependency Resolution**: Robust lock file management
- **Virtual Environments**: Isolated dependencies
- **Build System**: Modern Python packaging

## Future Architectural Evolution

### Phase 2: LLM Integration
- Replace keyword matching with LLM-powered NL understanding
- Add prompt engineering and chain-of-thought reasoning
- Implement query optimization suggestions

### Phase 3: Advanced Analytics
- Add statistical analysis and anomaly detection
- Implement automated insight generation
- Support for complex multi-step analysis

### Phase 4: Full Platform
- Rich frontend with interactive dashboards
- Real-time collaboration features
- Enterprise features (SSO, RBAC, compliance)
- Mobile application support

## Migration Strategy

The current stub implementations provide clear interfaces for future enhancements:

1. **Authentication**: Replace stub with Okta SDK integration
2. **Query Execution**: Replace synthetic data with BigQuery client
3. **NL-to-SQL**: Replace keywords with LLM API calls
4. **Visualization**: Enhance heuristics with ML models
5. **Document Search**: Add vector database and embedding pipeline

Each component can be upgraded independently without affecting the overall architecture.