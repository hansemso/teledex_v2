# engine/weather_engine.py
import requests

def get_weather():
    try:
        lat, lon = 27.3364, -82.5307
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        current = data["current_weather"]
        return f"Temp: {current['temperature']}°C, Wind: {current['windspeed']} km/h"
    except Exception as e:
        return f"Error fetching weather: {e}"