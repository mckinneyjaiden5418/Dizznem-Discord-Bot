"""Money bot commands."""
from bot.bot import DizznemBot
from discord.ext import commands
from log import logger
from user import User


class Money(commands.Cog):
    """Money bot commands."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initiate Misc.

        Args:
            bot (commands.Bot): Dizznem Bot.
        """
        self.bot: commands.Bot= bot


    @commands.hybrid_command(name="balance", description="Get your balance",aliases=["bal"])
    async def balance(self, ctx: commands.Context) -> None:
        """Get user balance.

        Args:
            ctx (commands.Context): Context.
        """
        user_id: int = ctx.author.id
        username: str = ctx.author.name
        user: User = User.create_if_not_exists(user_id=user_id, username=username)

        logger.debug(user.money)


    @commands.hybrid_command(name="gamble", description="Gamble your money", aliases=["gamba"])
    async def gamble(self, ctx: commands.Context) -> None:
        """Gamble money.

        Args:
            ctx (commands.Context): Context.
        """


async def setup(bot: DizznemBot) -> None:
    """Setup for money.

    Args:
        bot (commands.Bot): Dizznem Bot
    """
    await bot.add_cog(Money(bot))
