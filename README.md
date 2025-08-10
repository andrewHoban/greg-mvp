# MVP Data Interrogation Tool

An internal MVP for Product Managers to:
- Ask natural language questions about core data domains
- Get an explainable SQL proposal
- Run queries (mock now, real BigQuery later)
- Visualise results quickly
- Draft a PRD in Markdown

## Stack
- Frontend: Next.js (React, TypeScript)
- Backend: FastAPI (Python 3.11)
- Data: BigQuery (mocked for MVP)
- Visualization: chart.js (via react-chartjs-2)
- Knowledge base: YAML (hardcoded)
- Future: Okta SSO, LLM provider (OpenAI/Gemini), PDF doc search

## Quick Start (Local)

Prereqs:
- Docker & docker-compose
- (Optional) Python 3.11 + Node 20 if running without Docker

```bash
cp .env.example .env
docker-compose up --build
```

Frontend: http://localhost:3000  
Backend docs (Swagger): http://localhost:8000/docs

## Environment Variables (.env)
| Variable | Description | Example |
|----------|-------------|---------|
| APP_ENV | runtime environment | dev |
| LLM_PROVIDER | stub value | mock |
| LLM_API_KEY | future use | sk-... |
| BIGQUERY_PROJECT | future real BQ project | my-project |
| BIGQUERY_USE_MOCK | "true" or "false" | true |

## Replacing Mock BigQuery
1. Set BIGQUERY_USE_MOCK=false
2. Add Google Application Credentials (mount JSON or use workload identity in GCP)
3. Implement run_sql_real in services/bigquery.py

## NLQ → SQL
Currently uses hardcoded patterns. Extend in:
`backend/app/services/nlp_to_sql.py`
Add a real provider by implementing:
`backend/app/services/llm/providers/base.py` (see stub)

## Conversation Context
A simple in-memory store (conversation_memory.py) for continuity. For production replace with Redis/Postgres.

## PRD Drafting
Client-side Markdown editing + preview. Future: add backend persistence & export to PDF/DOCX.

## Tests
Basic structure in `backend/tests`. Run:
```bash
docker exec -it mvp-backend pytest
```

## Roadmap (Next)
1. Integrate real BigQuery
2. Add authentication (Okta → OIDC)
3. Swap NLQ→SQL to LLM provider (with guardrails)
4. Persist conversation + PRD drafts (Postgres)
5. Add doc/PDF semantic search microservice
6. Role-based access / field masking
7. Query cost estimation and safety checks

## License
Internal / Proprietary.