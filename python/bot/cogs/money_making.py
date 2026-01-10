"""Money bot commands."""

import random
from typing import Final

from bot.bot import DizznemBot
from discord import Color, Embed
from discord.ext import commands
from log import logger  # noqa: F401
from user import User
from utils.general import reset_cd
from utils.numbers import convert_money_str, format_number


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
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def gamble(self, ctx: commands.Context, amount: str) -> None:
        """Gamble command.

        Args:
            ctx (commands.Context): Context.
            amount (str): Gamble amount, all, half, or numerical.
        """
        user_id: int = ctx.author.id
        username: str = ctx.author.name
        user: User = User.create_if_not_exists(user_id=user_id, username=username)

        try:
            if amount.lower() == "all":
                gamble_amount: float = user.money
            elif amount.lower() == "half":
                gamble_amount: float = user.money / 2
            else:
                gamble_amount: float = convert_money_str(money_str=amount)
        except ValueError:
            reset_cd(ctx=ctx)
            embed: Embed = Embed(
                title="Error",
                color=Color.red(),
                description="Invalid money format.",
            )
            await ctx.send(embed=embed)
            return

        gamble_amount = round(gamble_amount, 2)

        if gamble_amount <= 0:
            reset_cd(ctx=ctx)
            embed: Embed = Embed(
                title="Error",
                color=Color.red(),
                description="Gamble amount must be greater than 0.",
            )
            await ctx.send(embed=embed)
            return

        if user.money < gamble_amount:
            reset_cd(ctx=ctx)
            embed: Embed = Embed(
                title="Error",
                color=Color.red(),
                description="You do not have enough money to gamble that amount.",
            )
            await ctx.send(embed=embed)
            return

        WIN: Final[int] = 400
        LOSE: Final[int] = 950
        TRIPLE_WIN: Final[int] = 999
        roll: int = random.randint(1, 1000)  # noqa: S311
        formatted_amount: str = format_number(number=gamble_amount)

        if roll <= WIN:
            user.money += gamble_amount
            embed: Embed = Embed(
                title="🎉 You won!",
                color=Color.green(),
                description=f"You won **${formatted_amount}**!",
            )
        elif roll <= LOSE:
            user.money -= gamble_amount
            embed: Embed = Embed(
                title="💀 You Lost",
                color=Color.red(),
                description=f"You lost **${formatted_amount}**!",
            )
        elif roll <= TRIPLE_WIN:
            winnings: float = gamble_amount * 3
            formatted_winnings: str = format_number(number=winnings)
            user.money += winnings
            embed: Embed = Embed(
                title="🔥 3x WIN!",
                color=Color.green(),
                description=f"You won **${formatted_winnings}**!",
            )
        else:
            winnings: float = gamble_amount * 10
            formatted_winnings: str = format_number(number=winnings)
            user.money += winnings
            embed: Embed = Embed(
                title="💎 JACKPOT!",
                color=Color.gold(),
                description=f"You hit the jackpot and won **${formatted_winnings}**!",
            )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="aba",
        description="Anime Battle Arena trivia for money",
        aliases=["animebattlearena"],
    )
    @commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
    async def aba(self, ctx: commands.Context) -> None:
        """ABA command.

        Args:
            ctx (commands.Context): Context.
        """

    @commands.hybrid_command(
        name="rogue",
        description="Rogue Lineage trivia for money",
        aliases=["roguelineage"],
    )
    @commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
    async def rogue(self, ctx: commands.Context) -> None:
        """Rogue command.

        Args:
            ctx (commands.Context): Context.
        """

    @commands.hybrid_command(
        name="trivia",
        description="Trivia for money",
    )
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def trivia(self, ctx: commands.Context) -> None:
        """Trivia command.

        Args:
            ctx (commands.Context): Context.
        """


async def setup(bot: DizznemBot) -> None:
    """Setup for money making.

    Args:
        bot (commands.Bot): Dizznem Bot
    """
    await bot.add_cog(MoneyMaking(bot))
