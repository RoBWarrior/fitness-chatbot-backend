# app/services/db_helpers.py
from app.core.db import get_db_connection

# --- User CRUD ---
def create_user(username: str, password_hash: str):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING user_id;",
            (username, password_hash)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        conn.rollback()
        print(f"Error creating user: {e}")
        return None
    finally:
        if conn:
            conn.close()

def save_document_record(doc_id: str, user_id: int, filename: str):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO documents (doc_id, user_id, filename) VALUES (%s, %s, %s);",
            (doc_id, user_id, filename)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error saving document record: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_user_documents(user_id: int):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT doc_id, filename FROM documents WHERE user_id=%s;",
            (user_id,)
        )
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching user documents: {e}")
        return []
    finally:
        if conn:
            conn.close()

def delete_document_record(doc_id: str):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM documents WHERE doc_id=%s;",
            (doc_id,)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error deleting document record: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_user_sessions(user_id: int):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT session_id, start_time, end_time FROM chat_sessions WHERE user_id=%s ORDER BY start_time DESC;",
            (user_id,)
        )
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching user sessions: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_user(username: str):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s;", (username,))
        return cur.fetchone()
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        if conn:
            conn.close()

# --- Chat Session CRUD ---
def create_session(user_id: int):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_sessions (user_id) VALUES (%s) RETURNING session_id;",
            (user_id,)
        )
        session_id = cur.fetchone()[0]
        conn.commit()
        return session_id
    except Exception as e:
        conn.rollback()
        print(f"Error creating session: {e}")
        return None
    finally:
        if conn:
            conn.close()


def end_session(session_id: int):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE chat_sessions SET end_time=NOW() WHERE session_id=%s;",
            (session_id,)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error ending session: {e}")
    finally:
        if conn:
            conn.close()

def delete_session(session_id: int):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        # Dependent messages will need to be deleted, relying on ON DELETE CASCADE if set up,
        # otherwise we should delete messages first. Assuming NO cascade for safety, let's delete messages first.
        cur.execute("DELETE FROM messages WHERE session_id=%s;", (session_id,))
        cur.execute("DELETE FROM chat_sessions WHERE session_id=%s;", (session_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error deleting session: {e}")
        return False
    finally:
        if conn:
            conn.close()

# --- Messages CRUD ---
def save_message(session_id: int, sender_type: str, content: str):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO messages (session_id, sender_type, content)
            VALUES (%s, %s, %s) RETURNING message_id;
            """,
            (session_id, sender_type, content)
        )
        message_id = cur.fetchone()[0]
        conn.commit()
        return message_id
    except Exception as e:
        conn.rollback()
        print(f"Error saving message: {e}")
        return None
    finally:
        if conn:
            conn.close()


def get_chat_history(session_id: int):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT sender_type, content, timestamp FROM messages WHERE session_id=%s ORDER BY timestamp ASC;",
            (session_id,)
        )
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return []
    finally:
        if conn:
            conn.close()
