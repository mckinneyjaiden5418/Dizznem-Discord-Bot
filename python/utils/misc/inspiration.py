"""Inspiration database utilities."""

import sqlite3
from pathlib import Path

DEFAULT_QUOTES: list[str] = [
    "The only way to do great work is to love what you do.",
    "In the middle of every difficulty lies opportunity.",
    "It does not matter how slowly you go as long as you do not stop.",
    "Life is what happens when you're busy making other plans.",
    "The future belongs to those who believe in the beauty of their dreams.",
]

INSPIRATION_DB_PATH: Path = Path("data/inspiration.db")


def ensure_inspiration_db(db_path: Path) -> None:
    """Create inspiration.db with default quotes if it doesn't exist.

    Args:
        db_path (Path): Path to the SQLite database file.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                messageID INTEGER PRIMARY KEY AUTOINCREMENT,
                message   TEXT NOT NULL
            )
        """,
        )
        cursor.execute("SELECT COUNT(*) FROM messages")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO messages (message) VALUES (?)",
                [(q,) for q in DEFAULT_QUOTES],
            )
        conn.commit()


def add_quote(db_path: Path, quote: str) -> None:
    """Add a quote to the inspiration database.

    Args:
        db_path (Path): SQLite database path.
        quote (str): Quote to add.
    """
    ensure_inspiration_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.execute(
            "SELECT IFNULL(MAX(messageID), 0) + 1 FROM messages",
        )
        next_id: int = cursor.fetchone()[0]
        conn.execute(
            "INSERT INTO messages (messageID, message) VALUES (?, ?)",
            (next_id, quote),
        )
        conn.commit()


def get_random_quote(db_path: Path) -> str | None:
    """Fetch a random inspirational quote from the database.

    Args:
        db_path (Path): Path to the SQLite database file.

    Returns:
        str | None: A random quote string, or None if the table is empty.
    """
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT message FROM messages ORDER BY RANDOM() LIMIT 1")
        row: tuple[str] | None = cursor.fetchone()
    return row[0] if row else None
