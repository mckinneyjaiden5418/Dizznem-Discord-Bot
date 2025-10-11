"""Main file for bot."""
import os
from typing import cast

import discord
from discord.ext import commands
from log import logger


def run_bot() -> None:
    """Run discord bot."""
    token: str = cast("str", os.getenv("DISCORD_BOT_TOKEN"))
    test_channel: int = int(cast("str", os.getenv("TEST_CHANNEL_ID")))

    intents: discord.Intents = discord.Intents.default()
    intents.message_content = True

    bot: commands.Bot = commands.Bot(command_prefix="$", intents=intents)

    @bot.event
    async def on_ready() -> None:
        channel: discord.TextChannel = cast("discord.TextChannel", bot.get_channel(test_channel))
        await channel.send("Hello")

    bot.run(token=token)
