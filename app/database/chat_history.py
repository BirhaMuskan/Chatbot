from app.database.connection import get_connection

def save_chat(user_question, ai_response):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO ChatHistory
    (UserQuestion, AIResponse)
    VALUES (?, ?)
    """

    cursor.execute(query, (user_question, ai_response))
    conn.commit()
    conn.close()