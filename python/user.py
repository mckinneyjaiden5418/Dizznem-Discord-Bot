"""User related code."""

import sqlite3
from pathlib import Path
from typing import Any, Self

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
        """,
        )

    logger.info("Database initalized.")


class User:
    """User class containing user information."""

    def __init__(
        self,
        id: int,  # noqa: A002 -- disabled for clarity, (I prefer id over user_id since user implied).
        name: str,
        money: float,
        prestige: int,
        level: int,
        message_count: int,
    ) -> None:
        """Initialize a user.

        Args:
            id (int): Discord user ID.
            name (str): Discord username.
            money (float): Money count.
            prestige (int): Prestige count.
            level (int): Current level.
            message_count (int): Number of messages sent.
        """
        self.id: int = id
        self.name: str = name
        self.money: float = money
        self.prestige: int = prestige
        self.level: int = level
        self.message_count: int = message_count

    @classmethod
    def from_db(cls, user_id: int) -> Self | None:
        """Load a user from the database.

        Args:
            user_id (int): Discord user ID.

        Returns:
            User | None: User instance if found, otherwise None.
        """
        with sqlite3.connect(DB_PATH) as conn:
            cursor: sqlite3.Cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row: Any = cursor.fetchone()

        if row is None:
            logger.warning(f"User with ID {user_id} not found in database.")
            return None

        return cls(*row)

    @classmethod
    def create_if_not_exists(cls, user_id: int, username: str) -> Self:
        """Create a new user if they don't exist in the database.

        Args:
            user_id (int): Discord user ID.
            username (str): Discord username.

        Returns:
            User: The existing or newly created user instance.
        """
        user: Self | None = cls.from_db(user_id)
        if user:
            return user

        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO users (id, name) VALUES (?, ?)", (user_id, username),
            )
            conn.commit()

        logger.debug(f"New user created: {username} ({user_id})")
        return cls.from_db(user_id) # pyright: ignore[reportReturnType]


