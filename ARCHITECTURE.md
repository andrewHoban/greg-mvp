# Architecture

## Overview
This FastAPI service converts a natural language question into a rudimentary SQL plan, executes (mock), and produces visualization suggestions.

## Components
- Routers: health, knowledge, query, viz
- Services:
  - knowledge_base: loads table metadata from YAML
  - nl_sql_pipeline: (placeholder) derives a simple plan
  - sql_executor: mock execution
  - viz_suggester: basic visualization suggestion
- Models: QueryRequest, QueryPlan, QueryResponse, VisualizationSuggestions
- Domain Data: YAML file describing tables
- Tests: endpoint smoke tests

## Data Flow
User question -> /query -> Pipeline builds QueryPlan -> (optional execution) -> Response (+ optional /viz/suggest for viz hints).

## Limitations
- No real DB connection
- Extremely naive NL parsing
- Static schema
- Minimal error handling
