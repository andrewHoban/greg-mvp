"""Query endpoint router."""

from fastapi import APIRouter

from backend.app.models import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest) -> QueryResponse:
    """Process natural language query and generate SQL."""
    # Mock implementation - in real version, integrate with AI service
    question = request.question.lower()

    # Simple keyword-based mock SQL generation
    if "users" in question and "count" in question:
        mock_sql = "SELECT COUNT(*) FROM users;"
        explanation = "Counts total number of users in the database."
        confidence = 0.9
        visualizations = ["bar_chart", "table"]
    elif "revenue" in question:
        mock_sql = (
            "SELECT SUM(amount) as total_revenue FROM transactions "
            "WHERE date >= '2024-01-01';"
        )
        explanation = "Calculates total revenue from transactions this year."
        confidence = 0.85
        visualizations = ["line_chart", "bar_chart"]
    elif "signup" in question and "country" in question:
        mock_sql = (
            "SELECT country_code, COUNT(*) as signups FROM users "
            "GROUP BY country_code ORDER BY signups DESC;"
        )
        explanation = "Shows user signups grouped by country, ordered by count."
        confidence = 0.8
        visualizations = ["pie_chart", "bar_chart", "table"]
    else:
        mock_sql = "SELECT * FROM users LIMIT 10;"
        explanation = "Default query returning first 10 users (question not understood)."
        confidence = 0.3
        visualizations = ["table"]

    return QueryResponse(
        sql=mock_sql,
        explanation=explanation,
        confidence=confidence,
        suggested_visualizations=visualizations,
    )
