# Greg MVP Architecture

## Overview

This FastAPI MVP implements a domain-aware natural language to SQL system with a clean, extensible architecture designed for rapid iteration and future enhancements.

## Core Principles

1. **Domain-Driven Design**: Business knowledge is explicitly modeled in versioned YAML files
2. **Service Layer Architecture**: Clear separation between API, business logic, and data layers
3. **Stub-First Development**: External integrations use placeholder implementations with production-ready interfaces
4. **Two-Phase Query Safety**: Prepare -> Review -> Execute workflow prevents accidental expensive operations

## Component Architecture

### API Layer (`routers/`)
- **Health**: System monitoring and status checks
- **Knowledge**: Domain metadata access and browsing
- **Query**: Natural language processing and SQL execution pipeline
- **Visualization**: Chart type suggestions and Plotly figure generation

### Service Layer (`services/`)
- **NLToSQLPipeline**: Converts natural language to SQL using keyword-based routing
- **SQLExecutor**: Query execution with mock data responses (BigQuery interface ready)
- **KnowledgeBase**: YAML domain knowledge loader and accessor
- **VizSuggester**: Visualization type recommendations based on field analysis

### Data Layer (`domain_data/`)
- **YAML Knowledge Definitions**: Structured domain metadata including:
  - Table schemas with semantic field roles
  - Join relationship definitions
  - Business rules and caveats
  - Sample questions for testing

### Model Layer (`models/`)
- **Pydantic Schemas**: Type-safe request/response models with validation
- **Domain Models**: Knowledge domain structure definitions

## Data Flow

### Query Processing Pipeline
1. **User Question** -> NL Query Request
2. **NL Processing** -> Keyword analysis and domain routing  
3. **SQL Generation** -> Domain-specific query templates
4. **Query Preparation** -> SQL with explanation and metadata
5. **User Review** -> Human verification step
6. **Query Execution** -> Mock data response (BigQuery-ready interface)
7. **Result Formatting** -> Structured response with warnings

### Knowledge Management Flow
1. **YAML Files** -> Domain definitions in version control
2. **Knowledge Base** -> Runtime loading and caching
3. **API Endpoints** -> RESTful access to domain metadata
4. **Query Routing** -> Domain-aware SQL generation

## Extension Points

### LLM Integration Ready
- `NLToSQLPipeline` uses simple keyword routing but interface supports LLM providers
- Configuration placeholders for API keys and model selection
- Response formatting matches expected LLM output structure

### BigQuery Integration Ready  
- `SQLExecutor` returns mock data but implements BigQuery client interface
- Configuration for project IDs and authentication
- Query result formatting matches BigQuery response structure

### Authentication Ready
- Okta SSO configuration placeholders in settings
- Dependency injection ready for auth middleware
- JWT token handling interfaces defined

### Visualization Engine Ready
- `VizSuggester` provides Plotly specifications
- Chart type analysis based on field semantics
- Frontend integration points for interactive dashboards

## Configuration Management

### Environment-Based Settings
- **Development**: Local SQLite, mock services, debug logging
- **Staging**: Cloud databases, real auth, structured logging  
- **Production**: Full BigQuery integration, monitoring, security

### Domain Knowledge Evolution
- YAML files in version control enable collaborative domain modeling
- Non-technical stakeholders can contribute domain expertise
- Schema validation prevents breaking changes
- Migration tools for knowledge base updates

## Testing Strategy

### Unit Testing
- Service layer components with mock dependencies
- Domain knowledge loading and validation
- SQL generation logic verification

### Integration Testing  
- API endpoint functionality
- End-to-end query processing pipeline
- Mock data response validation

### Future Testing
- Real BigQuery integration tests (development project)
- LLM provider integration tests with API mocking
- Performance testing with concurrent query loads

## Security Considerations

### Current MVP Security
- Input validation on all API endpoints
- SQL injection prevention through parameterized queries (when real DB connected)
- Environment variable protection for sensitive configuration

### Production Security Ready
- HTTPS enforcement configuration
- Okta SSO integration endpoints
- JWT token validation middleware
- API rate limiting and request throttling
- Audit logging for all query executions

## Performance Considerations  

### Current Performance
- In-memory knowledge base caching
- Fast keyword-based query routing
- Minimal dependencies for fast startup

### Production Performance Ready
- Redis caching layer for query results
- Connection pooling for BigQuery
- Async request processing
- Query result pagination
- Monitoring and metrics collection

## Monitoring and Observability

### Current Logging
- Structured logging with Loguru
- ISO timestamp formatting
- Request/response logging

### Production Monitoring Ready
- Health check endpoints for load balancers
- Metrics collection points (Prometheus-ready)
- Error tracking integration points
- Performance monitoring hooks
- Business metrics tracking (query success rates, domain usage)

This architecture provides immediate MVP functionality while establishing clear upgrade paths for production deployment with real integrations.