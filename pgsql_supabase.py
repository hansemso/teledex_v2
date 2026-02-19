import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (optional)
load_dotenv()

# --- CONFIGURATION ---
DB_HOST = os.getenv("SUPABASE_HOST", "db.<your-supabase-host>.supabase.co")
DB_NAME = os.getenv("SUPABASE_DB", "postgres")
DB_USER = os.getenv("SUPABASE_USER", "postgres")
DB_PASSWORD = os.getenv("SUPABASE_PASSWORD", "6D3gBAvxVAH6Cgd8")  # replace with your Supabase password
DB_PORT = os.getenv("SUPABASE_PORT", 5432)

# --- CONNECTION ---
def get_db_connection():
    """
    Connect to Supabase Postgres and return the connection object.
    """
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

# --- INSERT ENTRY ---
def insert_entry(label: str, value: float, category: str = "row1"):
    """
    Insert a telemetry entry into the database with current timestamp.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO telemetry (label, value, category, timestamp) VALUES (%s,%s,%s,NOW())",
            (label, value, category)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        raise Exception(f"Failed to insert entry: {e}")

# --- FETCH DATA ---
def fetch_data(label: str):
    """
    Fetch all numeric values for a given label from telemetry table.
    Returns a list of floats, ordered by timestamp ascending.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT value FROM telemetry WHERE label=%s ORDER BY timestamp ASC",
            (label,)
        )
        results = cur.fetchall()
        cur.close()
        conn.close()
        return [float(row[0]) for row in results]
    except Exception as e:
        raise Exception(f"Failed to fetch data: {e}")
