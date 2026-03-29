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


def get_networth_leaderboard(db_path: Path) -> list[tuple[str, float]]:
    """Get top 10 users by net worth (balance + stock value).

    Args:
        db_path (Path): Path to users.db.

    Returns:
        list[tuple[str, float]]: List of (username, networth).
    """
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT id, name, money FROM users")
        rows: list[tuple] = cursor.fetchall()

    results: list[tuple[str, float]] = []
    for user_id, name, money in rows:
        holdings: list[tuple[str, int, float]] = get_user_stocks(STOCKS_DB_PATH, user_id)
        stock_value: float = sum(value for _, _, value in holdings)
        results.append((name, money + stock_value))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:10]


def build_leaderboard_embed(
    category: str,
) -> Embed:
    """Build a leaderboard embed for the given category.

    Args:
        category (str): One of 'balance', 'networth', 'prestige'.

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
        rows: list[tuple[str, float]] = get_networth_leaderboard(USERS_DB_PATH)
        title: str = "📊 Net Worth Leaderboard"
        color: Color = Color.gold()
        lines: list[str] = [
            f"`{i + 1}.` **{name}** — ${format_number(val)}"
            for i, (name, val) in enumerate(rows)
        ]
    else:  # prestige
        rows: list[tuple[str, float]] = get_prestige_leaderboard(USERS_DB_PATH) # pyright: ignore[reportAssignmentType]
        title: str = "⭐ Prestige Leaderboard"
        color: Color = Color.og_blurple()
        lines: list[str] = [
            f"`{i + 1}.` **{name}** — {format_number(val)} prestiges"
            for i, (name, val) in enumerate(rows)
        ]

    embed = Embed(
        title=title,
        color=color,
        description="\n".join(lines) if lines else "No users found.",
    )
    return embed  # noqa: RET504
