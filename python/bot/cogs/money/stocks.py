"""Short description of the cog."""

from bot.bot import DizznemBot
from discord.ext import commands
from log import logger  # noqa: F401 -- Import logger for possible use.


class CogName(commands.Cog):
    """Class description."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initialize the cog.

        Args:
            bot (DizznemBot): Dizznem Bot.
        """
        self.bot: DizznemBot = bot

    # --------------------
    # Commands
    # --------------------

    @commands.hybrid_command(name="command_name", description="Command description")
    async def command_name(self, ctx: commands.Context) -> None:
        """Command docstring.

        Args:
            ctx (commands.Context): Context.
        """
        await ctx.send("Placeholder.")


async def setup(bot: DizznemBot) -> None:
    """Load the cog.

    Args:
        bot (DizznemBot): Dizznem Bot.
    """
    await bot.add_cog(CogName(bot))
