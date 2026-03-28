"""Miscellaneous bot commands."""

from pathlib import Path

from bot.bot import DizznemBot
from discord import Color, Embed
from discord.ext import commands
from log import logger  # noqa: F401
from utils.misc.count import ensure_count_db, increment_count
from utils.misc.help import get_help_text
from utils.misc.inspiration import ensure_inspiration_db, get_random_quote

DB_PATH: Path = Path("data/inspiration.db")
COUNT_DB_PATH: Path = Path("data/count.db")


class Misc(commands.Cog):
    """Miscellaneous bot commands."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initiate Misc.

        Args:
            bot (commands.Bot): Dizznem Bot.
        """
        self.bot: commands.Bot = bot
        ensure_inspiration_db(DB_PATH)
        ensure_count_db(COUNT_DB_PATH)

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

    @commands.hybrid_command(
        name="inspiration",
        description="Get an inspirational quote",
    )
    async def inspiration(self, ctx: commands.Context) -> None:
        """Inspiration command.

        Args:
            ctx (commands.Context): Context.
        """
        quote: str | None = get_random_quote(DB_PATH)
        if quote is None:
            await ctx.send(
                "No inspirational quotes found in the database.",
                ephemeral=True,
            )
            return

        embed: Embed = Embed(
            title="✨ Inspiration",
            color=Color.gold(),
            description=quote,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="count", description="Increase count by 1")
    async def count(self, ctx: commands.Context) -> None:
        """Count command.

        Args:
            ctx (commands.Context): Context.
        """
        new_count: int = increment_count(COUNT_DB_PATH)
        embed: Embed = Embed(
            title="🔢 Count",
            color=Color.og_blurple(),
            description=f"The count is now **{new_count}**.",
        )
        await ctx.send(embed=embed)


async def setup(bot: DizznemBot) -> None:
    """Setup for misc.

    Args:
        bot (commands.Bot): Dizznem Bot
    """
    await bot.add_cog(Misc(bot))
