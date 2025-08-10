from fastapi import APIRouter
from ..models.query_models import QueryPlan, VisualizationSuggestions
from ..services.viz_suggester import VisualizationSuggester

router = APIRouter(prefix="/viz", tags=["visualization"])

@router.post("/suggest", response_model=VisualizationSuggestions)
def suggest(plan: QueryPlan) -> VisualizationSuggestions:
    return VisualizationSuggester().suggest(plan)
