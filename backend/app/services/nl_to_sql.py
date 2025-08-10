"""Natural Language to SQL conversion service."""

from typing import NamedTuple

from loguru import logger

from backend.app.services.knowledge_base import KnowledgeBase


class NLToSQLResult(NamedTuple):
    """Result from NL to SQL conversion."""

    proposed_sql: str
    explanation: str
    referenced_domains: list[str]


class NLToSQLService:
    """Service for converting natural language questions to SQL queries."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base

    def process_question(self, question: str) -> NLToSQLResult:
        """
        Convert a natural language question to SQL.

        This is a stub implementation that returns a deterministic SQL query
        for revenue-related questions. In production, this would use an LLM
        or other advanced NL processing.
        """
        logger.info(f"Processing question: {question}")

        # Find relevant domains
        relevant_domains = self.knowledge_base.find_relevant_domains(question)
        logger.info(f"Found relevant domains: {relevant_domains}")

        # For MVP, return deterministic SQL for revenue questions
        # TODO: Implement actual NL to SQL conversion using LLM
        proposed_sql = self._generate_stub_sql(question)
        explanation = self._generate_explanation(question, proposed_sql)

        return NLToSQLResult(
            proposed_sql=proposed_sql,
            explanation=explanation,
            referenced_domains=relevant_domains,
        )

    def _generate_stub_sql(self, question: str) -> str:
        """Generate a stub SQL query based on the question."""
        question_lower = question.lower()

        # Revenue-related questions get the deterministic query from requirements
        if any(
            keyword in question_lower
            for keyword in ["revenue", "sales", "money", "earning", "income"]
        ):
            return """SELECT DATE_TRUNC(created_at, MONTH) AS month,
       SUM(amount) AS total_revenue
FROM financials_transactions
GROUP BY month
ORDER BY month"""

        # Customer-related questions
        elif any(
            keyword in question_lower for keyword in ["customer", "user", "client"]
        ):
            return """SELECT customer_id,
       COUNT(*) AS interaction_count,
       AVG(satisfaction_score) AS avg_satisfaction
FROM customer_care_tickets
GROUP BY customer_id
ORDER BY interaction_count DESC
LIMIT 100"""

        # Content/engagement questions
        elif any(
            keyword in question_lower
            for keyword in ["content", "article", "read", "engagement"]
        ):
            return """SELECT content_id,
       title,
       read_count,
       engagement_score
FROM reads_content
ORDER BY engagement_score DESC
LIMIT 100"""

        # Default fallback
        else:
            return """SELECT DATE_TRUNC(created_at, MONTH) AS month,
       SUM(amount) AS total_revenue
FROM financials_transactions
GROUP BY month
ORDER BY month"""

    def _generate_explanation(self, question: str, sql: str) -> str:
        """Generate an explanation for the SQL query."""
        question_lower = question.lower()

        if "revenue" in question_lower:
            return (
                "This query analyzes revenue trends by month. It groups financial transactions "
                "by month using DATE_TRUNC and sums the transaction amounts to show total "
                "revenue per month, ordered chronologically."
            )

        elif "customer" in question_lower:
            return (
                "This query analyzes customer interactions by counting tickets per customer "
                "and calculating their average satisfaction score, showing the most active "
                "customers first."
            )

        elif "content" in question_lower or "read" in question_lower:
            return (
                "This query shows content performance by displaying articles with their "
                "read counts and engagement scores, ordered by engagement level."
            )

        else:
            return (
                "This is a default revenue analysis query that shows monthly revenue trends "
                "from financial transactions, grouped by month and ordered chronologically."
            )
