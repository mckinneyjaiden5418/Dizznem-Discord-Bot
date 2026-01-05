"""Money bot commands."""

from typing import Literal

from bot.bot import DizznemBot
from discord import Asset, Color, Embed, Member
from discord.ext import commands
from log import logger  # noqa: F401
from user import User
from utils.numbers import convert_money_str, format_number


class Money(commands.Cog):
    """Money bot commands."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initiate Money.

        Args:
            bot (commands.Bot): Dizznem Bot.
        """
        self.bot: commands.Bot = bot

    @commands.hybrid_command(
        name="balance",
        description="Get your balance",
        aliases=["bal"],
    )
    async def balance(self, ctx: commands.Context, member: Member | None) -> None:
        """Balance command.

        Args:
            ctx (commands.Context): Context.
            member (Member | None): Member if mentioned.
        """
        user_id: int = member.id if member else ctx.author.id
        username: str = member.name if member else ctx.author.name
        display_name: str = member.display_name if member else ctx.author.display_name
        avatar: Asset | None = member.avatar if member else ctx.author.avatar
        user: User = User.create_if_not_exists(user_id=user_id, username=username)
        user_money: str = format_number(number=user.money)

        embed: Embed = Embed(
            title="Balance",
            color=Color.og_blurple(),
            description=f"${user_money}",
        )
        embed.set_author(name=display_name, icon_url=avatar)

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="give",
        description="Give your money to another user",
        aliases=["transfer"],
    )
    async def give(
        self, ctx: commands.Context, member: Member, amount: str,
    ) -> None:
        """Give command.

        Args:
            ctx (commands.Context): Context.
            member (Member | None): Member to give money to.
            amount (str): Amount to give.
        """
        try:
            amount_float: float = convert_money_str(money_str=amount)
        except ValueError:
            await ctx.send(
                embed=Embed(
                    title="Error",
                    color=Color.red(),
                    description="Invalid money format.",
                ),
            )
            return

        if amount_float <= 0:
            embed: Embed = Embed(
                title="Error",
                color=Color.red(),
                description="Amount must be greater than 0.",
            )
            await ctx.send(embed=embed)
            return

        max_transfer_amount: Literal[5_000_000] = 5_000_000

        if amount_float > max_transfer_amount:
            embed: Embed = Embed(
                title="Error",
                color=Color.red(),
                description="Amount must be less than or equal to 5 Million.",
            )
            await ctx.send(embed=embed)
            return

        if member.id == ctx.author.id:
            await ctx.send(
                embed=Embed(
                    title="Error",
                    color=Color.red(),
                    description="You cannot give money to yourself.",
                ),
            )
            return

        formatted_amount: str = format_number(number=amount_float)
        sender_id: int = ctx.author.id
        sender_username: str = ctx.author.name
        recipient_id: int = member.id
        recipient_username: str = member.name
        recipient_display_name: str = member.display_name

        sender_user: User = User.create_if_not_exists(
            user_id=sender_id,
            username=sender_username,
        )

        if sender_user.money < amount_float:
            embed: Embed = Embed(
                title="Error",
                color=Color.red(),
                description="You do not have enough money to send this amount.",
            )
            await ctx.send(embed=embed)
            return

        recipient_user: User = User.create_if_not_exists(
            user_id=recipient_id,
            username=recipient_username,
        )

        recipient_user.money += amount_float
        sender_user.money -= amount_float

        embed: Embed = Embed(
            title="Success",
            color=Color.green(),
            description=f"Successfully gave {recipient_display_name} ${formatted_amount}",
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="networth",
        description="Get your networth",
    )
    async def networth(self, ctx: commands.Context, member: Member | None) -> None:
        """Networth command.

        Args:
            ctx (commands.Context): Context.
            member (Member | None): Member if mentioned.
        """
        # Do this once stock feature is complete.

    @commands.hybrid_command(
        name="store",
        description="View the store",
        aliases=["shop"],
    )
    async def store(self, ctx: commands.Context) -> None:
        """Store command.

        Args:
            ctx (commands.Context): Context.
        """
        # Do later


async def setup(bot: DizznemBot) -> None:
    """Setup for money.

    Args:
        bot (commands.Bot): Dizznem Bot
    """
    await bot.add_cog(Money(bot))
