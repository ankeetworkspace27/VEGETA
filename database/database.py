import sqlite3
from datetime import datetime
from pathlib import Path


# Location of the database file
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "vegeta.db"


def get_connection():
    """
    Create a connection to VEGETA's SQLite database.
    """

    connection = sqlite3.connect(DB_PATH)

    # Allows us to access database columns by name
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """
    Create the required database tables.
    """

    with get_connection() as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                value TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        connection.commit()


def save_memory(key, value, category="general"):
    """
    Save a new memory or update an existing memory.
    """

    now = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO memories
            (key, value, category, created_at, updated_at)

            VALUES (?, ?, ?, ?, ?)

            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                category = excluded.category,
                updated_at = excluded.updated_at
            """,
            (key, value, category, now, now),
        )

        connection.commit()


def get_memory(key):
    """
    Get one memory using its key.
    """

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM memories
            WHERE key = ?
            """,
            (key,),
        ).fetchone()

    if row:
        return dict(row)

    return None


def get_all_memories():
    """
    Get all memories stored in the database.
    """

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT *
            FROM memories
            ORDER BY id ASC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def delete_memory(key):
    """
    Delete a memory using its key.
    """

    with get_connection() as connection:

        cursor = connection.execute(
            """
            DELETE FROM memories
            WHERE key = ?
            """,
            (key,),
        )

        connection.commit()

    return cursor.rowcount > 0


# Create the database and tables when this module is loaded.
initialize_database()