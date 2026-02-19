import matplotlib.pyplot as plt
import numpy as np
from pgsql_supabase import get_db_connection  # use the correct function

# --- Fetch numeric data from Supabase ---
def fetch_data(label):
    """
    Fetches all values for a given label from telemetry table.
    Returns a list of floats.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT value FROM telemetry WHERE label=%s ORDER BY timestamp ASC", (label,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [r[0] for r in rows] if rows else []
    except Exception as e:
        print(f"DB fetch error: {e}")
        return []

# --- Plot a single telemetry entry ---
def plot_entry(entry, position="left"):
    """
    Plots a single telemetry entry.
    entry: dict with 'label', 'x', 'y'
    """
    try:
        label = entry['label']
        y_val = float(entry['y'].split()[0])
        plt.figure()
        plt.title(f"Telemetry: {label}")
        plt.bar([0], [y_val])
        plt.ylabel("Value")
        plt.show()
    except Exception as e:
        print(f"Plot error: {e}")

# --- Predict future values (dummy example) ---
def plot_prediction(label, x_unit="days", horizon=5):
    """
    Fetch data and plot a simple prediction (dummy example)
    """
    data = fetch_data(label)
    if not data:
        print(f"No data for {label}")
        return

    x = np.arange(len(data))
    y = np.array(data)

    # Simple linear trend prediction
    if len(y) >= 2:
        coef = np.polyfit(x, y, 1)
        trend = np.poly1d(coef)
        x_pred = np.arange(len(y)+horizon)
        y_pred = trend(x_pred)
    else:
        x_pred = np.arange(len(y)+horizon)
        y_pred = np.append(y, [y[-1]]*horizon)

    plt.figure()
    plt.plot(x_pred, y_pred, marker='o')
    plt.title(f"Prediction for {label}")
    plt.xlabel(f"Time ({x_unit})")
    plt.ylabel("Value")
    plt.show()
