"""Visualization router."""

from fastapi import APIRouter
from loguru import logger

from backend.app.models import VisualizationRequest, VisualizationResponse
from backend.app.services.visualization_suggester import VisualizationSuggesterService

router = APIRouter()


@router.post("/suggest", response_model=VisualizationResponse)
async def suggest_visualization(
    request_data: VisualizationRequest,
) -> VisualizationResponse:
    """
    Suggest appropriate visualization types for the given SQL query.

    Analyzes the SQL query structure and optional data sample to recommend
    suitable chart types and provide a sample Plotly configuration.
    """
    logger.info("Generating visualization suggestions for SQL query")

    # Use visualization suggester service
    viz_service = VisualizationSuggesterService()
    result = viz_service.suggest_visualizations(
        request_data.sql, request_data.data_sample
    )

    logger.info(
        f"Generated {len(result.recommendations)} visualization recommendations"
    )

    return VisualizationResponse(
        recommendations=result.recommendations, plotly_config=result.plotly_config
    )
