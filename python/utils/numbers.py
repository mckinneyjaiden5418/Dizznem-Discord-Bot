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
