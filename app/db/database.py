import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "automation.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Track pipeline runs
    cur.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trigger TEXT,
            started_at TEXT,
            ended_at TEXT,
            status TEXT
        )
    """)

    # Track processed items (for deduplication)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS processed_items (
            item_id TEXT PRIMARY KEY,
            processed_at TEXT
        )
    """)

    conn.commit()
    conn.close()
