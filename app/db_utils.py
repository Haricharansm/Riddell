import sqlite3

DB_PATH = "assets/riddell_projects.db"  # Adjust path as needed

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cluster INTEGER,
            helmet_size TEXT,
            foam_type TEXT,
            shell_material TEXT,
            stage TEXT,
            owner TEXT,
            target_date TEXT,
            status_notes TEXT
        )
    """)
    conn.commit()
    conn.close()
