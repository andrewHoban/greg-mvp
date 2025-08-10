# NL→SQL FastAPI Service

## Quick Start
Install dependencies (Poetry assumed):
```
poetry install
poetry run uvicorn backend.app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive API docs.

## Endpoints
- GET /health
- GET /knowledge/tables
- GET /knowledge/schema
- POST /query (QueryRequest)
- POST /viz/suggest (QueryPlan)

## Example Query
```
curl -X POST http://127.0.0.1:8000/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "How many rows?", "preview_only": false}'
```

## Tests
```
poetry run pytest -q
```

## Next Enhancements
See ROADMAP.md
