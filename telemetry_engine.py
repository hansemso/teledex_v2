import matplotlib.pyplot as plt
import numpy as np
from pgsql_supabase import get_db_connection  # make sure this matches your db function

# --- Fetch numeric data from Supabase ---
def fetch_data(label):
    """
    Fetch all values for a given label from telemetry table.
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

# --- Graph 1: Position + Rate of Change ---
def plot_entry(entry, position="left"):
    """
    Plots a single telemetry entry as:
    - Position / value over time
    - Rate of change (derivative)
    """
    try:
        label = entry['label']
        y_val = float(entry['y'].split()[0])
        data = fetch_data(label)

        if not data:
            data = [y_val]  # if no DB data, use current value
        x = np.arange(len(data))

        # Rate of change
        if len(data) >= 2:
            dy = np.diff(data) / np.diff(x)
            dx = x[1:]
        else:
            dy = [0]
            dx = [0]

        plt.figure(figsize=(8,4))
        plt.plot(x, data, label="Position / Value", marker='o')
        plt.plot(dx, dy, label="Rate of Change", linestyle='--', marker='x')
        plt.xlabel("Time (points)")
        plt.ylabel("Value / ΔValue")
        plt.title(f"Telemetry: {label}")
        plt.legend()
        plt.show()
    except Exception as e:
        print(f"Plot error: {e}")

# --- Graph 2: Prediction ---
def plot_prediction(label, x_unit="days", horizon=5):
    """
    Fetch data and plot a simple linear prediction
    """
    data = fetch_data(label)
    if not data:
        print(f"No data for {label}")
        return

    x = np.arange(len(data))
    y = np.array(data)

    # Linear trend prediction
    if len(y) >= 2:
        coef = np.polyfit(x, y, 1)
        trend = np.poly1d(coef)
        x_pred = np.arange(len(y) + horizon)
        y_pred = trend(x_pred)
    else:
        x_pred = np.arange(len(y) + horizon)
        y_pred = np.append(y, [y[-1]]*horizon)  # repeat last value if only one point

    plt.figure(figsize=(8,4))
    plt.plot(x_pred, y_pred, marker='o')
    plt.title(f"Prediction for {label}")
    plt.xlabel(f"Time ({x_unit})")
    plt.ylabel("Value")
    plt.show()
