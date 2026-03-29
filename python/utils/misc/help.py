"""Help text utility."""

from discord.ext import commands


def get_help_text(bot: commands.Bot) -> str:
    """Generate help text dynamically from all loaded bot commands.

    Args:
        bot (commands.Bot): The bot instance.

    Returns:
        str: Formatted help text.
    """
    lines: list[str] = []
    for cmd in sorted(bot.commands, key=lambda c: c.name):
        description: str = cmd.description or cmd.help or "No description."
        lines.append(f"**${cmd.name}** — {description}")
    return "\n".join(lines)
