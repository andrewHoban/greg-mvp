# Greg MVP - AI Product Manager Assistant

This is a FastAPI-based MVP for an AI-powered assistant that helps product managers query data using natural language, with domain knowledge and NL->SQL capabilities.

## Features

* **FastAPI Backend**: Modern async Python API with automatic documentation
* **Natural Language to SQL**: Convert questions into SQL queries with domain-aware routing
* **Domain Knowledge System**: YAML-based knowledge definitions for reads, financials, and customer care
* **Query Pipeline**: Prepare -> Review -> Execute workflow for safe query processing
* **Mock Data Responses**: Synthetic data for immediate MVP functionality
* **Visualization Suggestions**: Chart type recommendations with Plotly specifications
* **Comprehensive Testing**: Pytest suite with health and pipeline validation

## Quick Start

1. **Clone and setup:**
   ```bash
   git clone <your-repo-url>
   cd greg-mvp
   ./scripts/dev_bootstrap.sh
   ```

2. **Start the FastAPI server:**
   ```bash
   make run
   # Server starts at http://127.0.0.1:8000
   ```

3. **Explore the API:**
   - **Interactive docs**: http://127.0.0.1:8000/docs
   - **Health check**: http://127.0.0.1:8000/health
   - **Root endpoint**: http://127.0.0.1:8000/

## API Endpoints

### Core Endpoints
```bash
GET  /health                    # System health check
GET  /                          # App info with version
GET  /docs                      # Interactive API documentation
```

### Knowledge Domain Access
```bash
GET  /knowledge/domains         # List available domains
GET  /knowledge/domains/{name}  # Get specific domain details
```

### Query Processing  
```bash
POST /query/prepare             # Generate SQL from natural language
POST /query/execute             # Execute SQL and return results
```

### Visualization
```bash
POST /viz/suggest              # Get chart suggestions for fields
```

## Example Usage

```bash
# List knowledge domains
curl http://127.0.0.1:8000/knowledge/domains

# Prepare a revenue query
curl -X POST http://127.0.0.1:8000/query/prepare \
  -H "Content-Type: application/json" \
  -d '{"question": "What was the total revenue last quarter?"}'

# Execute SQL query
curl -X POST http://127.0.0.1:8000/query/execute \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT COUNT(*) FROM users", "limit": 100}'
```

## Development Commands

```bash
make install    # Install dependencies with Poetry
make run        # Start production server  
make dev        # Start development server with auto-reload
make test       # Run pytest test suite
make lint       # Run linting checks
make format     # Format code with black/isort/ruff
make check      # Run all checks (lint + test)
make clean      # Clean up cache and temp files
```

## Architecture

The MVP uses a layered architecture:

- **API Layer**: FastAPI routers handling HTTP requests
- **Service Layer**: Business logic for NL->SQL, query execution, knowledge management
- **Data Layer**: YAML-based domain knowledge, mock data providers
- **Models**: Pydantic schemas for requests/responses

Key design decisions:
- **Stub implementations** for external services (BigQuery, LLMs) with clear interfaces
- **Domain-driven knowledge** stored in versioned YAML files  
- **Two-phase execution** (prepare -> execute) for query safety
- **Comprehensive abstractions** allowing easy component upgrades

## Project Structure

```
backend/app/
├── main.py              # FastAPI application
├── config.py            # Settings management  
├── dependencies.py      # Dependency injection
├── logging.py           # Logging configuration
├── routers/             # API endpoints
├── services/            # Business logic
├── models/              # Pydantic schemas
└── domain_data/         # Knowledge definitions

tests/                   # Test suite
scripts/                 # Development tools
docs/                    # Additional documentation
```

## Future Roadmap

See [ROADMAP.md](ROADMAP.md) for the complete 20-week development plan.
