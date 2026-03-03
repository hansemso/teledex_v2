import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_FILE = "teledex.db"


# ================================
# DATABASE CONNECTION
# ================================

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None


# ================================
# INITIALIZE DATABASE
# ================================

def init_db():

    conn = get_db_connection()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS telemetry(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label TEXT,
        value REAL,
        category TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# ================================
# INSERT ENTRY
# ================================

def insert_entry(label: str, value: float, category: str = "row1"):

    conn = get_db_connection()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO telemetry (label,value,category)
        VALUES (?,?,?)
    """, (label, value, category))

    conn.commit()
    conn.close()


# ================================
# FETCH DATA
# ================================

def fetch_data(label: str):

    conn = get_db_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    cur.execute("""
        SELECT value FROM telemetry
        WHERE label=?
        ORDER BY timestamp ASC
    """, (label,))

    results = cur.fetchall()
    conn.close()

    return [float(row[0]) for row in results]