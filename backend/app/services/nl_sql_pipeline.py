from .knowledge_base import KnowledgeBase
from ..models.query_models import QueryPlan

class NLToSQLPipeline:
    def __init__(self, kb: KnowledgeBase) -> None:
        self.kb = kb

    def build_plan(self, question: str) -> QueryPlan:
        tables = self.kb.list_tables()
        target_table = tables[0] if tables else "unknown"
        metrics = ["COUNT(*) as total"]
        sql = f"SELECT {metrics[0]} FROM {target_table} LIMIT 10"
        return QueryPlan(
            tables=[target_table],
            filters=[],
            group_by=[],
            metrics=metrics,
            sql=sql,
        )
