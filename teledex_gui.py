from pgsql_supabase import get_db_connection, insert_entry, fetch_data
import tkinter as tk
from tkinter import messagebox
import threading
import requests

from telemetry_engine import plot_entry, plot_prediction  # your plotting math engine


# --- ROOT WINDOW ---
root = tk.Tk()
root.title("Teledex")
root.geometry("600x800")
root.attributes("-topmost", True)

# --- TELEMETRY FRAME ---
telemetry_frame = tk.LabelFrame(root, text="Telemetry Inputs", padx=10, pady=10)
telemetry_frame.pack(fill="x", pady=10)

rows = []
x_options = ["days", "hours", "mins"]
positions = ["left", "top", "right"]  # plot positions

for i in range(3):
    row_frame = tk.Frame(telemetry_frame)
    row_frame.pack(pady=2)

    # 1st column: label
    label_entry = tk.Entry(row_frame, width=15)
    label_entry.insert(0, f"Label {i+1}")
    label_entry.grid(row=0, column=0, padx=5)

    # 2nd column: x-axis unit
    x_var = tk.StringVar(value="days")
    def make_cycle(var=x_var):
        def cycle():
            current = var.get()
            idx = x_options.index(current)
            var.set(x_options[(idx+1)%len(x_options)])
        return cycle
    x_button = tk.Button(row_frame, textvariable=x_var, width=10, command=make_cycle())
    x_button.grid(row=0, column=1, padx=5)

    # 3rd column: y-axis value
    y_entry = tk.Entry(row_frame, width=15)
    y_entry.insert(0, "10")
    y_entry.grid(row=0, column=2, padx=5)

    # 4th column: plot button
    def make_plot(r=i):
        def do_plot():
            label = rows[r]["label"].get()
            x_unit = rows[r]["x_var"].get()
            y_input = rows[r]["y_entry"].get()

            # --- TEMPORARY TEST: skip DB write ---
            # try:
            #     conn = get_db_connection()
            #     cur = conn.cursor()
            #     value = float(y_input.split()[0])
            #     cur.execute("INSERT INTO telemetry (label, value) VALUES (%s,%s)", (label, value))
            #     conn.commit()
            #     cur.close()
            #     conn.close()
            # except Exception as e:
            #     messagebox.showerror("Database Error", str(e))

            print(f"TEST: {label=} {y_input=} {x_unit=}")


            # Plot
            plot_entry({"label": label, "x": x_unit, "y": y_input}, position=positions[r])
        return do_plot

    plot_button = tk.Button(row_frame, text="PLOT", width=10, command=make_plot())
    plot_button.grid(row=0, column=3, padx=5)

    # 5th column: predict button
    def make_predict(r=i):
        def do_predict():
            label = rows[r]["label"].get()
            x_unit = rows[r]["x_var"].get()
            plot_prediction(label, x_unit=x_unit, horizon=5)
        return do_predict

    predict_button = tk.Button(row_frame, text="PREDICT", width=10, command=make_predict())
    predict_button.grid(row=0, column=4, padx=5)

    rows.append({
        "label": label_entry,
        "x_var": x_var,
        "y_entry": y_entry,
        "plot_button": plot_button,
        "predict_button": predict_button
    })

# --- WEATHER FUNCTION ---
def show_weather():
    try:
        lat, lon = 27.3364, -82.5307
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=precipitation_probability"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        
        current = data['current_weather']
        temp = current.get('temperature', '?')
        wind = current.get('windspeed', '?')
        code = current.get('weathercode', 0)
        
        code_map = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
            55: "Dense drizzle", 61: "Slight rain", 63: "Moderate rain",
            65: "Heavy rain", 80: "Rain showers", 95: "Thunderstorm"
        }
        condition = code_map.get(code, "Unknown")
        
        hourly = data.get('hourly', {})
        precip_probs = hourly.get('precipitation_probability', [])[:6]
        forecast_text = "Next 6h rain probability: " + ", ".join(f"{p}%" for p in precip_probs)

        weather_text = f"Temp: {temp}°C\nCondition: {condition}\nWind: {wind} km/h\n{forecast_text}"
    except Exception as e:
        weather_text = f"Could not fetch weather: {e}"

    weather_pad.config(state="normal")
    weather_pad.delete(1.0, tk.END)
    weather_pad.insert(tk.END, weather_text)
    weather_pad.config(state="disabled")

def auto_refresh_weather():
    threading.Thread(target=show_weather, daemon=True).start()
    root.after(600000, auto_refresh_weather)  # every 10 minutes

# --- WEATHER WIDGETS ---
tk.Label(root, text="Current Weather (Sarasota, FL)").pack(pady=5)
weather_pad = tk.Text(root, height=6, width=40, state="disabled")
weather_pad.pack(pady=5)
tk.Button(root, text="Update Weather", width=20,
          command=lambda: threading.Thread(target=show_weather, daemon=True).start()).pack(pady=5)

import random
import time

def auto_feed():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # --- 1. Coffee Mug Sales (simulate increasing sales)
        coffee_value = random.randint(20, 100) + int(time.time() // 60)  # increase over time   
        cur.execute(
            "INSERT INTO telemetry (label, value) VALUES (%s,%s)",
            ("Sale of coffee mugs", coffee_value)
        )

        # --- 2. Resting Heart Rate (simulate normal human range)
        heart_value = random.randint(55, 75)
        cur.execute(
            "INSERT INTO telemetry (label, value) VALUES (%s,%s)",
            ("Resting heart rate", heart_value)
        )

        # --- 3. Apricot Stock (simulate stock fluctuation)
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

    # Run again in 60 seconds
    root.after(60000, auto_feed)


# --- START APP ---
if __name__ == "__main__":
    root.after(1000, auto_refresh_weather)
    root.after(5000, auto_feed)  # start auto feed after 5 seconds
    show_weather()
    root.mainloop()
