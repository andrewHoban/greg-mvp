"""SQL executor service for running queries."""

import random
from datetime import datetime, timedelta
from typing import Any, NamedTuple

from loguru import logger


class SQLExecutorResult(NamedTuple):
    """Result from SQL execution."""

    data: list[dict[str, Any]]
    warning: str | None = None


class SQLExecutorService:
    """Service for executing SQL queries."""

    def __init__(self) -> None:
        pass

    def execute_query(self, sql: str, limit: int | None = 100) -> SQLExecutorResult:
        """
        Execute SQL query and return results.

        This is a stub implementation that returns synthetic data.
        In production, this would connect to BigQuery or other database.
        """
        logger.info(f"Executing SQL query (limit: {limit})")

        # Generate synthetic data based on query type
        synthetic_data = self._generate_synthetic_data(sql, limit or 100)

        warning = (
            "⚠️ This is synthetic data for demo purposes. "
            "Production implementation will connect to actual BigQuery database."
        )

        return SQLExecutorResult(data=synthetic_data, warning=warning)

    def _generate_synthetic_data(self, sql: str, limit: int) -> list[dict[str, Any]]:
        """Generate synthetic data based on the SQL query structure."""
        sql_lower = sql.lower()

        # Revenue data
        if "total_revenue" in sql_lower and "month" in sql_lower:
            return self._generate_revenue_data(limit)

        # Customer data
        elif "customer_id" in sql_lower and "satisfaction" in sql_lower:
            return self._generate_customer_data(limit)

        # Content data
        elif "content_id" in sql_lower and "read_count" in sql_lower:
            return self._generate_content_data(limit)

        # Generic fallback
        else:
            return self._generate_revenue_data(limit)

    def _generate_revenue_data(self, limit: int) -> list[dict[str, Any]]:
        """Generate synthetic monthly revenue data."""
        data = []
        base_date = datetime(2024, 1, 1)
        base_revenue = 50000

        for i in range(min(limit, 12)):  # Up to 12 months
            month = base_date + timedelta(days=30 * i)
            # Add some realistic variation
            revenue = base_revenue + (i * 5000) + random.randint(-10000, 15000)

            data.append({"month": month.strftime("%Y-%m-%d"), "total_revenue": revenue})

        return data

    def _generate_customer_data(self, limit: int) -> list[dict[str, Any]]:
        """Generate synthetic customer interaction data."""
        data = []

        for i in range(min(limit, 50)):  # Up to 50 customers
            data.append(
                {
                    "customer_id": f"CUST_{1000 + i}",
                    "interaction_count": random.randint(1, 25),
                    "avg_satisfaction": round(random.uniform(3.0, 5.0), 2),
                }
            )

        # Sort by interaction count (descending)
        data.sort(key=lambda x: x["interaction_count"], reverse=True)
        return data

    def _generate_content_data(self, limit: int) -> list[dict[str, Any]]:
        """Generate synthetic content performance data."""
        sample_titles = [
            "Q4 Financial Performance Analysis",
            "Customer Satisfaction Trends",
            "Product Roadmap Update",
            "Market Research Insights",
            "Competitive Analysis Report",
            "User Engagement Metrics",
            "Revenue Growth Strategies",
            "Customer Retention Analysis",
            "Product Feature Usage Data",
            "Sales Performance Review",
        ]

        data = []

        for i in range(min(limit, len(sample_titles))):
            data.append(
                {
                    "content_id": f"CONTENT_{100 + i}",
                    "title": sample_titles[i],
                    "read_count": random.randint(50, 1000),
                    "engagement_score": round(random.uniform(0.1, 1.0), 3),
                }
            )

        # Sort by engagement score (descending)
        data.sort(key=lambda x: x["engagement_score"], reverse=True)
        return data
