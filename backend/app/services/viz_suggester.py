from typing import Any, Dict, List


class VizSuggester:
    """Visualization suggester with Plotly specs."""
    
    def suggest(self, fields: List[str]) -> Dict[str, Any]:
        """Suggest visualizations based on field types."""
        chart_types = self._determine_chart_types(fields)
        figure = self._create_basic_plotly_figure(fields, chart_types[0] if chart_types else "bar")
        
        return {
            "chart_types": chart_types,
            "figure": figure
        }
    
    def _determine_chart_types(self, fields: List[str]) -> List[str]:
        """Determine appropriate chart types for given fields."""
        field_names_lower = [f.lower() for f in fields]
        
        # Simple heuristics based on field names
        suggested_types = []
        
        if any(word in ' '.join(field_names_lower) for word in ['date', 'time', 'month', 'day']):
            suggested_types.extend(["line", "bar"])
        
        if any(
            word in " ".join(field_names_lower)
            for word in ["count", "total", "amount", "revenue"]
        ):
            suggested_types.extend(["bar", "pie"])
        
        if any(word in ' '.join(field_names_lower) for word in ['country', 'region', 'category']):
            suggested_types.extend(["bar", "pie"])
        
        return suggested_types or ["bar", "scatter"]
    
    def _create_basic_plotly_figure(self, fields: List[str], chart_type: str) -> Dict[str, Any]:
        """Create basic Plotly figure specification."""
        return {
            "data": [{
                "type": chart_type,
                "x": ["Sample 1", "Sample 2", "Sample 3"],
                "y": [10, 20, 15],
                "name": "Sample Data"
            }],
            "layout": {
                "title": f"Visualization for {', '.join(fields)}",
                "xaxis": {"title": fields[0] if fields else "X Axis"},
                "yaxis": {"title": fields[1] if len(fields) > 1 else "Y Axis"}
            }
        }