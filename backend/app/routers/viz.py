"""
Visualization endpoints for chart suggestions and generation.
"""
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from ..dependencies import get_current_user
from ..models.query_models import VisualizationRequest, VisualizationSpec
from ..services.viz_suggester import VizSuggester

router = APIRouter()


@router.post("/suggest", response_model=VisualizationSpec)
async def suggest_visualizations(
    request: VisualizationRequest,
    current_user: str = Depends(get_current_user)
) -> VisualizationSpec:
    """
    Suggest appropriate visualizations based on data characteristics.
    
    Returns suggested chart types and a basic Plotly specification.
    Frontend rendering would happen on the client side.
    """
    try:
        logger.info(f"Generating visualization suggestions for user {current_user}")
        
        # Initialize visualization suggester
        suggester = VizSuggester()
        
        # Generate suggestions
        suggestions = suggester.suggest_visualizations(request)
        
        logger.info(f"Generated {len(suggestions.suggested_charts)} chart suggestions")
        
        return suggestions
        
    except Exception as e:
        logger.error(f"Error generating visualization suggestions: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate visualization suggestions: {str(e)}"
        )