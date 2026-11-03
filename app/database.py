import sqlite3

def get_db_connection():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            role TEXT
        )
    """)
    cursor.execute("INSERT INTO users (username, email, role) VALUES ('admin', 'admin@example.com', 'admin')")
    cursor.execute("INSERT INTO users (username, email, role) VALUES ('alice', 'alice@example.com', 'user')")
    conn.commit()
    return conn