from ..models.query_models import QueryPlan, VisualizationSuggestion, VisualizationSuggestions

class VisualizationSuggester:
    def suggest(self, plan: QueryPlan) -> VisualizationSuggestions:
        suggestions = [
            VisualizationSuggestion(
                title="Simple Metric",
                chart_type="single_value",
                x="",
                y=plan.metrics,
            )
        ]
        return VisualizationSuggestions(suggestions=suggestions)
