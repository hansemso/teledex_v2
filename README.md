Teledex v2 – Learning Tools GUI

Teledex v2 is a desktop learning app built with Python and DearPyGUI, designed to help users study code, quiz themselves, and track telemetry and other learning data. This version is a full rewrite of the original Teledex, modernized with modular GUI and backend structure.

Features

Interactive Quiz Module – Study and test yourself with code snippets and Q&A cards.

Telemetry Module – View and log learning progress or custom telemetry data.

Weather Module – Display current weather conditions.

Auto-Feed Module – Automate updates or scheduled tasks.

CRUD for Study Cards – Add, edit, and delete study cards dynamically.

Logging – All app activity is logged for debugging and progress tracking.

Installation

Clone the repository:
git clone https://github.com/hansemso/teledex_v2.git
cd teledex_v2

py -m pip install -r requirements.txt

py main.py

teledex_v2/
│
├─ main.py              # App entry point
├─ requirements.txt     # Dependencies
├─ gui/                 # DearPyGUI interface modules
│   ├─ quiz_gui.py
│   ├─ telemetry_gui.py
│   ├─ weather_gui.py
│   └─ auto_feed_gui.py
├─ engine/              # Backend logic modules
│   ├─ quiz_engine.py
│   ├─ telemetry_engine.py
│   ├─ weather_engine.py
│   └─ auto_feed_engine.py
├─ utils/               # Utility files
│   ├─ logger.py
│   └─ study_cards_v2.json
├─ teledex.db           # SQLite database (optional)
└─ teledex.log          # App log file