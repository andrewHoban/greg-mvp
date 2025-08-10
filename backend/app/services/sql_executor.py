from typing import Any, Dict, Optional

from backend.app.logging import get_logger_for_module

logger = get_logger_for_module(__name__)


class SQLExecutor:
    """SQL Executor that returns synthetic data for testing and development."""

    def __init__(self) -> None:
        """Initialize the SQL executor."""
        logger.info("Initializing SQL Executor")

    def execute(self, sql: str, limit: Optional[int] = 100) -> Dict[str, Any]:
        """
        Execute SQL query and return synthetic results.
        
        Args:
            sql: SQL query to execute
            limit: Maximum number of rows to return
            
        Returns:
            Dictionary containing rows, columns, and metadata
        """
        logger.info(f"Executing SQL query: {sql[:100]}...")

        # Generate synthetic data based on SQL content
        if "revenue" in sql.lower() and "sum" in sql.lower():
            # Revenue query - return monthly revenue data
            rows = [
                {"month": "2024-01", "total_revenue": 125000.50, "transaction_count": 445},
                {"month": "2023-12", "total_revenue": 118500.25, "transaction_count": 420},
                {"month": "2023-11", "total_revenue": 135200.75, "transaction_count": 478},
                {"month": "2023-10", "total_revenue": 142300.00, "transaction_count": 502},
            ]
            columns = ["month", "total_revenue", "transaction_count"]
        elif "select 1" in sql.lower():
            # Simple test query
            rows = [{"sample_value": 1}]
            columns = ["sample_value"]
        else:
            # Default synthetic data
            rows = [
                {"id": 1, "name": "Sample Record 1", "value": 100.50},
                {"id": 2, "name": "Sample Record 2", "value": 200.75},
                {"id": 3, "name": "Sample Record 3", "value": 150.25},
            ]
            columns = ["id", "name", "value"]

        # Apply limit if specified
        if limit and len(rows) > limit:
            rows = rows[:limit]

        result = {
            "rows": rows,
            "columns": columns,
            "row_count": len(rows),
            "execution_time_ms": 45,  # Simulated execution time
            "warning": "This is synthetic data for development purposes. Connect to BigQuery for real data.",
        }

        logger.info(f"Executed query returning {len(rows)} rows")
        return result
