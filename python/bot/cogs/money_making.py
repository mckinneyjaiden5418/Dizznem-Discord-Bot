"""Money bot commands."""

from bot.bot import DizznemBot
from discord.ext import commands
from log import logger  # noqa: F401


class MoneyMaking(commands.Cog):
    """Money making bot commands."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initiate Money.

        Args:
            bot (commands.Bot): Dizznem Bot.
        """
        self.bot: commands.Bot = bot

    @commands.hybrid_command(
        name="gamble",
        description="Gamble your money",
        aliases=["gamba"],
    )
    async def gamble(self, ctx: commands.Context) -> None:
        """Gamble command.

        Args:
            ctx (commands.Context): Context.
        """


async def setup(bot: DizznemBot) -> None:
    """Setup for money making.

    Args:
        bot (commands.Bot): Dizznem Bot
    """
    await bot.add_cog(MoneyMaking(bot))
