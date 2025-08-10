"""Knowledge endpoint router."""

from datetime import datetime

from fastapi import APIRouter, Query

from backend.app.models import KnowledgeItem, KnowledgeResponse

router = APIRouter()


@router.get("/knowledge", response_model=KnowledgeResponse)
async def get_knowledge(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    category: str | None = Query(None, description="Filter by category"),
) -> KnowledgeResponse:
    """Get knowledge base items."""
    # Mock data - in real implementation, this would query a database
    mock_items = [
        KnowledgeItem(
            id="1",
            title="SQL Query Best Practices",
            content="Best practices for writing efficient SQL queries...",
            category="sql",
            tags=["sql", "performance", "best-practices"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        KnowledgeItem(
            id="2",
            title="Data Visualization Guidelines",
            content="Guidelines for creating effective data visualizations...",
            category="visualization",
            tags=["charts", "design", "guidelines"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]

    # Filter by category if provided
    if category:
        mock_items = [item for item in mock_items if item.category == category]

    # Simple pagination (in real implementation, do this at the database level)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_items = mock_items[start_idx:end_idx]

    return KnowledgeResponse(
        items=paginated_items,
        total=len(mock_items),
        page=page,
        per_page=per_page,
    )
