from app.core.config import settings

def run_sql_mock(sql: str):
    lower = sql.lower()
    if "total_spent" in lower:
        return {
            "columns": ["customer_id", "total_spent"],
            "rows": [[1, 1200],[2, 950],[3, 860],[4, 800],[5, 790],[6, 700],[7, 695],[8, 600],[9, 590],[10, 540]]
        }
    if "read_at" in lower and "from reads.activity" in lower:
        return {
            "columns": ["user_id", "book_id", "read_at"],
            "rows": [[101,"B123","2025-08-10T10:00:00Z"],[102,"B456","2025-08-10T09:55:00Z"],[103,"B789","2025-08-10T09:50:00Z"],[104,"B234","2025-08-10T09:45:00Z"],[105,"B567","2025-08-10T09:40:00Z"],[106,"B012","2025-08-10T09:35:00Z"],[107,"B678","2025-08-10T09:30:00Z"],[108,"B901","2025-08-10T09:25:00Z"],[109,"B345","2025-08-10T09:20:00Z"],[110,"B234","2025-08-10T09:15:00Z"]]}
    if "complaint_type" in lower:
        return {
            "columns": ["complaint_type","num_complaints"],
            "rows": [["Late delivery",25],["Damaged item",18],["Wrong item",10]]
        }
    return {"columns": [], "rows": []}

def run_sql_real(sql: str):
    # Placeholder for real BigQuery
    # from google.cloud import bigquery
    # client = bigquery.Client(project=settings.bigquery_project)
    # job = client.query(sql)
    # rows = list(job.result())
    # columns = [schema_field.name for schema_field in job.schema]
    # data_rows = [[getattr(r, c) for c in columns] for r in rows]
    # return {"columns": columns, "rows": data_rows}
    raise NotImplementedError("Real BigQuery not yet implemented")

def run_sql(sql: str):
    if settings.bigquery_use_mock:
        return run_sql_mock(sql)
    return run_sql_real(sql)
