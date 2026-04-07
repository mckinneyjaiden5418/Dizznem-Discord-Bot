"""Number related util."""

from pathlib import Path

from user import User
from utils.money.stocks import get_user_stocks


def format_number(number: float) -> str:
    """Format money.

    Args:
        number (float): Number to be formatted.

    Returns:
        str: Formatted money as a readable string.
    """
    formatted_money: str = f"{number:,.2f}"
    return formatted_money.removesuffix(".00")


def convert_money_str(money_str: str) -> float:
    """Convert money string to valid float.

    Args:
        money_str (str): Money formatted string.

    Returns:
        float: Valid float.
    """
    if isinstance(money_str, (int, float)):
        return money_str

    cleaned: str = money_str.replace("$", "").replace(",", "").strip()

    try:
        value = float(cleaned)
    except ValueError as e:
        msg: str = f"Invalid money value: {money_str}"
        raise ValueError(msg) from e

    return value


def get_net_worth(user: User, db_path: Path) -> float:
    """Calculate total net worth from balance and stock value.

    Args:
        user (User): User object.
        db_path (Path): Path to users.db.

    Returns:
        float: Total networth.
    """
    stock_value: float = sum(value for _, _, value in get_user_stocks(db_path, user.id))
    return user.money + stock_value


def format_duration(seconds: float) -> str:
    """Format cooldown time.

    Args:
        seconds (float): Seconds until cooldown expires.

    Returns:
        str: Formatted duration string.
    """
    seconds = round(seconds)

    days: int
    hours: int
    minutes: int
    remainder: int
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts: list[str] = []

    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return ", ".join(parts)
