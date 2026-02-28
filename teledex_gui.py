import tkinter as tk
import threading
import requests
import random
import time

from pgsql_supabase import get_db_connection
from quiz_engine import run_quiz
from telemetry_engine import plot_entry, plot_prediction


# ===============================
# ROOT WINDOW
# ===============================

root = tk.Tk()
root.title("Teledex")
root.geometry("600x800")
root.attributes("-topmost", True)
root.configure(padx=10, pady=10)


# ===============================
# TELEMETRY FRAME
# ===============================

telemetry_frame = tk.LabelFrame(root, text="Telemetry Inputs", padx=10, pady=10)
telemetry_frame.pack(fill="x", pady=10)

rows = []
x_options = ["days", "hours", "mins"]


# -------------------------------
# Telemetry Rows
# -------------------------------

for i in range(3):

    row_frame = tk.Frame(telemetry_frame)
    row_frame.pack(pady=2)

    label_entry = tk.Entry(row_frame, width=15)
    label_entry.insert(0, f"Label {i+1}")
    label_entry.grid(row=0, column=0, padx=5)

    x_var = tk.StringVar(value="days")

    def make_cycle(var=x_var):
        def cycle():
            current = var.get()
            idx = x_options.index(current)
            var.set(x_options[(idx + 1) % len(x_options)])
        return cycle

    tk.Button(
        row_frame,
        textvariable=x_var,
        width=10,
        command=make_cycle()
    ).grid(row=0, column=1, padx=5)

    y_entry = tk.Entry(row_frame, width=15)
    y_entry.insert(0, "10")
    y_entry.grid(row=0, column=2, padx=5)

    # Plot button
    def make_plot(r=i):
        def do_plot():
            label = rows[r]["label"].get()
            y_input = rows[r]["y_entry"].get()

            print(f"TEST: label='{label}' y_input='{y_input}'")

            try:
                plot_entry(label, float(y_input))
            except Exception as e:
                print("Plot error:", e)

        return do_plot

    tk.Button(
        row_frame,
        text="PLOT",
        width=10,
        command=make_plot(i)
    ).grid(row=0, column=3, padx=5)

    # Predict button
    def make_predict(r=i):
        def do_predict():
            label = rows[r]["label"].get()
            plot_prediction(label, horizon=5)

        return do_predict

    tk.Button(
        row_frame,
        text="PREDICT",
        width=10,
        command=make_predict(i)
    ).grid(row=0, column=4, padx=5)

    rows.append({
        "label": label_entry,
        "x_var": x_var,
        "y_entry": y_entry
    })


# ===============================
# WEATHER SYSTEM
# ===============================

weather_pad = None


def show_weather():
    global weather_pad

    try:
        lat, lon = 27.3364, -82.5307

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=precipitation_probability"

        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        current = data["current_weather"]

        temp = current.get("temperature", "?")
        wind = current.get("windspeed", "?")
        code = current.get("weathercode", 0)

        code_map = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy",
            3: "Overcast", 45: "Fog", 48: "Rime fog",
            51: "Light drizzle", 53: "Moderate drizzle",
            55: "Dense drizzle", 61: "Slight rain",
            63: "Moderate rain", 65: "Heavy rain",
            80: "Rain showers", 95: "Thunderstorm"
        }

        condition = code_map.get(code, "Unknown")

        hourly = data.get("hourly", {})
        precip_probs = hourly.get("precipitation_probability", [])[:6]

        forecast_text = "Next 6h rain probability: " + ", ".join(
            f"{p}%" for p in precip_probs
        )

        weather_text = (
            f"Temp: {temp}°C\n"
            f"Condition: {condition}\n"
            f"Wind: {wind} km/h\n"
            f"{forecast_text}"
        )

    except Exception as e:
        weather_text = f"Could not fetch weather: {e}"

    weather_pad.config(state="normal")
    weather_pad.delete(1.0, tk.END)
    weather_pad.insert(tk.END, weather_text)
    weather_pad.config(state="disabled")


def show_weather_async():
    threading.Thread(target=show_weather, daemon=True).start()


# ===============================
# WEATHER WIDGETS
# ===============================

tk.Label(root, text="Current Weather (Sarasota, FL)").pack(pady=5)

weather_pad = tk.Text(root, height=6, width=40, state="disabled")
weather_pad.pack(pady=5)

tk.Button(
    root,
    text="Update Weather",
    width=20,
    command=show_weather_async
).pack(pady=5)


# ===============================
# AUTO FEED SYSTEM
# ===============================

def auto_feed():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        coffee_value = random.randint(20, 100) + int(time.time() // 60)

        cur.execute(
            "INSERT INTO telemetry (label, value) VALUES (%s,%s)",
            ("Sale of coffee mugs", coffee_value)
        )

        heart_value = random.randint(55, 75)

        cur.execute(
            "INSERT INTO telemetry (label, value) VALUES (%s,%s)",
            ("Resting heart rate", heart_value)
        )

        stock_value = random.uniform(95, 115)

        cur.execute(
            "INSERT INTO telemetry (label, value) VALUES (%s,%s)",
            ("Price of Apricot stock", round(stock_value, 2))
        )

        conn.commit()
        cur.close()
        conn.close()

        print("Auto-feed inserted new data.")

    except Exception as e:
        print("Auto-feed error:", e)

    root.after(60000, auto_feed)


# ===============================
# LEARNING TOOL PANEL
# ===============================

control_frame = tk.LabelFrame(root, text="Learning Tools", padx=10, pady=10)
control_frame.pack(fill="x", pady=10)

tk.Button(
    control_frame,
    text="Python Quizzes",
    width=25,
    command=run_quiz
).pack(pady=10)


# ===============================
# APP STARTUP
# ===============================

if __name__ == "__main__":
    root.after(1000, show_weather_async)
    root.after(5000, auto_feed)

    root.mainloop()