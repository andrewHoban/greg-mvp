"""
Natural Language to SQL Pipeline
This is a stub implementation that returns deterministic responses.
TODO: Integrate with actual NL-to-SQL service (e.g., LLM-based).
"""

from typing import Tuple

from ..logging import get_logger

logger = get_logger(__name__)


class NLToSQLPipeline:
    """Natural language to SQL conversion pipeline."""
    
    def __init__(self) -> None:
        """Initialize the pipeline."""
        logger.info("Initializing NL-to-SQL pipeline (stub implementation)")
    
    def generate(self, question: str) -> Tuple[str, str, list]:
        """
        Generate SQL and explanation from natural language question.
        
        Args:
            question: Natural language question
            
        Returns:
            Tuple of (sql_query, explanation, referenced_domains)
        """
        logger.info(f"Processing question: {question}")
        
        # TODO: Replace with actual NL-to-SQL implementation
        # This is a deterministic stub that returns a generic revenue query
        
        sql_query = """SELECT 
    DATE_TRUNC(created_at, MONTH) AS month,
    SUM(amount) AS total_revenue
FROM financials_transactions 
GROUP BY month 
ORDER BY month"""
        
        explanation = """This query analyzes revenue trends by month. It:
1. Groups financial transactions by month using DATE_TRUNC
2. Sums the 'amount' field to calculate total revenue per month  
3. Orders results chronologically by month
4. Uses the 'financials_transactions' table from the financials domain"""
        
        referenced_domains = ["financials"]
        
        logger.info(f"Generated SQL query with {len(referenced_domains)} referenced domains")
        
        return sql_query, explanation, referenced_domains