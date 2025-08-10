# Greg MVP - AI Product Manager Assistant

Greg MVP is a Proof of Concept FastAPI application that helps product managers query data using natural language. It converts natural language questions into SQL queries, executes them (with mock data), and provides visualization suggestions.

## Quick Start

### Prerequisites
- Python 3.11+
- Poetry (for dependency management)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd greg-mvp
   ```

2. **Fetch and checkout the Python FastAPI branch:**
   ```bash
   git fetch origin
   git checkout <branch-name>
   ```

3. **Install dependencies:**
   ```bash
   make install
   ```

4. **Start the server:**
   ```bash
   make run
   ```

5. **Verify the installation:**
   ```bash
   # Check health endpoint
   curl http://127.0.0.1:8000/health
   
   # Should return: {"status":"ok","timestamp":"...","version":"0.1.0"}
   ```

6. **Test a sample query:**
   ```bash
   # Prepare a revenue query
   curl -X POST "http://127.0.0.1:8000/query/prepare" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is our total revenue this year?"}'
   ```

### Development Setup

Use the development bootstrap script:
```bash
./scripts/dev_bootstrap.sh
```

Or run in development mode with auto-reload:
```bash
make dev
```

## Features

All features are currently implemented with mock/stub data for development and testing:

- ✅ **Natural Language to SQL**: Converts questions to SQL queries (deterministic logic)
- ✅ **Query Execution**: Executes SQL and returns synthetic data
- ✅ **Knowledge Base**: YAML-based domain definitions (financials, reads, customer_care)
- ✅ **Visualization Suggestions**: Recommends chart types and generates sample Plotly figures
- ✅ **Health Monitoring**: Health check endpoints for service monitoring
- 🔄 **Authentication**: Okta integration (planned)
- 🔄 **BigQuery Integration**: Real data connection (planned)
- 🔄 **LLM Provider**: Advanced NL processing (planned)

## API Endpoints

### Core Endpoints
- `GET /` - Application metadata
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### Query Processing
- `POST /query/prepare` - Convert natural language to SQL
- `POST /query/execute` - Execute SQL query (returns mock data)

### Knowledge Management
- `GET /knowledge/domains` - List available domains
- `GET /knowledge/domains/{name}` - Get domain details

### Visualization
- `POST /viz/suggest` - Get visualization suggestions for data

## Development Commands

```bash
make install    # Install dependencies
make run        # Run in production mode
make dev        # Run in development mode with auto-reload
make lint       # Lint code with ruff
make format     # Format code with black and isort
make test       # Run tests
make check      # Run all checks (lint, format, type check, tests)
make clean      # Clean build artifacts
make refresh    # Clean, install, and test
```

## Architecture

The application follows a layered architecture with clear separation of concerns:

- **API Layer**: FastAPI routers handling HTTP requests
- **Service Layer**: Business logic for NL->SQL, execution, and visualization
- **Data Layer**: Knowledge base and mock data providers
- **Models**: Pydantic models for request/response validation

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architectural information.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for upcoming features and milestones.

## Contributing

1. Ensure all tests pass: `make test`
2. Ensure code passes linting: `make lint`
3. Run the full check suite: `make check`

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
BIGQUERY_PROJECT=your-gcp-project
OKTA_ISSUER_URL=https://your-okta-domain/oauth2/default
OKTA_AUDIENCE=api://default
APP_ENV=dev
```
