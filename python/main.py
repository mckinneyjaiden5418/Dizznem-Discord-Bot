"""Main."""

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from log import logger

load_dotenv()

def validate_env() -> bool:
    """Validate if .env file has required variable(s)."""
    required_vars: list[str] = ["DISCORD_BOT_TOKEN"]
    missing_vars: list[str] = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
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
    logger.info("Starting Dizznem Bot...")
    if not validate_env():
        return

    try:
        run_bot()
    except Exception as e:
        logger.error(f"Dizznem Bot failed to start: {e}")
        raise


if __name__ == "__main__":
    main()
