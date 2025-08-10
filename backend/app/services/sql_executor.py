"""
SQL Executor with mock data generation
TODO: Integrate with actual BigQuery execution
"""

import datetime
from typing import List, Tuple, Any
from decimal import Decimal
import random

from ..logging import get_logger

logger = get_logger(__name__)


class SQLExecutor:
    """SQL query executor that returns synthetic data."""
    
    def __init__(self) -> None:
        """Initialize the SQL executor."""
        logger.info("Initializing SQL executor (stub implementation with mock data)")
    
    def execute(self, sql: str, limit: int = 100) -> Tuple[List[str], List[List[Any]], str]:
        """
        Execute SQL query and return synthetic results.
        
        Args:
            sql: SQL query string
            limit: Maximum number of rows to return
            
        Returns:
            Tuple of (columns, rows, warning_message)
        """
        logger.info(f"Executing SQL query (mock): {sql[:100]}...")
        
        # TODO: Replace with actual BigQuery execution
        # For now, return synthetic data based on common query patterns
        
        # Detect query type and return appropriate mock data
        sql_lower = sql.lower()
        
        if "revenue" in sql_lower or "amount" in sql_lower:
            return self._generate_revenue_data(limit)
        elif "read" in sql_lower or "kwh" in sql_lower:
            return self._generate_energy_data(limit)
        elif "customer" in sql_lower or "ticket" in sql_lower:
            return self._generate_customer_data(limit)
        else:
            return self._generate_generic_data(limit)
    
    def _generate_revenue_data(self, limit: int) -> Tuple[List[str], List[List[Any]], str]:
        """Generate mock revenue data."""
        columns = ["month", "total_revenue"]
        rows = []
        
        # Generate data for past 12 months
        base_date = datetime.datetime.now().replace(day=1)
        for i in range(min(limit, 12)):
            month_date = base_date - datetime.timedelta(days=30 * i)
            revenue = Decimal(str(random.uniform(50000, 150000)))
            rows.append([
                month_date.strftime("%Y-%m-01"),
                round(float(revenue), 2)
            ])
        
        warning = "This is synthetic data for demonstration purposes. Real BigQuery integration pending."
        
        return columns, rows, warning
    
    def _generate_energy_data(self, limit: int) -> Tuple[List[str], List[List[Any]], str]:
        """Generate mock energy/reads data."""
        columns = ["account_id", "read_date", "read_value_kwh"]
        rows = []
        
        for i in range(min(limit, 50)):
            account_id = f"ACC{1000 + i}"
            read_date = (datetime.datetime.now() - datetime.timedelta(days=i)).date()
            read_value = round(random.uniform(200, 800), 2)
            rows.append([account_id, str(read_date), read_value])
        
        warning = "This is synthetic data for demonstration purposes. Real BigQuery integration pending."
        
        return columns, rows, warning
    
    def _generate_customer_data(self, limit: int) -> Tuple[List[str], List[List[Any]], str]:
        """Generate mock customer care data."""
        columns = ["ticket_id", "customer_id", "issue_type", "status", "created_at"]
        statuses = ["open", "in_progress", "closed", "pending"]
        issue_types = ["billing", "outage", "connection", "general_inquiry"]
        
        rows = []
        for i in range(min(limit, 30)):
            ticket_id = f"TICKET-{2000 + i}"
            customer_id = f"CUST-{3000 + i}"
            issue_type = random.choice(issue_types)
            status = random.choice(statuses)
            created_at = (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30)))
            
            rows.append([
                ticket_id,
                customer_id,
                issue_type,
                status,
                created_at.strftime("%Y-%m-%d %H:%M:%S")
            ])
        
        warning = "This is synthetic data for demonstration purposes. Real BigQuery integration pending."
        
        return columns, rows, warning
    
    def _generate_generic_data(self, limit: int) -> Tuple[List[str], List[List[Any]], str]:
        """Generate generic mock data."""
        columns = ["id", "value", "timestamp"]
        rows = []
        
        for i in range(min(limit, 20)):
            rows.append([
                i + 1,
                f"sample_value_{i + 1}",
                (datetime.datetime.now() - datetime.timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S")
            ])
        
        warning = "This is synthetic data for demonstration purposes. Real BigQuery integration pending."
        
        return columns, rows, warning