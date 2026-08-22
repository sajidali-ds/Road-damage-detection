import sqlite3
import os
from datetime import datetime

from config import DB_PATH

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def init_db():
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            predicted_class TEXT NOT NULL,
            confidence REAL NOT NULL,
            latitude REAL,
            longitude REAL,
            address TEXT,
            image_path TEXT,
            emailed INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def add_report(predicted_class, confidence, lat, lon, address="", image_path="", emailed=False):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO reports (predicted_class, confidence, latitude, longitude, address, image_path, emailed, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (predicted_class, confidence, lat, lon, address, image_path, int(emailed), datetime.now().isoformat()),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_reports():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports ORDER BY created_at DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
