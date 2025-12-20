import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import dotenv

dotenv.load_dotenv()

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def init_db():
    """Initializes the database schema."""
    conn = get_db_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    agent_name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            conn.commit()
    except Exception as e:
        print(f"Error initializing DB: {e}")
    finally:
        conn.close()

def save_message(agent_name: str, role: str, content: str):
    """Saves a message to the conversation history."""
    conn = get_db_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO conversations (agent_name, role, content)
                VALUES (%s, %s, %s)
            """, (agent_name, role, content))
            conn.commit()
    except Exception as e:
        print(f"Error saving message: {e}")
    finally:
        conn.close()

def get_last_conversation(agent_name: str, limit: int = 5) -> str:
    """Retrieves the last N messages for context."""
    conn = get_db_connection()
    if not conn:
        return ""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT role, content, timestamp 
                FROM conversations 
                WHERE agent_name = %s 
                ORDER BY id DESC 
                LIMIT %s
            """, (agent_name, limit))
            rows = cur.fetchall()
            
            # Reverse to get chronological order
            history = []
            for row in reversed(rows):
                history.append(f"{row['role']}: {row['content']}")
            
            return "\n".join(history)
    except Exception as e:
        print(f"Error retrieving history: {e}")
        return ""
    finally:
        conn.close()
