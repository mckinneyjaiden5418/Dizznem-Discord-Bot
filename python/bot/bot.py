"""Main file for bot."""
import os
from pathlib import Path
from typing import cast

from discord import Intents, Message, TextChannel
from discord.ext import commands
from log import logger
from user import autosave


class DizznemBot(commands.Bot):
    """Dizznem Bot class."""

    def __init__(self) -> None:
        """Initiate Dizznem Bot config/intents."""
        intents: Intents = Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="$", intents=intents, help_command=None)

        self.token: str = cast("str", os.getenv("DISCORD_BOT_TOKEN"))
        self.bot_tag: str = cast("str", os.getenv("DISCORD_BOT_TAG", "dizznem"))
        self.test_channel_id: int = int(cast("str", os.getenv("TEST_CHANNEL_ID", "0")))


    async def setup_hook(self) -> None:
        """Load all cogs and start autosave for database."""
        logger.info("Loading cogs...")
        cogs_path: Path = Path(__file__).parent/"cogs"
        for file in cogs_path.iterdir():
            if file.is_file() and file.suffix == ".py" and not file.name.startswith("_"):
                ext: str = f"bot.cogs.{file.stem}"
                try:
                    await self.load_extension(ext)
                    logger.info(f"Loaded cog {ext}.")
                except FileNotFoundError as e:
                    logger.error(f"Failed to load cog {ext}: {e}.")

        self.loop.create_task(autosave())
        logger.info("Autosave task started.")


    async def on_ready(self) -> None:
        """Bot startup."""
        channel: TextChannel = cast("TextChannel", self.get_channel(self.test_channel_id))
        await channel.send("Hello")
        logger.info("Bot started.")


    async def on_message(self, message: Message) -> None:
        """Handle message events.

        Args:
            message (Message): User message.
        """
        if message.author == self.user or message.author.bot:
            return

        # Level feature here when added.

        triggers: list[tuple[str, str]] = [
            (self.bot_tag, ""),
            ("wackdiff", "cuckdiff*"),
            ("wack", "cuck*"),
            ("minor", "A MINORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR"),
            ("spark", "Please spark Dizznem please!!!!!!"),
            ("dizznem", "dihhnem*"),
            ("cook", "We need to cook."),
            ("call", "Better Call Saul!"),
            # ("gay", "Dizznem Bot is an LGBTQ+ ally!"),  # Vaulted pride month command
            ("limit", "WE SAIYANS HAVE NO LIMITS!!!"),
            ("super speed clicker", "https://www.roblox.com/games/139600379808227/Super-Speed-Clicker"),
        ]

        content: str = message.content.lower()
        for trigger, response in triggers:
            if trigger not in content:
                continue

            if trigger == self.bot_tag:
                await message.channel.send("Placeholder!")
                # AI feature here when added.
            else:
                await message.channel.send(response)

            break

        await self.process_commands(message)


    def run_bot(self) -> None:
        """Run bot."""
        super().run(self.token)
