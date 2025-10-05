"""Main."""

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from log import log

load_dotenv()

def validate_env() -> bool:
    """Validate if .env file has required variable(s)."""
    required_vars: list[str] = ["DISCORD_BOT_TOKEN"]
    missing_vars: list[str] = [var for var in required_vars if not os.getenv(var)]

    # Put logger info here later
    return not missing_vars


def run_bot() -> None: # Move this to bot.py later.
    """Run discord bot."""
    token: str | None = os.getenv("DISCORD_BOT_TOKEN")

    intents: discord.Intents = discord.Intents.default()
    intents.message_content = True

    bot: commands.Bot = commands.Bot(command_prefix="$", intents=intents)

    bot.run(token=token) # pyright: ignore[reportArgumentType]


def main() -> None:
    """Start bot."""
    log.debug("test")
    # Put logger info here later
    if not validate_env():
        return

    # Put logger info here later

    try:
        run_bot()
    except Exception as e:  # noqa: F841, TRY203
        # Put logger info here later
        raise


if __name__ == "__main__":
    main()
