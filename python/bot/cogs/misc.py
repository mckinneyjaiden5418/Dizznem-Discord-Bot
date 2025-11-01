"""Miscellaneous bot commands."""

from bot.bot import DizznemBot
from discord import Color, Embed
from discord.ext import commands
from log import logger  # noqa: F401
from utils.help import get_help_text


class Misc(commands.Cog):
    """Miscellaneous bot commands."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initiate Misc.

        Args:
            bot (commands.Bot): Dizznem Bot.
        """
        self.bot: commands.Bot = bot

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


async def setup(bot: DizznemBot) -> None:
    """Setup for misc.

    Args:
        bot (commands.Bot): Dizznem Bot
    """
    await bot.add_cog(Misc(bot))
