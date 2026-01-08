"""Money bot commands."""

import random
from typing import Final

from bot.bot import DizznemBot
from discord import Color, Embed
from discord.ext import commands
from log import logger  # noqa: F401
from user import User
from utils.numbers import format_number


class MoneyMaking(commands.Cog):
    """Money making bot commands."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initiate Money.

        Args:
            bot (commands.Bot): Dizznem Bot.
        """
        self.bot: commands.Bot = bot

    # NOTE: Could probably refactor daily and weekly command to use 1 function as a way to prevent
    # redundant code.

    @commands.hybrid_command(
        name="daily",
        description="Daily money",
    )
    @commands.cooldown(rate=1, per=86400, type=commands.BucketType.user)
    async def daily(self, ctx: commands.Context) -> None:
        """Daily command.

        Args:
            ctx (commands.Context): Context.
        """
        user_id: int = ctx.author.id
        username: str = ctx.author.name
        user: User = User.create_if_not_exists(user_id=user_id, username=username)
        daily_value: int = random.randint(100_000, 1_000_000) * (  # noqa: S311
            user.prestige + 1
        )
        formatted_daily_value: str = format_number(number=daily_value)

        user.money += daily_value

        embed: Embed = Embed(
            title="Daily",
            color=Color.green(),
            description=f"You earned ${formatted_daily_value}",
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="weekly",
        description="Weekly money",
    )
    @commands.cooldown(rate=1, per=604800, type=commands.BucketType.user)
    async def weekly(self, ctx: commands.Context) -> None:
        """Weekly command.

        Args:
            ctx (commands.Context): Context.
        """
        user_id: int = ctx.author.id
        username: str = ctx.author.name
        user: User = User.create_if_not_exists(user_id=user_id, username=username)
        weekly_value: int = random.randint(1_000_000, 5_000_000) * (  # noqa: S311
            user.prestige + 1
        )
        formatted_weekly_value: str = format_number(number=weekly_value)

        user.money += weekly_value

        embed: Embed = Embed(
            title="Weekly",
            color=Color.green(),
            description=f"You earned ${formatted_weekly_value}",
        )

        await ctx.send(embed=embed)

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
