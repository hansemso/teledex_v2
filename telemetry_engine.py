# telemetry_engine.py
# Offline-first telemetry storage system

import os
import psycopg2
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np

load_dotenv()

# ===============================
# Configuration
# ===============================

DB_HOST = os.getenv("SUPABASE_HOST")
DB_NAME = os.getenv("SUPABASE_DB", "postgres")
DB_USER = os.getenv("SUPABASE_USER", "postgres")
DB_PASSWORD = os.getenv("SUPABASE_PASSWORD")
DB_PORT = int(os.getenv("SUPABASE_PORT", 5432))

_memory_cache = {}

# ===============================
# Safe Database Connection
# ===============================

def safe_connect():
    if not DB_HOST or not DB_PASSWORD:
        return None

    try:
        return psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
    except Exception:
        return None

# ===============================
# Telemetry Storage
# ===============================

def insert_entry(label: str, value: float, category: str = "row1"):

    try:
        conn = safe_connect()

        if conn is None:
            _memory_cache.setdefault(label, []).append(float(value))
            print("Telemetry stored locally (offline mode)")
            return

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO telemetry (label, value, category, timestamp)
            VALUES (%s,%s,%s,NOW())
            """,
            (label, value, category)
        )

        conn.commit()
        cur.close()
        conn.close()

    except Exception:
        _memory_cache.setdefault(label, []).append(float(value))

# ===============================
# Data Retrieval
# ===============================

def fetch_data(label: str):

    try:
        conn = safe_connect()

        if conn is not None:
            cur = conn.cursor()

            cur.execute(
                "SELECT value FROM telemetry WHERE label=%s ORDER BY timestamp ASC",
                (label,)
            )

            results = cur.fetchall()

            cur.close()
            conn.close()

            if results:
                return [float(r[0]) for r in results]

    except Exception:
        pass

    return _memory_cache.get(label, [])

# ===============================
# Visualization
# ===============================

def plot_entry(label: str, y_hint: float = 0):

    data = fetch_data(label)

    if not data:
        data = [y_hint]

    data = list(map(float, data))

    x = np.arange(len(data))

    plt.figure(figsize=(8,4))
    plt.plot(x, data, marker='o', label="Value")

    if len(data) > 1:
        dx = np.arange(1, len(data))
        dy = np.diff(data)

        plt.plot(dx, dy, linestyle="--", marker="x", label="Rate")

    plt.xlabel("Time Index")
    plt.ylabel("Telemetry Value")
    plt.title(f"Telemetry: {label}")
    plt.legend()
    plt.grid()

    plt.show()

def plot_prediction(label: str, horizon=5):

    data = fetch_data(label)

    if not data:
        print(f"No data for {label}")
        return

    data = np.array(list(map(float, data)))

    x = np.arange(len(data))
    y = data

    if len(data) >= 2:
        coef = np.polyfit(x, y, 1)
        trend = np.poly1d(coef)

        x_future = np.arange(len(data) + horizon)
        y_future = trend(x_future)

    else:
        x_future = np.arange(len(data) + horizon)
        y_future = np.append(data, [data[-1]] * horizon)

    plt.figure(figsize=(8,4))
    plt.plot(x_future, y_future, marker='o')
    plt.title(f"Prediction for {label}")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.grid()

    plt.show()