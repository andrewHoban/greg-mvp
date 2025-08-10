from fastapi import FastAPI
from .logging_config import configure_logging
from .config import settings
from .errors import DomainError, domain_error_handler, unhandled_error_handler
from .routers import health, knowledge, query, viz

def create_app() -> FastAPI:
    configure_logging(settings.log_level)
    app = FastAPI(title="NL→SQL Service", version="0.1.0")
    app.include_router(health.router)
    app.include_router(knowledge.router)
    app.include_router(query.router)
    app.include_router(viz.router)
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
    return app

app = create_app()
