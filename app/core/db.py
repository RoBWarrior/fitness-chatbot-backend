import psycopg2
from psycopg2 import Error
from app.core.config import DATABASE_URL

def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Database connection successful")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to Database: {e}")
        return None
    
def create_tables():
    #Creates the 'users', 'chat_sessions', and 'messages' tables in the database.
    conn = get_db_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        # Create the users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create the documents table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                doc_id VARCHAR(255) PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                filename VARCHAR(255) NOT NULL,
                uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create the chat_sessions table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions (
                session_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                start_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP WITH TIME ZONE
            );
        """)

        # Create the messages table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id SERIAL PRIMARY KEY,
                session_id INTEGER NOT NULL REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
                sender_type VARCHAR(50) NOT NULL, -- 'user' or 'assistant'
                content TEXT NOT NULL,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        print("✅ Database tables created successfully.")
    except Error as e:
        conn.rollback()
        print(f"❌ Error creating tables: {e}")
    finally:
        if conn:
            conn.close()
