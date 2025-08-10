from fastapi import APIRouter

from backend.app.models.query_models import (
    VisualizationRequest,
    VisualizationResponse,
    VisualizationSuggestion,
)
from backend.app.services.viz_suggester import VisualizationSuggester

router = APIRouter(prefix="/viz", tags=["Visualization"])


@router.post("/suggest", response_model=VisualizationResponse)
async def suggest_visualizations(
    request: VisualizationRequest
) -> VisualizationResponse:
    """
    Suggest appropriate visualizations for query result data.
    
    This endpoint analyzes the structure and content of query results
    and suggests appropriate chart types and visualizations.
    """
    suggester = VisualizationSuggester()

    # Convert the request data to a format the suggester expects
    data = {
        "rows": request.data.rows,
        "columns": request.data.columns,
        "row_count": request.data.row_count
    }

    result = suggester.suggest(data)

    # Convert suggestions to Pydantic models
    suggestions = [
        VisualizationSuggestion(
            chart_type=s["chart_type"],
            title=s["title"],
            description=s["description"],
            recommended=s["recommended"]
        )
        for s in result["suggestions"]
    ]

    return VisualizationResponse(
        suggestions=suggestions,
        sample_figure=result["sample_figure"],
        total_suggestions=result["total_suggestions"]
    )
