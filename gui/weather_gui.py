# gui/weather_gui.py
from dearpygui.dearpygui import *
from engine.weather_engine import get_weather

def build_frame():
    with window(label="Weather", width=600, height=150):
        add_text("Weather info will appear here.", tag="weather_text")
        add_button(label="Update Weather", callback=update_weather)
        # fetch immediately
        update_weather()

def update_weather(sender=None, app_data=None, user_data=None):
    try:
        info = get_weather()
        set_value("weather_text", info)
    except Exception as e:
        set_value("weather_text", f"[Weather] Error: {e}")