from typing import Dict, List, Any


class SQLExecutor:
    """SQL query executor with mock data responses."""
    
    def execute(self, sql: str, limit: int = 100) -> Dict[str, Any]:
        """Execute SQL query and return results."""
        sql_lower = sql.lower()
        
        # Return mock data based on query pattern
        if 'revenue' in sql_lower or 'amount' in sql_lower:
            return self._mock_financial_data()
        elif 'user' in sql_lower or 'customer' in sql_lower:
            return self._mock_user_data() 
        else:
            return self._mock_generic_data()
    
    def _mock_financial_data(self) -> Dict[str, Any]:
        """Return mock financial data."""
        return {
            "columns": ["month", "total_revenue"],
            "rows": [
                ["2024-06", 125000.50],
                ["2024-07", 138900.75], 
                ["2024-08", 142500.00]
            ],
            "warning": "This is mock data for MVP demonstration"
        }
    
    def _mock_user_data(self) -> Dict[str, Any]:
        """Return mock user data."""
        return {
            "columns": ["country_code", "user_count"],
            "rows": [
                ["US", 1250],
                ["CA", 340],
                ["UK", 180],
                ["DE", 125]
            ],
            "warning": "This is mock data for MVP demonstration"
        }
    
    def _mock_generic_data(self) -> Dict[str, Any]:
        """Return mock generic data."""
        return {
            "columns": ["message"],
            "rows": [["Query executed successfully"]],
            "warning": "This is mock data for MVP demonstration"
        }