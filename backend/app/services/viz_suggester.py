"""
Visualization suggestion service with simple heuristics
"""

from typing import List

from ..logging import get_logger
from ..models.query_models import FieldMetadata, VisualizationSuggestion, ChartSpec

logger = get_logger(__name__)


class VizSuggester:
    """Simple heuristic-based visualization suggester."""
    
    def __init__(self) -> None:
        """Initialize the visualization suggester."""
        logger.info("Initializing visualization suggester")
    
    def suggest_visualizations(
        self, 
        fields: List[FieldMetadata], 
        context: str = None
    ) -> VisualizationSuggestion:
        """
        Suggest visualizations based on field metadata and context.
        
        Args:
            fields: List of field metadata
            context: Optional context about the data
            
        Returns:
            Visualization suggestions with reasoning
        """
        logger.info(f"Generating visualization suggestions for {len(fields)} fields")
        
        suggestions = []
        reasoning_parts = []
        
        # Categorize fields
        numeric_fields = [f for f in fields if f.type in ["NUMERIC", "INTEGER", "FLOAT", "DECIMAL"]]
        date_fields = [f for f in fields if f.type in ["DATE", "DATETIME", "TIMESTAMP"]]
        categorical_fields = [f for f in fields if f.type in ["STRING", "TEXT"] and f.semantic_role != "key"]
        key_fields = [f for f in fields if f.semantic_role == "key"]
        
        # Time series suggestions
        if date_fields and numeric_fields:
            for date_field in date_fields:
                for numeric_field in numeric_fields:
                    suggestions.append(ChartSpec(
                        chart_type="line",
                        x_axis=date_field.name,
                        y_axis=numeric_field.name,
                        config={
                            "title": f"{numeric_field.name} over time",
                            "xaxis_title": date_field.name,
                            "yaxis_title": numeric_field.name
                        }
                    ))
            reasoning_parts.append("Line charts suggested for time series analysis")
        
        # Categorical comparisons
        if categorical_fields and numeric_fields:
            for cat_field in categorical_fields[:2]:  # Limit to prevent too many suggestions
                for num_field in numeric_fields[:2]:
                    suggestions.append(ChartSpec(
                        chart_type="bar",
                        x_axis=cat_field.name,
                        y_axis=num_field.name,
                        config={
                            "title": f"{num_field.name} by {cat_field.name}",
                            "xaxis_title": cat_field.name,
                            "yaxis_title": num_field.name
                        }
                    ))
            reasoning_parts.append("Bar charts suggested for categorical comparisons")
        
        # Distribution analysis
        if len(numeric_fields) >= 1:
            for num_field in numeric_fields[:2]:
                suggestions.append(ChartSpec(
                    chart_type="histogram",
                    x_axis=num_field.name,
                    config={
                        "title": f"Distribution of {num_field.name}",
                        "xaxis_title": num_field.name,
                        "yaxis_title": "Count"
                    }
                ))
            reasoning_parts.append("Histograms suggested for distribution analysis")
        
        # Correlation analysis for multiple numeric fields
        if len(numeric_fields) >= 2:
            suggestions.append(ChartSpec(
                chart_type="scatter",
                x_axis=numeric_fields[0].name,
                y_axis=numeric_fields[1].name,
                color=categorical_fields[0].name if categorical_fields else None,
                config={
                    "title": f"{numeric_fields[1].name} vs {numeric_fields[0].name}",
                    "xaxis_title": numeric_fields[0].name,
                    "yaxis_title": numeric_fields[1].name
                }
            ))
            reasoning_parts.append("Scatter plot suggested for correlation analysis")
        
        # Composition analysis for categorical data
        if len(categorical_fields) >= 1 and len(numeric_fields) >= 1:
            suggestions.append(ChartSpec(
                chart_type="pie",
                color=categorical_fields[0].name,
                config={
                    "title": f"Composition by {categorical_fields[0].name}",
                    "values": numeric_fields[0].name
                }
            ))
            reasoning_parts.append("Pie chart suggested for composition analysis")
        
        # Default suggestion if no specific patterns found
        if not suggestions:
            if fields:
                suggestions.append(ChartSpec(
                    chart_type="table",
                    config={
                        "title": "Data Table",
                        "columns": [f.name for f in fields]
                    }
                ))
                reasoning_parts.append("Table view suggested as fallback visualization")
        
        # Combine reasoning
        reasoning = ". ".join(reasoning_parts) if reasoning_parts else "Basic visualizations suggested based on field types"
        
        logger.info(f"Generated {len(suggestions)} visualization suggestions")
        
        return VisualizationSuggestion(
            suggestions=suggestions,
            reasoning=reasoning
        )