# Greg MVP - AI Product Manager Assistant

A FastAPI-based MVP for an AI-powered assistant that helps product managers query data using natural language.

## Features

- **Health Monitoring**: Service health check endpoint
- **Knowledge Base**: Searchable knowledge base for best practices and guidelines
- **Natural Language Queries**: Convert natural language questions into SQL queries
- **Visualization Suggestions**: AI-powered recommendations for data visualization
- **Full API Documentation**: Interactive Swagger UI and ReDoc
- **Type Safety**: Full type hints with MyPy validation
- **Code Quality**: Linting with Ruff, formatting, and comprehensive tests
- **CI/CD**: GitHub Actions for continuous integration
- **Docker Support**: Containerized application ready for deployment

## API Endpoints

- `GET /` - Root endpoint
- `GET /api/health` - Health check
- `GET /api/knowledge` - Get knowledge base items (supports pagination and filtering)
- `POST /api/query` - Process natural language queries and generate SQL
- `POST /api/visualization-suggestions` - Get visualization suggestions for queries
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Local Development Setup

### Prerequisites

- Python 3.12+
- Poetry (for dependency management)
- Docker (optional, for containerized deployment)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd greg-mvp
```

### 2. Install Dependencies with Poetry

```bash
# Install Poetry if you don't have it
pip install poetry

# Install project dependencies
poetry install
```

### 3. Local Validation Steps

#### Run the FastAPI Server

```bash
# Start the development server with hot reload
poetry run uvicorn backend.app.main:app --reload

# The server will be available at: http://localhost:8000
```

#### Test All Endpoints

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test knowledge base
curl http://localhost:8000/api/knowledge

# Test natural language query
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "How many users signed up from USA last month?"}' \
  http://localhost:8000/api/query

# Test visualization suggestions  
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "SELECT country, COUNT(*) FROM users GROUP BY country"}' \
  http://localhost:8000/api/visualization-suggestions
```

#### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### Run Tests

```bash
# Run all tests with verbose output
poetry run pytest tests/ -v

# Run tests with coverage
poetry run pytest tests/ --cov=backend --cov-report=html
```

#### Code Quality Checks

```bash
# Lint code with Ruff
poetry run ruff check backend/ tests/

# Auto-fix linting issues
poetry run ruff check --fix backend/ tests/

# Type checking with MyPy
poetry run mypy backend/ tests/

# Format code (if using Ruff formatter)
poetry run ruff format backend/ tests/
```

### 4. Docker Deployment

#### Build Docker Image

```bash
# Build the Docker image
docker build -t greg-mvp:latest .
```

#### Run with Docker

```bash
# Run the containerized application
docker run -p 8000:8000 greg-mvp:latest

# Or run in background
docker run -d -p 8000:8000 --name greg-mvp greg-mvp:latest

# Check logs
docker logs greg-mvp

# Stop the container
docker stop greg-mvp
```

#### Test Docker Deployment

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# View API docs
open http://localhost:8000/docs
```

## Project Structure

```
greg-mvp/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py            # FastAPI app and configuration
│   │   ├── models.py          # Pydantic models
│   │   └── routers/           # API route handlers
│   │       ├── health.py      # Health check endpoint
│   │       ├── knowledge.py   # Knowledge base endpoints
│   │       ├── query.py       # Query processing endpoints
│   │       └── visualization.py # Visualization suggestion endpoints
├── tests/                     # Test suite
│   ├── conftest.py           # Test configuration
│   ├── test_health.py        # Health endpoint tests
│   ├── test_knowledge.py     # Knowledge endpoint tests
│   ├── test_query.py         # Query endpoint tests
│   ├── test_main.py          # Main app tests
│   └── test_visualization.py # Visualization endpoint tests
├── legacy/                    # Original Node.js implementation (preserved)
├── .github/workflows/         # GitHub Actions CI/CD
├── Dockerfile                 # Docker configuration
├── pyproject.toml            # Poetry configuration and tool settings
└── README.md                 # This file
```

## Development Workflow

### Running Locally

1. **Start the server**: `poetry run uvicorn backend.app.main:app --reload`
2. **Run tests**: `poetry run pytest`
3. **Check code quality**: `poetry run ruff check backend/ tests/`
4. **Type checking**: `poetry run mypy backend/ tests/`

### Adding New Features

1. Create new route handlers in `backend/app/routers/`
2. Define Pydantic models in `backend/app/models.py`
3. Add tests in the `tests/` directory
4. Update documentation as needed

### Before Committing

```bash
# Ensure all checks pass
poetry run ruff check backend/ tests/
poetry run mypy backend/ tests/  
poetry run pytest tests/ -v
```

## Configuration

The application uses environment variables for configuration:

- `PORT`: Server port (default: 8000)
- `ENVIRONMENT`: Environment mode (development/production)

Create a `.env` file for local development:

```env
PORT=8000
ENVIRONMENT=development
```

## API Usage Examples

### Query Natural Language Questions

```python
import requests

response = requests.post('http://localhost:8000/api/query', json={
    'question': 'How many active users do we have by country?'
})
result = response.json()
print(f"SQL: {result['sql']}")
print(f"Explanation: {result['explanation']}")
```

### Get Visualization Suggestions

```python
import requests

response = requests.post('http://localhost:8000/api/visualization-suggestions', json={
    'query': 'SELECT date, revenue FROM sales WHERE date >= "2024-01-01"'
})
suggestions = response.json()['suggestions']
for suggestion in suggestions:
    print(f"{suggestion['type']}: {suggestion['title']} (confidence: {suggestion['confidence']})")
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is part of the Greg MVP initiative.

---

For more information, visit the [API documentation](http://localhost:8000/docs) when running locally.
