from fastapi import APIRouter

from backend.app.models.query_models import VisualizationRequest, VisualizationSuggestion
from backend.app.services.viz_suggester import VizSuggester

router = APIRouter(prefix="/viz")


@router.post("/suggest", response_model=VisualizationSuggestion)
async def suggest_visualization(request: VisualizationRequest):
    """Suggest visualizations for given fields."""
    suggester = VizSuggester()
    result = suggester.suggest(request.fields)
    return VisualizationSuggestion(**result)