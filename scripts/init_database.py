import sqlite3
import os

DB_PATH = "data/database/honeytrap.db"

def init_database():
    """Initialize the honeypot database"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            session_id TEXT NOT NULL,
            src_ip TEXT NOT NULL,
            src_port INTEGER,
            event_type TEXT NOT NULL,
            protocol TEXT DEFAULT 'SSH',
            command TEXT,
            username TEXT,
            password TEXT,
            country TEXT DEFAULT 'Unknown',
            city TEXT DEFAULT 'Unknown',
            lat REAL,
            lon REAL,
            payload TEXT,
            severity TEXT DEFAULT 'INFO',
            cwd TEXT
        )
    """)

    # Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON logs(timestamp DESC)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_src_ip ON logs(src_ip)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_session ON logs(session_id)")

    conn.commit()
    conn.close()
    print(f"[+] Database initlialized: {DB_PATH}")

if __name__ == "__main__":
    init_database()