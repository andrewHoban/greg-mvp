# Greg MVP - AI Product Manager Assistant

A FastAPI-based MVP for an AI-powered assistant that helps product managers query data using natural language and generate visualizations.

## Features

* **Natural Language to SQL**: Converts questions into SQL queries with explanations
* **Query Execution**: Executes SQL queries with synthetic data (stub implementation)
* **Knowledge Domains**: Manages domain-specific data schemas (financials, customer care, content)
* **Visualization Suggestions**: Recommends chart types and generates Plotly configurations
* **REST API**: Complete FastAPI backend with OpenAPI documentation

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/andrewHoban/greg-mvp.git
   cd greg-mvp
   ```

2. **Install dependencies:**
   ```bash
   make install
   ```

3. **Start the server:**
   ```bash
   make run
   ```

4. **Test the health endpoint:**
   ```bash
   curl http://localhost:8000/health
   # Expected: {"status":"ok","version":"0.1.0","timestamp":"2024-..."}
   ```

5. **View API documentation:**
   Open http://localhost:8000/docs in your browser

## Development

### Requirements

* Python 3.11+
* Poetry (for dependency management)

### Setup

Use the development bootstrap script to set up everything automatically:

```bash
./scripts/dev_bootstrap.sh
```

Or set up manually:

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
make install

# Copy environment file
cp .env.example .env

# Start development server (with auto-reload)
make dev
```

### Available Commands

```bash
make install    # Install dependencies
make run        # Run production server
make dev        # Run development server with auto-reload
make test       # Run tests
make lint       # Run linting
make format     # Format code
make check      # Run linting + tests
make clean      # Clean cache files
make refresh    # Clean + reinstall
```

## API Endpoints

### Core Endpoints

* `GET /health` - Health check
* `GET /docs` - Interactive API documentation

### Query Endpoints

* `POST /query/prepare` - Convert natural language to SQL
  ```json
  {
    "question": "What was our total revenue last month?"
  }
  ```

* `POST /query/execute` - Execute SQL query
  ```json
  {
    "sql": "SELECT * FROM financials_transactions",
    "limit": 100
  }
  ```

### Knowledge Endpoints

* `GET /knowledge` - List all knowledge domains
* `GET /knowledge/{domain_name}` - Get domain details

### Visualization Endpoints

* `POST /viz/suggest` - Get visualization recommendations
  ```json
  {
    "sql": "SELECT month, revenue FROM financials",
    "data_sample": []
  }
  ```

## Architecture

The application follows a clean architecture pattern:

* **FastAPI App** (`backend/app/main.py`) - Application entry point
* **Routers** (`backend/app/routers/`) - API endpoint definitions  
* **Services** (`backend/app/services/`) - Business logic
* **Models** (`backend/app/models/`) - Pydantic data models
* **Domain** (`backend/domain/`) - YAML knowledge base files

## Testing

Run the test suite:

```bash
make test
```

Tests cover:
* Health endpoint functionality
* Query preparation and execution
* API request/response validation
* Error handling

## Knowledge Domains

The system includes three predefined knowledge domains:

1. **Financials** - Revenue, transactions, financial metrics
2. **Customer Care** - Support tickets, satisfaction scores, agent performance  
3. **Reads** - Content engagement, reading analytics, user behavior

Domain schemas are defined in YAML files under `backend/domain/`.

## Future Enhancements

See [ROADMAP.md](ROADMAP.md) for planned features and [ARCHITECTURE.md](ARCHITECTURE.md) for detailed technical design.

Key areas for development:
- [ ] Real BigQuery integration
- [ ] Okta authentication 
- [ ] LLM-powered NL→SQL conversion
- [ ] Advanced visualization engine
- [ ] Caching and performance optimization