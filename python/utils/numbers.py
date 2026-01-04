"""Number related util."""


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
    cleaned: str = money_str.replace("$", "").replace(",", "").strip()

    try:
        value = float(cleaned)
    except ValueError as e:
        msg: str = f"Invalid money value: {money_str}"
        raise ValueError(msg) from e

    return value
