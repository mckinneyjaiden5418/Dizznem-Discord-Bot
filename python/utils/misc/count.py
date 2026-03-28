"""Count database utilities."""

import sqlite3
from pathlib import Path


def ensure_count_db(db_path: Path) -> None:
    """Create count.db with a default count of 0 if it doesn't exist.

    Args:
        db_path (Path): Path to the SQLite database file.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS count (
                id    INTEGER PRIMARY KEY,
                count INTEGER NOT NULL
            )
        """,
        )
        cursor.execute("SELECT COUNT(*) FROM count")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO count (id, count) VALUES (1, 0)")
        conn.commit()


def increment_count(db_path: Path) -> int:
    """Increment the count by 1 and return the new value.

    Args:
        db_path (Path): Path to the SQLite database file.

    Returns:
        int: The updated count value.
    """
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("UPDATE count SET count = count + 1 WHERE id = 1")
        cursor.execute("SELECT count FROM count WHERE id = 1")
        new_count: int = cursor.fetchone()[0]
        conn.commit()
    return new_count
