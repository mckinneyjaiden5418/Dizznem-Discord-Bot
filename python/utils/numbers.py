"""Number related util."""


def format_money(money: float) -> str:
    """Format money.

    Args:
        money (float): Money.

    Returns:
        str: Formatted money as a readable string.
    """
    formatted_money: str = f"{money:,.2f}"
    return formatted_money.removesuffix(".00")
