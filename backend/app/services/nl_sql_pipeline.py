class NLToSQLPipeline:
    """NL-to-SQL conversion pipeline with keyword-based routing."""
    
    def generate(self, question: str) -> dict:
        """Generate SQL from natural language question."""
        question_lower = question.lower()
        
        # Simple keyword-based routing
        if any(word in question_lower for word in ['revenue', 'sales', 'profit', 'financial']):
            return self._generate_financial_query(question)
        elif any(word in question_lower for word in ['user', 'customer', 'signup', 'login']):
            return self._generate_user_query(question)
        else:
            return self._generate_generic_query(question)
    
    def _generate_financial_query(self, question: str) -> dict:
        """Generate financial domain SQL."""
        return {
            "proposed_sql": """
                SELECT 
                    DATE_TRUNC(transaction_date, MONTH) as month,
                    SUM(amount) as total_revenue
                FROM financials.transactions 
                WHERE transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)
                GROUP BY month
                ORDER BY month
            """.strip(),
            "explanation": "Aggregates monthly revenue from transactions in the last 3 months",
            "referenced_domains": ["financials"]
        }
    
    def _generate_user_query(self, question: str) -> dict:
        """Generate user/customer domain SQL."""  
        return {
            "proposed_sql": """
                SELECT 
                    country_code,
                    COUNT(*) as user_count
                FROM reads.users
                WHERE signup_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH)
                GROUP BY country_code
                ORDER BY user_count DESC
            """.strip(),
            "explanation": "Counts new user signups by country in the last month",
            "referenced_domains": ["reads"]
        }
    
    def _generate_generic_query(self, question: str) -> dict:
        """Generate generic query for unrecognized patterns."""
        return {
            "proposed_sql": "SELECT 'Query not yet supported' as message",
            "explanation": "This query type is not yet supported in the MVP",
            "referenced_domains": []
        }