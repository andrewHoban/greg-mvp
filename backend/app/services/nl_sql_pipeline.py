from typing import Dict

from backend.app.logging import get_logger_for_module

logger = get_logger_for_module(__name__)


class NLToSQLPipeline:
    """Natural Language to SQL Pipeline that generates deterministic SQL queries."""

    def __init__(self) -> None:
        """Initialize the NL to SQL pipeline."""
        logger.info("Initializing NL to SQL Pipeline")

    def generate(self, question: str) -> Dict[str, any]:
        """
        Generate SQL query from natural language question.
        
        Args:
            question: Natural language question
            
        Returns:
            Dictionary containing SQL, explanation, and referenced domains
        """
        logger.info(f"Processing question: {question}")

        # Deterministic logic based on question content
        if "revenue" in question.lower():
            sql = """
SELECT 
    DATE_TRUNC('month', transaction_date) as month,
    SUM(amount) as total_revenue,
    COUNT(*) as transaction_count
FROM transactions 
WHERE transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
GROUP BY month
ORDER BY month DESC
            """.strip()

            explanation = (
                "This query calculates monthly revenue by summing transaction amounts "
                "and counting transactions for the last 12 months, grouped by month."
            )

            referenced_domains = ["financials"]
        else:
            sql = "SELECT 1 as sample_value"
            explanation = "This is a simple test query that returns a constant value."
            referenced_domains = []

        result = {
            "proposed_sql": sql,
            "explanation": explanation,
            "referenced_domains": referenced_domains,
            "confidence_score": 0.95,
        }

        logger.info(f"Generated SQL query for question: {question[:50]}...")
        return result
