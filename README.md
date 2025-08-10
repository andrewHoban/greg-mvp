# Greg MVP - Internal Data Exploration and Knowledge Platform

This is the MVP implementation of an internal data exploration and knowledge platform that enables product managers and analysts to query data using natural language, with placeholders and abstraction layers designed for later expansion.

⚠️ **WARNING: This is an MVP with placeholder implementations**
- Authentication uses demo stubs (real Okta integration pending)
- SQL execution returns synthetic data (real BigQuery integration pending)
- NL-to-SQL uses deterministic keyword matching (LLM integration pending)

## Features

### Current MVP Implementation
- **Natural Language to SQL**: Convert questions into structured SQL queries with explanations
- **Domain Knowledge Base**: YAML-based schema definitions for reads, financials, and customer care
- **Query Pipeline**: Two-step process (prepare → review → execute) for safe SQL execution
- **Visualization Suggestions**: Basic chart type recommendations with Plotly specs
- **Health Monitoring**: Application health and status endpoints

### Planned Extensions (See ROADMAP.md)
- Real Okta SSO authentication
- Actual BigQuery execution with cost controls
- Advanced LLM integration for NL-to-SQL
- Document PDF ingestion and semantic search
- PRD generation with templates
- Rich frontend UI
- Advanced analytics and caching

## Quick Start

### Option 1: Bootstrap Script (Recommended)
```bash
git clone https://github.com/andrewHoban/greg-mvp.git
cd greg-mvp
./scripts/dev_bootstrap.sh
```

### Option 2: Manual Setup
```bash
# 1. Clone and setup
git clone https://github.com/andrewHoban/greg-mvp.git
cd greg-mvp

# 2. Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# 3. Install dependencies
make install

# 4. Create environment file
cp .env.example .env
# Edit .env with your configuration (optional for MVP)

# 5. Start development server
make dev
```

## Usage

### API Endpoints

Once running (default: http://localhost:8000):

- **Health Check**: `GET /health`
- **API Documentation**: http://localhost:8000/docs
- **Knowledge Domains**: `GET /knowledge/domains`
- **Prepare Query**: `POST /query/prepare`
- **Execute Query**: `POST /query/execute`
- **Visualization**: `POST /viz/suggest`

### Example API Usage

```bash
# Health check
curl http://localhost:8000/health

# Prepare a query
curl -X POST http://localhost:8000/query/prepare \
  -H 'Content-Type: application/json' \
  -d '{"question": "Show total revenue by month"}'

# List knowledge domains
curl http://localhost:8000/knowledge/domains
```

## Architecture

### Backend Structure
```
backend/app/
├── main.py              # FastAPI app assembly
├── config.py            # Settings management
├── logging.py           # Loguru configuration
├── dependencies.py      # Dependency injection
├── routers/             # API endpoints
│   ├── health.py        # Health checks
│   ├── knowledge.py     # Domain knowledge access
│   ├── query.py         # NL-to-SQL pipeline
│   └── viz.py           # Visualization suggestions
├── services/            # Business logic
│   ├── knowledge_base.py    # YAML domain loader
│   ├── nl_sql_pipeline.py   # NL-to-SQL conversion
│   ├── sql_executor.py      # Query execution
│   └── viz_suggester.py     # Chart suggestions
├── models/              # Pydantic models
├── domain_data/         # YAML knowledge files
└── templates/           # Future PRD templates
```

### Domain Knowledge

The system includes three sample domains:
- **reads**: Content consumption metrics
- **financials**: Revenue and transaction data  
- **customer_care**: Support ticket analytics

Each domain defines:
- Table schemas with field descriptions
- Join relationships
- Business rules and caveats
- Sample questions

## Development

### Available Make Targets

```bash
make help       # Show available commands
make install    # Install dependencies
make dev        # Run with hot reload
make run        # Run in production mode
make test       # Run tests
make lint       # Run linting
make format     # Format code
make check      # Run all checks
make clean      # Clean cache files
make refresh    # Clean and reinstall
```

### Testing

```bash
# Run all tests
make test

# Run specific test
poetry run pytest tests/test_health.py -v
```

### Code Quality

```bash
# Format code
make format

# Run linter
make lint

# Run all quality checks
make check
```

## Configuration

Key environment variables (see .env.example):

- `OKTA_*`: SSO configuration (placeholder)
- `BIGQUERY_*`: BigQuery connection (placeholder)
- `DATABASE_URL`: Local database for caching
- `LOG_LEVEL`: Logging verbosity
- `DEBUG`: Development mode flag

## Security Note

⚠️ **Current authentication is for demonstration only**
- Uses X-User-Email header or falls back to demo@example.com
- No token validation or session management
- Production deployment requires proper Okta integration

## Contributing

1. Follow the existing code structure and patterns
2. Add tests for new functionality
3. Update documentation for API changes
4. Use the provided linting and formatting tools
5. Focus on maintaining the abstraction layers for future expansion