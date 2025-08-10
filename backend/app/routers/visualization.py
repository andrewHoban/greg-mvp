"""Visualization suggestion router."""

from fastapi import APIRouter

from backend.app.models import (
    VisualizationRequest,
    VisualizationResponse,
    VisualizationSuggestion,
    VisualizationType,
)

router = APIRouter()


@router.post("/visualization-suggestions", response_model=VisualizationResponse)
async def get_visualization_suggestions(
    request: VisualizationRequest,
) -> VisualizationResponse:
    """Get visualization suggestions based on query or data."""
    query = request.query.lower()
    suggestions = []

    # Mock logic for visualization suggestions
    if "count" in query or "sum" in query:
        suggestions.extend([
            VisualizationSuggestion(
                type=VisualizationType.BAR_CHART,
                title="Bar Chart",
                description="Show counts or sums as bars for easy comparison",
                config={"x_axis": "category", "y_axis": "value"},
                confidence=0.9,
            ),
            VisualizationSuggestion(
                type=VisualizationType.PIE_CHART,
                title="Pie Chart",
                description="Show proportions of the total",
                config={"label_field": "category", "value_field": "value"},
                confidence=0.7,
            ),
        ])

    if "time" in query or "date" in query or "trend" in query:
        suggestions.append(
            VisualizationSuggestion(
                type=VisualizationType.LINE_CHART,
                title="Line Chart",
                description="Show trends over time",
                config={"x_axis": "date", "y_axis": "value"},
                confidence=0.95,
            ),
        )

    if "group by" in query or "country" in query or "category" in query:
        suggestions.extend([
            VisualizationSuggestion(
                type=VisualizationType.BAR_CHART,
                title="Grouped Bar Chart",
                description="Compare values across categories",
                config={"x_axis": "category", "y_axis": "value", "group_by": True},
                confidence=0.85,
            ),
            VisualizationSuggestion(
                type=VisualizationType.TABLE,
                title="Data Table",
                description="Show detailed breakdown in tabular format",
                config={"sortable": True, "filterable": True},
                confidence=0.8,
            ),
        ])

    # Default suggestion if no specific patterns detected
    if not suggestions:
        suggestions.append(
            VisualizationSuggestion(
                type=VisualizationType.TABLE,
                title="Data Table",
                description="Show raw data in table format",
                config={"sortable": True},
                confidence=0.6,
            ),
        )

    # Sort by confidence and limit to top 3
    suggestions.sort(key=lambda x: x.confidence, reverse=True)
    suggestions = suggestions[:3]

    return VisualizationResponse(suggestions=suggestions)
