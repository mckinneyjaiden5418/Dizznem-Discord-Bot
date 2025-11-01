"""Level bot commands."""

from bot.bot import DizznemBot
from discord import Color, Embed
from discord.ext import commands
from log import logger  # noqa: F401


class Level(commands.Cog):
    """Level bot commands."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initiate Level.

        Args:
            bot (commands.Bot): Dizznem Bot.
        """
        self.bot: commands.Bot = bot

    @commands.hybrid_command(
        name="level",
        description="Get your level and related information",
        aliases=["lvl"],
    )
    async def level(self, ctx: commands.Context) -> None:
        """Level command.

        Args:
            ctx (commands.Context): Context.
        """
        # finish the rest of this later.
        level_information: str = "Placeholder"
        embed: Embed = Embed(
            title="Placeholder",
            color=Color.og_blurple(),
            description=level_information,
        )
        await ctx.send(embed=embed)


async def setup(bot: DizznemBot) -> None:
    """Setup for level.

    Args:
        bot (commands.Bot): Dizznem Bot
    """
    await bot.add_cog(Level(bot))
