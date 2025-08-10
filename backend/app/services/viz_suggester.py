from typing import Any, Dict, List

import plotly.express as px
import plotly.graph_objects as go

from backend.app.logging import get_logger_for_module

logger = get_logger_for_module(__name__)


class VisualizationSuggester:
    """Service for suggesting appropriate visualizations for query results."""

    def __init__(self) -> None:
        """Initialize the visualization suggester."""
        logger.info("Initializing Visualization Suggester")

    def suggest(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest appropriate visualizations for the given data.
        
        Args:
            data: Query result data with rows and columns
            
        Returns:
            Dictionary containing suggested chart types and sample plotly figure
        """
        rows = data.get("rows", [])
        columns = data.get("columns", [])

        logger.info(f"Suggesting visualizations for data with {len(rows)} rows and columns: {columns}")

        # Analyze data structure to suggest appropriate charts
        suggestions = []

        # If data has time-based columns, suggest time series
        if any("date" in col.lower() or "month" in col.lower() or "time" in col.lower() for col in columns):
            suggestions.append({
                "chart_type": "line",
                "title": "Time Series Chart",
                "description": "Best for showing trends over time",
                "recommended": True
            })
            suggestions.append({
                "chart_type": "bar",
                "title": "Bar Chart (Time)",
                "description": "Good for comparing values across time periods",
                "recommended": False
            })

        # If data has numeric columns, suggest various chart types
        numeric_cols = [col for col in columns if any(
            isinstance(row.get(col), (int, float)) for row in rows if row.get(col) is not None
        )]

        if len(numeric_cols) >= 2:
            suggestions.append({
                "chart_type": "scatter",
                "title": "Scatter Plot",
                "description": "Good for showing relationships between two numeric variables",
                "recommended": False
            })

        if len(numeric_cols) >= 1:
            suggestions.append({
                "chart_type": "histogram",
                "title": "Histogram",
                "description": "Shows distribution of numeric data",
                "recommended": False
            })

        # Default suggestions
        if not suggestions:
            suggestions.extend([
                {
                    "chart_type": "bar",
                    "title": "Bar Chart",
                    "description": "Good general-purpose chart for categorical data",
                    "recommended": True
                },
                {
                    "chart_type": "table",
                    "title": "Data Table",
                    "description": "Simple tabular display of data",
                    "recommended": False
                }
            ])

        # Generate a sample Plotly figure
        sample_figure = self._create_sample_figure(rows, columns)

        result = {
            "suggestions": suggestions,
            "sample_figure": sample_figure,
            "total_suggestions": len(suggestions)
        }

        logger.info(f"Generated {len(suggestions)} visualization suggestions")
        return result

    def _create_sample_figure(self, rows: List[Dict], columns: List[str]) -> Dict[str, Any]:
        """Create a sample Plotly figure based on the data."""
        if not rows or not columns:
            # Return empty figure
            fig = go.Figure()
            fig.update_layout(title="No Data Available")
            return fig.to_dict()

        # Try to create a meaningful chart based on data structure
        try:
            # If we have revenue data, create a revenue chart
            if "total_revenue" in columns and "month" in columns:
                fig = px.line(
                    x=[row["month"] for row in rows],
                    y=[row["total_revenue"] for row in rows],
                    title="Revenue Over Time",
                    labels={"x": "Month", "y": "Total Revenue"}
                )
            else:
                # Create a simple bar chart with the first two columns
                x_col = columns[0]
                y_col = columns[1] if len(columns) > 1 else columns[0]

                fig = px.bar(
                    x=[str(row[x_col]) for row in rows],
                    y=[row[y_col] if isinstance(row[y_col], (int, float)) else 1 for row in rows],
                    title=f"{y_col} by {x_col}",
                    labels={"x": x_col.title(), "y": y_col.title()}
                )

            return fig.to_dict()

        except Exception as e:
            logger.warning(f"Error creating sample figure: {e}")
            # Return simple empty figure
            fig = go.Figure()
            fig.update_layout(title="Sample Chart")
            return fig.to_dict()
