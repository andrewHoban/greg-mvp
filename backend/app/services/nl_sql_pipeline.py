"""
Natural language to SQL pipeline service.

This is currently a stub implementation with deterministic responses.
In the future, this will integrate with LLM services for actual NL-to-SQL generation.
"""
import re
from typing import List
from loguru import logger

from ..models.query_models import NLQueryRequest, ProposedQuery
from .knowledge_base import KnowledgeBase


class NLSQLPipeline:
    """Service for converting natural language to SQL queries."""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
    
    async def generate_sql(self, request: NLQueryRequest) -> ProposedQuery:
        """
        Generate SQL query from natural language request.
        
        Currently returns deterministic stub responses based on keywords.
        TODO: Integrate with actual LLM service (OpenAI, Anthropic, etc.)
        """
        logger.info(f"Processing NL query: {request.question}")
        
        question_lower = request.question.lower()
        
        # Simple keyword-based routing to demonstrate different domains
        if any(word in question_lower for word in ['revenue', 'sales', 'money', 'transaction', 'subscription']):
            return self._generate_finance_query(request)
        elif any(word in question_lower for word in ['read', 'article', 'content', 'view']):
            return self._generate_reads_query(request)
        elif any(word in question_lower for word in ['ticket', 'support', 'customer', 'agent']):
            return self._generate_support_query(request)
        else:
            return self._generate_default_query(request)
    
    def _generate_finance_query(self, request: NLQueryRequest) -> ProposedQuery:
        """Generate a finance-related query stub."""
        if 'month' in request.question.lower():
            sql = """
            SELECT 
                DATE_TRUNC(transaction_date, MONTH) as month,
                SUM(amount) as total_revenue
            FROM transactions 
            WHERE status = 'completed'
            GROUP BY month 
            ORDER BY month DESC
            """.strip()
            explanation = "This query calculates total revenue by month from completed transactions, showing the most recent months first."
            tables_used = ["transactions"]
        else:
            sql = """
            SELECT 
                plan_name,
                COUNT(*) as subscriber_count,
                SUM(monthly_amount) as total_monthly_revenue
            FROM subscriptions 
            WHERE end_date IS NULL
            GROUP BY plan_name 
            ORDER BY total_monthly_revenue DESC
            """.strip()
            explanation = "This query shows active subscription plans with subscriber counts and total monthly revenue."
            tables_used = ["subscriptions"]
        
        return ProposedQuery(
            sql=sql,
            explanation=explanation,
            tables_used=tables_used,
            warnings=["This is a stub implementation for demonstration purposes"]
        )
    
    def _generate_reads_query(self, request: NLQueryRequest) -> ProposedQuery:
        """Generate a reads-related query stub."""
        sql = """
        SELECT 
            a.category,
            COUNT(r.user_id) as read_count,
            AVG(r.read_duration_seconds) as avg_duration_seconds,
            AVG(r.completion_percentage) as avg_completion_pct
        FROM user_reads r
        LEFT JOIN articles a ON r.article_id = a.article_id
        GROUP BY a.category
        ORDER BY read_count DESC
        """.strip()
        
        return ProposedQuery(
            sql=sql,
            explanation="This query analyzes reading patterns by article category, showing read counts, average duration, and completion rates.",
            tables_used=["user_reads", "articles"],
            warnings=["This is a stub implementation for demonstration purposes"]
        )
    
    def _generate_support_query(self, request: NLQueryRequest) -> ProposedQuery:
        """Generate a support-related query stub."""
        sql = """
        SELECT 
            category,
            COUNT(*) as ticket_count,
            AVG(TIMESTAMP_DIFF(resolved_at, created_at, HOUR)) as avg_resolution_hours
        FROM support_tickets 
        WHERE status = 'resolved'
        GROUP BY category
        ORDER BY ticket_count DESC
        """.strip()
        
        return ProposedQuery(
            sql=sql,
            explanation="This query shows support ticket volume and average resolution times by category.",
            tables_used=["support_tickets"],
            warnings=["This is a stub implementation for demonstration purposes"]
        )
    
    def _generate_default_query(self, request: NLQueryRequest) -> ProposedQuery:
        """Generate a default query when no specific domain is detected."""
        sql = """
        SELECT 
            'general' as category,
            COUNT(*) as record_count,
            CURRENT_TIMESTAMP() as generated_at
        FROM (SELECT 1) as dummy
        """.strip()
        
        return ProposedQuery(
            sql=sql,
            explanation="This is a default query generated when the request doesn't match specific domain keywords.",
            tables_used=["dummy"],
            warnings=[
                "This is a stub implementation for demonstration purposes",
                "Could not detect specific domain from question"
            ]
        )