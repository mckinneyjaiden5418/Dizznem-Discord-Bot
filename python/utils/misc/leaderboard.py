"""Leaderboard utilities."""

import sqlite3
from pathlib import Path

from discord import Color, Embed
from utils.money.stocks import USERS_DB_PATH as STOCKS_DB_PATH
from utils.money.stocks import get_user_stocks
from utils.numbers import format_number

USERS_DB_PATH: Path = Path("data/users.db")


def get_balance_leaderboard(db_path: Path) -> list[tuple[str, float]]:
    """Get top 10 users by balance.

    Args:
        db_path (Path): Path to users.db.

    Returns:
        list[tuple[str, float]]: List of (username, balance).
    """
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "SELECT name, money FROM users ORDER BY money DESC LIMIT 10",
        )
        return cursor.fetchall()


def get_prestige_leaderboard(db_path: Path) -> list[tuple[str, int]]:
    """Get top 10 users by prestige.

    Args:
        db_path (Path): Path to users.db.

    Returns:
        list[tuple[str, int]]: List of (username, prestige).
    """
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "SELECT name, prestige FROM users ORDER BY prestige DESC LIMIT 10",
        )
        return cursor.fetchall()


def get_networth_leaderboard(db_path: Path, limit: int = 10) -> list[tuple[str, float]]:
    """Get top users by net worth (balance + stock value).

    Args:
        db_path (Path): Path to users.db.
        limit (int): Number of results to return. Defaults to 10.

    Returns:
        list[tuple[str, float]]: List of (username, networth).
    """
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT id, name, money FROM users")
        rows: list[tuple] = cursor.fetchall()

    results: list[tuple[str, float]] = []
    for uid, name, money in rows:
        holdings: list[tuple[str, int, float]] = get_user_stocks(STOCKS_DB_PATH, uid)
        stock_value: float = sum(value for _, _, value in holdings)
        results.append((name, money + stock_value))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:limit]


def get_level_leaderboard(db_path: Path) -> list[tuple[str, int]]:
    """Get top 10 users by level.

    Args:
        db_path (Path): Path to users.db.

    Returns:
        list[tuple[str, int]]: List of (username, level).
    """
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "SELECT name, level FROM users ORDER BY level DESC LIMIT 10",
        )
        return cursor.fetchall()


def build_leaderboard_embed(category: str) -> Embed:
    """Build a leaderboard embed for the given category.

    Args:
        category (str): One of 'balance', 'networth', 'prestige', 'level'.

    Returns:
        Embed: The leaderboard embed.
    """
    if category == "balance":
        rows: list[tuple[str, float]] = get_balance_leaderboard(USERS_DB_PATH)
        title: str = "💰 Balance Leaderboard"
        color: Color = Color.green()
        lines: list[str] = [
            f"`{i + 1}.` **{name}** — ${format_number(val)}"
            for i, (name, val) in enumerate(rows)
        ]
    elif category == "networth":
        rows = get_networth_leaderboard(USERS_DB_PATH)
        title = "📊 Net Worth Leaderboard"
        color = Color.gold()
        lines = [
            f"`{i + 1}.` **{name}** — ${format_number(val)}"
            for i, (name, val) in enumerate(rows)
        ]
    elif category == "prestige":
        rows = get_prestige_leaderboard(
            USERS_DB_PATH,
        )  # pyright: ignore[reportAssignmentType]
        title = "⭐ Prestige Leaderboard"
        color = Color.og_blurple()
        lines = [
            f"`{i + 1}.` **{name}** — {format_number(val)} prestiges"
            for i, (name, val) in enumerate(rows)
        ]
    else:  # level
        rows = get_level_leaderboard(
            USERS_DB_PATH,
        )  # pyright: ignore[reportAssignmentType]
        title = "📈 Level Leaderboard"
        color = Color.blue()
        lines = [
            f"`{i + 1}.` **{name}** — Level {format_number(val)}"
            for i, (name, val) in enumerate(rows)
        ]

    return Embed(
        title=title,
        color=color,
        description="\n".join(lines) if lines else "No users found.",
    )


def get_balance_rank(db_path: Path, user_id: int) -> int | None:
    """Get a user's rank by balance.

    Args:
        db_path (Path): Path to users.db.
        user_id (int): Discord user ID.

    Returns:
        int | None: Rank (1-indexed), or None if user not found.
    """
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) + 1 FROM users
            WHERE money > (SELECT money FROM users WHERE id = ?)
            """,
            (user_id,),
        )
        row: tuple = cursor.fetchone()
    return row[0] if row else None


def get_networth_rank(db_path: Path, user_id: int) -> int | None:
    """Get a user's rank by net worth.

    Args:
        db_path (Path): Path to users.db.
        user_id (int): Discord user ID.

    Returns:
        int | None: Rank (1-indexed), or None if user not found.
    """
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT id, name, money FROM users")
        rows: list[tuple] = cursor.fetchall()

    results: list[tuple[int, float]] = []
    for uid, _, money in rows:
        holdings: list[tuple[str, int, float]] = get_user_stocks(STOCKS_DB_PATH, uid)
        stock_value: float = sum(value for _, _, value in holdings)
        results.append((uid, money + stock_value))

    results.sort(key=lambda x: x[1], reverse=True)
    for i, (uid, _) in enumerate(results):
        if uid == user_id:
            return i + 1
    return None


def get_prestige_rank(db_path: Path, user_id: int) -> int | None:
    """Get a user's rank by prestige.

    Args:
        db_path (Path): Path to users.db.
        user_id (int): Discord user ID.

    Returns:
        int | None: Rank (1-indexed), or None if user not found.
    """
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) + 1 FROM users
            WHERE prestige > (SELECT prestige FROM users WHERE id = ?)
            """,
            (user_id,),
        )
        row: tuple = cursor.fetchone()
    return row[0] if row else None


def get_level_rank(db_path: Path, user_id: int) -> int | None:
    """Get a user's rank by level.

    Args:
        db_path (Path): Path to users.db.
        user_id (int): Discord user ID.

    Returns:
        int | None: Rank (1-indexed), or None if user not found.
    """
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) + 1 FROM users
            WHERE level > (SELECT level FROM users WHERE id = ?)
            """,
            (user_id,),
        )
        row: tuple = cursor.fetchone()
    return row[0] if row else None


def get_all_ranks(db_path: Path, user_id: int) -> dict[str, int | None]:
    """Get a user's rank across all leaderboard categories.

    Args:
        db_path (Path): Path to users.db.
        user_id (int): Discord user ID.

    Returns:
        dict[str, int | None]: Ranks keyed by category name.
    """
    return {
        "balance": get_balance_rank(db_path, user_id),
        "networth": get_networth_rank(db_path, user_id),
        "prestige": get_prestige_rank(db_path, user_id),
        "level": get_level_rank(db_path, user_id),
    }
