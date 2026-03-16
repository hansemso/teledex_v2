#The only reason to change this is to add subsystems, which each have their own means of debugging w/o going through here. build_frame is the i/o control to this file. 
#Other files do not have event loop, viewport, context...cannot open w/o this file.   

from dearpygui.dearpygui import *

from gui import telemetry_gui
from gui import quiz_gui
from gui import weather_gui
from gui import auto_feed_gui


def setup_teledex():

    telemetry_gui.build_frame()
    quiz_gui.build_frame()
    weather_gui.build_frame()
    auto_feed_gui.build_frame()


def main():  # Lifecycle order 1-7.

    print("Starting Teledex GUI...")

    create_context()

    create_viewport(title="Teledex", width=900, height=700)

    setup_dearpygui()   #   

    setup_teledex()  # widgets,ie each window.

    show_viewport()

    start_dearpygui()

    destroy_context()


if __name__ == "__main__":  
    main()  # Modularized program entry point.

