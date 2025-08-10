"""
Visualization suggestion service.

This service provides chart type suggestions based on data characteristics
and generates basic Plotly specifications.
"""
from typing import Any, Dict, List
from loguru import logger

from ..models.query_models import VisualizationRequest, VisualizationSpec


class VizSuggester:
    """Service for suggesting visualizations based on data characteristics."""
    
    def suggest_visualizations(
        self, 
        request: VisualizationRequest
    ) -> VisualizationSpec:
        """
        Suggest appropriate visualizations for the given data summary.
        
        This is currently a heuristic-based implementation.
        Future versions could use ML models or more sophisticated analysis.
        """
        logger.info("Generating visualization suggestions")
        
        data_summary = request.data_summary
        columns = data_summary.get('columns', [])
        sample_row = data_summary.get('sample_row', [])
        
        # Analyze column types and patterns
        suggestions = self._analyze_columns_for_charts(columns, sample_row)
        
        # Generate a basic Plotly spec for the first suggestion
        plotly_spec = None
        if suggestions:
            plotly_spec = self._generate_plotly_spec(
                suggestions[0], 
                columns, 
                sample_row,
                data_summary
            )
        
        reasoning = self._generate_reasoning(columns, suggestions)
        
        return VisualizationSpec(
            suggested_charts=suggestions,
            plotly_spec=plotly_spec,
            reasoning=reasoning
        )
    
    def _analyze_columns_for_charts(
        self, 
        columns: List[str], 
        sample_row: List[Any]
    ) -> List[str]:
        """Analyze columns to suggest appropriate chart types."""
        suggestions = []
        
        if not columns or not sample_row:
            return ["table"]  # Default to table view
        
        # Count numeric vs text columns
        numeric_cols = 0
        date_cols = 0
        category_cols = 0
        
        for i, col in enumerate(columns):
            if i < len(sample_row):
                value = sample_row[i]
                col_lower = col.lower()
                
                if isinstance(value, (int, float)):
                    numeric_cols += 1
                elif 'date' in col_lower or 'time' in col_lower:
                    date_cols += 1
                else:
                    category_cols += 1
        
        # Suggest charts based on column composition
        if date_cols > 0 and numeric_cols > 0:
            suggestions.extend(["line", "area"])
        
        if category_cols > 0 and numeric_cols > 0:
            suggestions.extend(["bar", "horizontal_bar"])
        
        if numeric_cols >= 2:
            suggestions.extend(["scatter", "bubble"])
        
        if category_cols > 0:
            suggestions.extend(["pie", "donut"])
        
        if len(columns) > 3:
            suggestions.append("heatmap")
        
        # Always include table as fallback
        if "table" not in suggestions:
            suggestions.append("table")
        
        return suggestions[:5]  # Limit to top 5 suggestions
    
    def _generate_plotly_spec(
        self, 
        chart_type: str, 
        columns: List[str], 
        sample_row: List[Any],
        data_summary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a basic Plotly figure specification."""
        
        if chart_type == "bar":
            return {
                "data": [{
                    "type": "bar",
                    "x": ["Category A", "Category B", "Category C", "Category D"],
                    "y": [25, 30, 22, 28],
                    "name": "Sample Data"
                }],
                "layout": {
                    "title": "Sample Bar Chart",
                    "xaxis": {"title": columns[0] if columns else "Category"},
                    "yaxis": {"title": columns[1] if len(columns) > 1 else "Value"}
                }
            }
        
        elif chart_type == "line":
            return {
                "data": [{
                    "type": "scatter",
                    "mode": "lines+markers",
                    "x": ["2024-01", "2024-02", "2024-03", "2024-04"],
                    "y": [125000, 132000, 128500, 145000],
                    "name": "Time Series"
                }],
                "layout": {
                    "title": "Sample Line Chart",
                    "xaxis": {"title": "Time Period"},
                    "yaxis": {"title": "Value"}
                }
            }
        
        elif chart_type == "scatter":
            return {
                "data": [{
                    "type": "scatter",
                    "mode": "markers",
                    "x": [1, 2, 3, 4, 5],
                    "y": [10, 11, 12, 13, 14],
                    "name": "Data Points"
                }],
                "layout": {
                    "title": "Sample Scatter Plot",
                    "xaxis": {"title": columns[0] if columns else "X Axis"},
                    "yaxis": {"title": columns[1] if len(columns) > 1 else "Y Axis"}
                }
            }
        
        elif chart_type == "pie":
            return {
                "data": [{
                    "type": "pie",
                    "labels": ["Segment A", "Segment B", "Segment C"],
                    "values": [45, 35, 20],
                    "name": "Distribution"
                }],
                "layout": {
                    "title": "Sample Pie Chart"
                }
            }
        
        else:
            # Default table representation
            return {
                "data": [{
                    "type": "table",
                    "header": {"values": columns},
                    "cells": {"values": [[sample_row[i] if i < len(sample_row) else ""] for i in range(len(columns))]}
                }],
                "layout": {
                    "title": "Data Table"
                }
            }
    
    def _generate_reasoning(self, columns: List[str], suggestions: List[str]) -> str:
        """Generate reasoning for chart suggestions."""
        if not suggestions:
            return "Unable to generate chart suggestions due to insufficient data information."
        
        reasoning_parts = [
            f"Based on the data structure with {len(columns)} columns, "
        ]
        
        if "line" in suggestions:
            reasoning_parts.append("line charts work well for time series data; ")
        
        if "bar" in suggestions:
            reasoning_parts.append("bar charts are effective for categorical comparisons; ")
        
        if "scatter" in suggestions:
            reasoning_parts.append("scatter plots can reveal correlations between numeric variables; ")
        
        if "pie" in suggestions:
            reasoning_parts.append("pie charts show proportional relationships; ")
        
        reasoning_parts.append(f"The top suggestion is a {suggestions[0]} chart.")
        
        return "".join(reasoning_parts)