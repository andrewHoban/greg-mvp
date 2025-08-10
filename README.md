# Greg MVP - AI Product Manager Assistant

A Python FastAPI backend for an AI-powered assistant that helps product managers query data using natural language, generate insights, and create visualizations.

## Features

* **Natural Language to SQL**: Convert natural language questions into SQL queries with explanations
* **Mock Data Execution**: Execute queries against synthetic data (BigQuery integration planned)
* **Knowledge Base**: Structured domain knowledge with table documentation and join rules
* **Visualization Suggestions**: AI-powered chart and graph recommendations
* **RESTful API**: FastAPI-based REST API with automatic OpenAPI documentation
* **Development Tools**: Comprehensive linting, testing, and development workflow

## Quick Start

### Prerequisites

- Python 3.11+
- Poetry (for dependency management)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd greg-mvp
   ```

2. **Install dependencies:**
   ```bash
   make install
   ```

3. **Start the development server:**
   ```bash
   make run
   ```

4. **Verify the installation:**
   ```bash
   curl http://127.0.0.1:8000/health
   # Should return: {"status":"ok","service":"greg-mvp-backend","version":"0.1.0"}
   ```

### Alternative Setup (Manual)

If you prefer manual setup or don't have `make` available:

```bash
# Install Poetry (if not already installed)
pip3 install poetry

# Install dependencies
poetry install

# Start the server
poetry run uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Bootstrap Script

For automated development environment setup:

```bash
# Full setup with server start
./scripts/dev_bootstrap.sh

# Setup without starting server
./scripts/dev_bootstrap.sh --no-run
```

## API Endpoints

### Core Endpoints

- **Health Check**: `GET /health` - Service status
- **API Root**: `GET /` - Basic API information  
- **Documentation**: `GET /docs` - Interactive API documentation

### Query Processing

- **Prepare Query**: `POST /query/prepare`
  - Input: Natural language question
  - Output: SQL query + explanation + referenced domains
  
- **Execute Query**: `POST /query/execute`  
  - Input: SQL query + optional limit
  - Output: Mock data results with columns and rows

### Knowledge Base

- **List Domains**: `GET /knowledge/domains` - Available data domains
- **Get Domain**: `GET /knowledge/domains/{domain_name}` - Detailed domain info
- **Search Tables**: `GET /knowledge/search/tables?q={query}` - Find tables by name/description

### Visualization

- **Suggest Charts**: `POST /viz/suggest`
  - Input: Field metadata + context
  - Output: Chart type recommendations with Plotly specs

## Example Usage

### Natural Language Query

```bash
curl -X POST "http://127.0.0.1:8000/query/prepare" \
     -H "Content-Type: application/json" \
     -d '{"question": "What was the total revenue last quarter?"}'
```

### Query Execution

```bash
curl -X POST "http://127.0.0.1:8000/query/execute" \
     -H "Content-Type: application/json" \
     -d '{
       "sql": "SELECT DATE_TRUNC(created_at, MONTH) AS month, SUM(amount) AS total_revenue FROM financials_transactions GROUP BY month ORDER BY month",
       "limit": 100
     }'
```

### Knowledge Base Access

```bash
# List all domains
curl "http://127.0.0.1:8000/knowledge/domains"

# Get specific domain
curl "http://127.0.0.1:8000/knowledge/domains/financials"
```

## Development Workflow

### Available Make Targets

```bash
make install    # Install dependencies
make run        # Start development server  
make dev        # Start with APP_ENV=dev
make lint       # Run code linting
make format     # Auto-format code
make test       # Run test suite
make check      # Run lint + mypy + tests
make export     # Export requirements.txt
make clean      # Remove cache files
make refresh    # Clean + install
```

### Code Quality

- **Linting**: Ruff for fast Python linting
- **Formatting**: Black + isort for consistent code style  
- **Type Checking**: MyPy for static type analysis
- **Testing**: pytest with async support

## Architecture Overview

### Application Structure

```
backend/app/
├── main.py              # FastAPI application entry point
├── config.py            # Pydantic settings management
├── logging.py           # Loguru logging configuration
├── dependencies.py      # FastAPI dependency injection
├── models/              # Pydantic models for API
├── routers/             # FastAPI route handlers
├── services/            # Business logic layer
├── domain_data/         # YAML knowledge base files
└── templates/           # Future PRD generation templates
```

### Service Layer

- **NLToSQLPipeline**: Converts natural language to SQL (stub implementation)
- **SQLExecutor**: Executes queries and returns synthetic data
- **KnowledgeBase**: Loads domain data from YAML files
- **VizSuggester**: Recommends visualizations based on data types

### Data Domains

The system includes three sample knowledge domains:

1. **Financials**: Revenue, billing, transactions
2. **Reads**: Energy meter readings and consumption  
3. **Customer Care**: Support tickets and service interactions

## Current Implementation Status

### ✅ Implemented (MVP Scope)

- FastAPI application with async support
- Health check and API documentation
- Natural language query preparation (deterministic stub)
- Mock data query execution  
- YAML-based knowledge base
- Visualization suggestion heuristics
- Comprehensive test suite
- Development tooling and scripts

### 🚧 Stub Implementations (Marked with TODOs)

- **NL-to-SQL conversion**: Returns deterministic sample SQL
- **Query execution**: Generates synthetic data instead of BigQuery
- **Authentication**: Placeholder OKTA configuration
- **PRD generation**: Template directory created but not implemented

### 🔜 Planned Features

- Real BigQuery integration
- LLM-based natural language processing
- OKTA authentication and authorization
- PDF document search and indexing
- Advanced visualization AI
- PRD template generation

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
BIGQUERY_PROJECT=your-gcp-project
OKTA_ISSUER_URL=https://your-okta-domain/oauth2/default  
OKTA_AUDIENCE=api://default
APP_ENV=dev
```

### Application Settings

Settings are managed via Pydantic Settings in `backend/app/config.py`:

- API host/port configuration
- BigQuery project settings
- OKTA authentication URLs (placeholder)
- Logging levels and formats

## Testing

```bash
# Run all tests
make test

# Run with coverage
poetry run pytest --cov=backend

# Run specific test file
poetry run pytest tests/test_health.py -v
```

## Next Steps

1. **BigQuery Integration**: Replace mock SQL execution with real BigQuery client
2. **LLM Integration**: Implement actual natural language processing
3. **Authentication**: Add OKTA-based API security
4. **Advanced Analytics**: Enhanced insight generation
5. **PRD Generation**: Jinja2-based document creation
6. **PDF Search**: Document indexing and retrieval

## Contributing

1. Follow the established code style (Black + Ruff + isort)
2. Add tests for new functionality  
3. Update documentation for API changes
4. Use the provided development tools

## License

[Add your license information here]
