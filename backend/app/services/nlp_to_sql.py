from app.services.conversation_memory import append_message, get_conversation, ensure_conversation

# Hardcoded natural language to SQL mapping and explanations
def get_sql_for_question(question: str, conversation_id: str | None = None):
    cid = ensure_conversation(conversation_id)
    append_message(cid, "user", question)
    q = question.lower().strip()

    if "top customers" in q:
        sql = """-- Get top 10 customers by total spend
SELECT customer_id, SUM(amount) AS total_spent
FROM financials.transactions
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;"""
        explanation = "Returns top 10 customers by total spend from financials.transactions."
    elif "read activity" in q or "recent reads" in q:
        sql = """-- Recent read events
SELECT user_id, book_id, read_at
FROM reads.activity
ORDER BY read_at DESC
LIMIT 10;"""
        explanation = "Shows the 10 most recent read events."
    elif "customer complaints" in q or "complaints by type" in q:
        sql = """-- Complaints count by type
SELECT complaint_type, COUNT(*) AS num_complaints
FROM customercare.complaints
GROUP BY complaint_type
ORDER BY num_complaints DESC;"""
        explanation = "Counts complaints grouped by type."
    else:
        sql = """-- No direct mapping found
-- TODO: Use LLM provider when integrated
SELECT 1 AS placeholder;"""
        explanation = "No hardcoded mapping yet. Placeholder query returned."

    append_message(cid, "assistant", f"SQL proposed:\n{{sql}}\nExplanation: {{explanation}}")
    history = get_conversation(cid)
    return sql, explanation, cid, history
