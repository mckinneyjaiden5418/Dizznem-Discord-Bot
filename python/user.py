"""User related code."""

import sqlite3
from pathlib import Path

from log import logger

DB_PATH: Path = Path("data/users.db")


def init_db() -> None:
    """Initalize database if not done so already."""
    logger.info("Initiating database...")

    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                money REAL DEFAULT 0,
                prestige INTEGER DEFAULT 0,
                level INTEGER DEFAULT 0,
                message_count INTEGER DEFAULT 0
            )
        """
        )

    logger.info("Database initalized.")


class User:
    """User class containing user information."""

    def __init__(
        self,
        id: int,
        name: str,
        money: float,
        prestige: int,
        level: int,
        message_count: int,
    ) -> None:
        """Initialize a user.

        Args:
            id (int): ID.
            name (str): Discord username.
            money (float): Money count.
            prestige (int): Prestige count.
            level (int): Current level.
            message_count (int): # of messages.
        """

    @classmethod
    def from_db(cls, user_id: int) -> None:
        """Load a user from the database.

        Args:
            user_id (int): _description_
        """
        with sqlite3.connect(DB_PATH) as conn:
            cur: sqlite3.Cursor = conn.execute(
                """
                UPDATE users
                SET name = ?, prestige = ?
                WHERE id = ?
            """,
                (self.username, self.points, self.money, self.user_id),
            )
            conn.commit()
