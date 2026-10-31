import sqlite3
from pathlib import Path
from datetime import datetime


PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
DATABASE_PATH = DATA_DIR / "enquiries.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS enquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                service TEXT NOT NULL,
                message TEXT,
                status TEXT NOT NULL DEFAULT 'New',
                created_at TEXT NOT NULL
            )
        """)


def add_enquiry(customer_name, email, phone, service, message):
    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO enquiries (
                customer_name,
                email,
                phone,
                service,
                message,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_name,
            email,
            phone,
            service,
            message,
            "New",
            datetime.now().isoformat(timespec="seconds")
        ))

        return cursor.lastrowid


def get_enquiries():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT *
            FROM enquiries
            ORDER BY created_at DESC
        """).fetchall()

        return [dict(row) for row in rows]


def update_enquiry_status(enquiry_id, status):
    allowed_statuses = {
        "New",
        "Contacted",
        "Completed"
    }

    if status not in allowed_statuses:
        raise ValueError("Invalid enquiry status.")

    with get_connection() as connection:
        cursor = connection.execute("""
            UPDATE enquiries
            SET status = ?
            WHERE id = ?
        """, (status, enquiry_id))

        return cursor.rowcount > 0