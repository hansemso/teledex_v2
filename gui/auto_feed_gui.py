# gui/auto_feed_gui.py
from dearpygui.dearpygui import *
from engine.auto_feed_engine import start_auto_feed

def build_frame():
    with window(label="Auto Feed", width=300, height=100):
        add_button(label="Start Auto Feed", callback=lambda s,a,u: start_auto_feed())