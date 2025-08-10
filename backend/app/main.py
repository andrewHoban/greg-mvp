from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import nlp_to_sql, bigquery, prd, knowledge
from app.core.config import settings

app = FastAPI(title="MVP Data Interrogation Tool", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP; tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nlp_to_sql.router)
app.include_router(bigquery.router)
app.include_router(prd.router)
app.include_router(knowledge.router)

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.app_env}
