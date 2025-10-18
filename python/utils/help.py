"""Help command stuff."""
def get_help_text() -> str:
    """Get text for help command.

    Returns:
        str: Help text.
    """
    help_text_list: list[str] = [
        "$balance - Get your balance",
        "$gamble - Gamble your money",
    ]

    help_text_list.sort()

    return "\n".join(help_text_list)
