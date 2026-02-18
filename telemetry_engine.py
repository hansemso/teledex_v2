import matplotlib.pyplot as plt
import numpy as np
from pgsql_supabase import get_connection

# --- Fetch numeric data from Supabase ---
def fetch_data(label):
    """
    Fetches all values for a given label from telemetry table.
    Returns a list of floats.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT value FROM telemetry WHERE label=%s ORDER BY timestamp ASC", (label,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [r[0] for r in rows] if rows else []
    except Exception as e:
        print(f"DB fetch error: {e}")
        return []

# --- Convert time axis ---
def convert_time(x_unit, num_points):
    """
    Convert points to time array based on x_unit.
    """
