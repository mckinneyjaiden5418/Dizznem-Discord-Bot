"""Money bot commands."""

from bot.bot import DizznemBot
from discord import Asset, Color, Embed
from discord.ext import commands
from log import logger  # noqa: F401
from user import User
from utils.money import format_money


class Money(commands.Cog):
    """Money bot commands."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initiate Money.

        Args:
            bot (commands.Bot): Dizznem Bot.
        """
        self.bot: commands.Bot = bot

    @commands.hybrid_command(
        name="balance", description="Get your balance", aliases=["bal"],
    )
    async def balance(self, ctx: commands.Context) -> None:
        """Balance command.

        Args:
            ctx (commands.Context): Context.
        """
        user_id: int = ctx.author.id
        username: str = ctx.author.name
        display_name: str = ctx.author.display_name
        avatar: Asset | None = ctx.author.avatar
        user: User = User.create_if_not_exists(user_id=user_id, username=username)
        user_money: str = format_money(user.money)

        embed: Embed = Embed(
            title="Balance", color=Color.og_blurple(), description=f"${user_money}",
        )
        embed.set_author(name=display_name, icon_url=avatar)

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="gamble", description="Gamble your money", aliases=["gamba"],
    )
    async def gamble(self, ctx: commands.Context) -> None:
        """Gamble command.

        Args:
            ctx (commands.Context): Context.
        """


async def setup(bot: DizznemBot) -> None:
    """Setup for money.

    Args:
        bot (commands.Bot): Dizznem Bot
    """
    await bot.add_cog(Money(bot))
