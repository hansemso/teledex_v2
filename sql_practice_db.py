import sqlite3

def create_connection():
    return sqlite3.connect(":memory:")

def setup_database(conn):
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            city TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            amount REAL,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    """)

    customers = [
        (1, "Alice", "New York"),
        (2, "Bob", "Chicago"),
        (3, "Charlie", "New York"),
    ]

    orders = [
        (1, 1, 120.50),
        (2, 1, 75.00),
        (3, 2, 200.00),
        (4, 3, 50.00),
    ]

    cur.executemany("INSERT INTO customers VALUES (?,?,?)", customers)
    cur.executemany("INSERT INTO orders VALUES (?,?,?)", orders)

    conn.commit()