"""Money bot commands."""

from bot.bot import DizznemBot
from discord import Asset, Color, Embed, Member
from discord.ext import commands
from log import logger  # noqa: F401
from user import User
from utils.numbers import format_number


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


async def setup(bot: DizznemBot) -> None:
    """Setup for money.

    Args:
        bot (commands.Bot): Dizznem Bot
    """
    await bot.add_cog(Money(bot))
