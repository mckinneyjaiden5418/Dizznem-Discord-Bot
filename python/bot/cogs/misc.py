"""Miscellaneous bot commands."""

from pathlib import Path

from bot.bot import DizznemBot
from discord import Color, Embed
from discord.ext import commands
from log import logger  # noqa: F401
from utils.misc.help import get_help_text
from utils.misc.inspiration import ensure_db, get_random_quote

DB_PATH = Path("data/inspiration.db")  # adjust if your data folder is elsewhere


class Misc(commands.Cog):
    """Miscellaneous bot commands."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initiate Misc.

        Args:
            bot (commands.Bot): Dizznem Bot.
        """
        self.bot: commands.Bot = bot
        ensure_db(DB_PATH)

    @commands.hybrid_command(name="help", description="Get all Dizznem Bot commands")
    async def help(self, ctx: commands.Context) -> None:
        """Help command.

        Args:
            ctx (commands.Context): Context.
        """
        help_text: str = get_help_text()
        embed: Embed = Embed(
            title="Commands",
            color=Color.og_blurple(),
            description=help_text,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="inspiration", description="Get an inspirational quote")
    async def inspiration(self, ctx: commands.Context) -> None:
        """Get an inspirational quote.

        Args:
            ctx (commands.Context): Context.
        """
        quote: str | None = get_random_quote(DB_PATH)
        if quote is None:
            await ctx.send("No inspirational quotes found in the database.", ephemeral=True)
            return

        embed: Embed = Embed(
            title="✨ Inspiration",
            color=Color.gold(),
            description=quote,
        )
        await ctx.send(embed=embed)


async def setup(bot: DizznemBot) -> None:
    """Setup for misc.

    Args:
        bot (commands.Bot): Dizznem Bot
    """
    await bot.add_cog(Misc(bot))