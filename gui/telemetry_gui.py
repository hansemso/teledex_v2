import sqlite3
from dearpygui.dearpygui import *

DB_FILE = "teledex.db"


def init_db():

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT,
            value TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def get_latest_telemetry():

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        SELECT label, value, timestamp
        FROM telemetry
        ORDER BY id DESC
        LIMIT 10
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def build_frame():

    init_db()   # ensure database exists

    with window(label="Telemetry", width=600, height=250):

        with table(tag="telemetry_table", header_row=True):

            add_table_column(label="Label")
            add_table_column(label="Value")
            add_table_column(label="Timestamp")

    update_table()


def update_table():

    rows = get_latest_telemetry()

    children = get_item_children("telemetry_table", 1) or []

    for child in children:
        delete_item(child)

    for row in rows:

        with table_row(parent="telemetry_table"):

            for cell in row:
                add_text(str(cell))

#========debugger:

if __name__ == "__main__":
    from dearpygui.dearpygui import *

    create_context()
    create_viewport(title="Module Test", width=600, height=400)
    setup_dearpygui()
    
    build_frame()   # This calls your module's GUI

    show_viewport()
    start_dearpygui()
    destroy_context()