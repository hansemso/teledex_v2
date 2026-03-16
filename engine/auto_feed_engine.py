import threading
import time
import random
import sqlite3

DB_FILE = "teledex.db"

def setup_db():
    """Ensure telemetry table exists."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT,
            value REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Telemetry table ready.")

def get_db_connection():
    return sqlite3.connect(DB_FILE)

def start_auto_feed():
    """Starts auto-feed in a separate thread."""
    setup_db()
    def feed_loop():
        while True:
            try:
                conn = get_db_connection()
                cur = conn.cursor()

                coffee_value = random.randint(20, 100) + int(time.time() // 60)
                heart_value = random.randint(55, 75)
                stock_value = round(random.uniform(95, 115), 2)

                cur.execute("INSERT INTO telemetry (label, value) VALUES (?, ?)", ("Sale of coffee mugs", coffee_value))
                cur.execute("INSERT INTO telemetry (label, value) VALUES (?, ?)", ("Resting heart rate", heart_value))
                cur.execute("INSERT INTO telemetry (label, value) VALUES (?, ?)", ("Price of Apricot stock", stock_value))

                conn.commit()
                cur.close()
                conn.close()
                print("Auto-feed inserted new data.")
            except Exception as e:
                print("Auto-feed error:", e)
            time.sleep(60)
    threading.Thread(target=feed_loop, daemon=True).start()