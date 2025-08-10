"""Visualization suggester service."""

from typing import Any, NamedTuple

from loguru import logger

from backend.app.models import ChartRecommendation


class VisualizationSuggesterResult(NamedTuple):
    """Result from visualization suggester."""

    recommendations: list[ChartRecommendation]
    plotly_config: dict[str, Any]


class VisualizationSuggesterService:
    """Service for suggesting appropriate visualizations."""

    def suggest_visualizations(
        self, sql: str, data_sample: list[dict[str, Any]] | None = None
    ) -> VisualizationSuggesterResult:
        """
        Suggest appropriate visualization types based on SQL query and optional data sample.

        Analyzes the query structure to recommend suitable chart types and provides
        a sample Plotly configuration.
        """
        logger.info("Generating visualization suggestions")

        # Analyze SQL query to determine data structure
        sql_lower = sql.lower()
        recommendations = self._analyze_query_for_charts(sql_lower)

        # Generate sample Plotly configuration
        plotly_config = self._generate_plotly_config(
            sql_lower, recommendations[0].chart_type if recommendations else "bar"
        )

        return VisualizationSuggesterResult(
            recommendations=recommendations, plotly_config=plotly_config
        )

    def _analyze_query_for_charts(self, sql: str) -> list[ChartRecommendation]:
        """Analyze SQL query to suggest appropriate chart types."""
        recommendations = []

        # Time series data (has date/time columns)
        if any(
            keyword in sql
            for keyword in ["date_trunc", "month", "day", "year", "created_at"]
        ):
            recommendations.append(
                ChartRecommendation(
                    chart_type="line",
                    reasoning="Time-based data is best displayed as a line chart to show trends over time",
                    priority=1,
                )
            )
            recommendations.append(
                ChartRecommendation(
                    chart_type="bar",
                    reasoning="Bar chart can effectively show values for each time period",
                    priority=2,
                )
            )

        # Aggregated data with GROUP BY
        elif "group by" in sql:
            if "count" in sql:
                recommendations.append(
                    ChartRecommendation(
                        chart_type="bar",
                        reasoning="Count data is well-suited for bar charts to compare quantities",
                        priority=1,
                    )
                )
                recommendations.append(
                    ChartRecommendation(
                        chart_type="pie",
                        reasoning="Pie chart can show proportional relationships for count data",
                        priority=2,
                    )
                )
            elif any(keyword in sql for keyword in ["sum", "avg", "average"]):
                recommendations.append(
                    ChartRecommendation(
                        chart_type="bar",
                        reasoning="Aggregated numeric data works well with bar charts for comparisons",
                        priority=1,
                    )
                )
                recommendations.append(
                    ChartRecommendation(
                        chart_type="scatter",
                        reasoning="Scatter plot can reveal correlations in aggregated data",
                        priority=3,
                    )
                )

        # Data with scores or ratings
        elif any(keyword in sql for keyword in ["score", "rating", "satisfaction"]):
            recommendations.append(
                ChartRecommendation(
                    chart_type="histogram",
                    reasoning="Score data distribution is best shown with histograms",
                    priority=1,
                )
            )
            recommendations.append(
                ChartRecommendation(
                    chart_type="box",
                    reasoning="Box plot shows score distribution and outliers effectively",
                    priority=2,
                )
            )

        # Default recommendations for other queries
        else:
            recommendations.append(
                ChartRecommendation(
                    chart_type="bar",
                    reasoning="Bar chart is a versatile choice for most data comparisons",
                    priority=1,
                )
            )
            recommendations.append(
                ChartRecommendation(
                    chart_type="table",
                    reasoning="Table format preserves all data details for analysis",
                    priority=2,
                )
            )

        return recommendations

    def _generate_plotly_config(
        self, sql: str, primary_chart_type: str
    ) -> dict[str, Any]:
        """Generate a sample Plotly configuration based on chart type."""

        if primary_chart_type == "line":
            return {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "x": ["2024-01", "2024-02", "2024-03", "2024-04"],
                        "y": [45000, 52000, 48000, 58000],
                        "name": "Revenue Trend",
                        "line": {"color": "#1f77b4", "width": 3},
                        "marker": {"size": 8},
                    }
                ],
                "layout": {
                    "title": "Revenue Trend Over Time",
                    "xaxis": {"title": "Month"},
                    "yaxis": {"title": "Total Revenue ($)"},
                    "showlegend": True,
                },
            }

        elif primary_chart_type == "bar":
            return {
                "data": [
                    {
                        "type": "bar",
                        "x": ["Jan", "Feb", "Mar", "Apr"],
                        "y": [45000, 52000, 48000, 58000],
                        "name": "Monthly Values",
                        "marker": {"color": "#2ca02c"},
                    }
                ],
                "layout": {
                    "title": "Monthly Performance",
                    "xaxis": {"title": "Period"},
                    "yaxis": {"title": "Value"},
                    "showlegend": True,
                },
            }

        elif primary_chart_type == "pie":
            return {
                "data": [
                    {
                        "type": "pie",
                        "labels": [
                            "Category A",
                            "Category B",
                            "Category C",
                            "Category D",
                        ],
                        "values": [30, 25, 25, 20],
                        "hole": 0.3,  # Donut chart
                    }
                ],
                "layout": {"title": "Distribution Breakdown", "showlegend": True},
            }

        elif primary_chart_type == "scatter":
            return {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "markers",
                        "x": [1, 2, 3, 4, 5],
                        "y": [10, 20, 15, 25, 18],
                        "name": "Data Points",
                        "marker": {"size": 10, "color": "#ff7f0e"},
                    }
                ],
                "layout": {
                    "title": "Correlation Analysis",
                    "xaxis": {"title": "X Variable"},
                    "yaxis": {"title": "Y Variable"},
                    "showlegend": True,
                },
            }

        else:  # Default fallback
            return {
                "data": [
                    {
                        "type": "bar",
                        "x": ["Item 1", "Item 2", "Item 3"],
                        "y": [10, 20, 15],
                        "marker": {"color": "#d62728"},
                    }
                ],
                "layout": {
                    "title": "Data Visualization",
                    "xaxis": {"title": "Categories"},
                    "yaxis": {"title": "Values"},
                },
            }
