# Architecture Overview

## System Design

The Greg MVP follows a clean, modular architecture built on FastAPI and Python 3.11+.

```
greg-mvp/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── models/              # Pydantic data models
│   │   ├── routers/             # API route handlers
│   │   │   ├── health.py        # Health check endpoint
│   │   │   ├── knowledge.py     # Knowledge domain endpoints
│   │   │   ├── query.py         # Query processing endpoints
│   │   │   └── viz.py           # Visualization endpoints
│   │   └── services/            # Business logic layer
│   │       ├── knowledge_base.py     # Domain knowledge manager
│   │       ├── nl_to_sql.py          # NL to SQL conversion
│   │       ├── sql_executor.py       # Query execution
│   │       └── visualization_suggester.py  # Chart recommendations
│   └── domain/                  # YAML knowledge base
│       ├── financials.yaml
│       ├── customer_care.yaml
│       └── reads.yaml
├── tests/                       # Test suite
├── scripts/                     # Development scripts
├── pyproject.toml              # Poetry dependencies & config
└── Makefile                    # Build automation
```

## Core Components

### 1. FastAPI Application (`backend/app/main.py`)

The main application configures:
- CORS middleware for cross-origin requests
- Application lifespan management
- Router registration
- Logging configuration
- Knowledge base initialization

### 2. API Routers

**Health Router** (`/health`)
- Simple health check endpoint
- Returns status, version, and timestamp

**Knowledge Router** (`/knowledge`)
- Lists available knowledge domains
- Provides detailed domain schemas
- Loads from YAML files in `backend/domain/`

**Query Router** (`/query`)
- `/prepare`: Natural language → SQL conversion
- `/execute`: SQL query execution (stub with synthetic data)

**Visualization Router** (`/viz`)
- `/suggest`: Chart type recommendations
- Returns Plotly configuration samples

### 3. Services Layer

**Knowledge Base Service**
- Loads and manages YAML domain definitions
- Provides schema information
- Finds relevant domains for questions

**NL to SQL Service**
- Converts natural language to SQL (stub implementation)
- Returns deterministic queries for MVP
- Provides explanations and domain references

**SQL Executor Service** 
- Executes SQL queries (stub with synthetic data)
- Simulates BigQuery responses
- Returns structured result sets

**Visualization Suggester Service**
- Analyzes SQL queries for chart recommendations
- Generates Plotly configuration templates
- Ranks suggestions by appropriateness

### 4. Data Models

Pydantic models define:
- API request/response schemas
- Data validation and serialization
- Type hints and documentation
- Error handling

### 5. Knowledge Base

YAML files define domain schemas:
- Table structures and column types
- Sample questions for each domain
- Metadata and descriptions

## Technology Stack

### Core Framework
- **FastAPI**: Modern, high-performance web framework
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server with auto-reload

### Dependencies
- **Loguru**: Structured logging
- **PyYAML**: YAML configuration parsing
- **Google Cloud BigQuery**: Future database integration
- **Plotly**: Visualization configuration
- **HTTPx**: HTTP client for external APIs

### Development Tools
- **Poetry**: Dependency management and packaging
- **pytest**: Testing framework with async support
- **Ruff**: Fast Python linter
- **Black**: Code formatter
- **isort**: Import sorting
- **MyPy**: Static type checking (optional)

## Request Flow

```
1. Client Request → FastAPI Router
2. Router → Service Layer (business logic)
3. Service → Knowledge Base (domain lookup)
4. Service → Processing (NL→SQL, execution, etc.)
5. Service → Response Model (Pydantic validation)
6. Response Model → Client (JSON response)
```

## Configuration Management

- **Environment Variables**: `.env` file for configuration
- **Settings**: Pydantic Settings for typed configuration
- **Poetry**: `pyproject.toml` for dependencies and tooling
- **Makefile**: Standardized development commands

## Error Handling

- **HTTP Status Codes**: Proper REST status codes
- **Pydantic Validation**: Request/response validation
- **Structured Logging**: Detailed error logging
- **Exception Handling**: Graceful error responses

## Testing Strategy

- **Unit Tests**: Service layer functionality
- **Integration Tests**: API endpoint behavior
- **Validation Tests**: Request/response structure
- **Stub Testing**: Synthetic data validation

## Future Architecture Considerations

### Scalability
- Async/await throughout for concurrent processing
- Connection pooling for database operations
- Caching layer (Redis) for frequent queries
- Load balancing for multiple instances

### Security
- Authentication middleware (Okta integration)
- API rate limiting
- Input sanitization and validation
- Secure credential management

### Monitoring
- Application performance monitoring (APM)
- Health check endpoints
- Metrics collection and alerting
- Request/response logging

### Data Integration
- BigQuery connector for real data
- Schema migration management
- Data pipeline integration
- Real-time data streaming