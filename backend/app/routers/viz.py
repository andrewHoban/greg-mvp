"""
Visualization suggestion endpoints
"""

from fastapi import APIRouter

from ..logging import get_logger
from ..models.query_models import VisualizationRequest, VisualizationSuggestion
from ..services.viz_suggester import VizSuggester

logger = get_logger(__name__)

router = APIRouter(prefix="/viz", tags=["visualization"])

# Initialize visualization suggester
viz_suggester = VizSuggester()


@router.post("/suggest", response_model=VisualizationSuggestion)
async def suggest_visualizations(
    request: VisualizationRequest
) -> VisualizationSuggestion:
    """
    Suggest chart types and configurations based on field metadata.
    
    Args:
        request: Field metadata and optional context
        
    Returns:
        Visualization suggestions with reasoning
    """
    logger.info(f"Generating visualization suggestions for {len(request.fields)} fields")
    
    # Generate suggestions using the viz suggester
    suggestions = viz_suggester.suggest_visualizations(
        fields=request.fields,
        context=request.context
    )
    
    logger.info(f"Generated {len(suggestions.suggestions)} visualization suggestions")
    
    return suggestions