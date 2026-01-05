"""Admin commands.

Quick note:
I'm using discord IDs here to check for admin because I don't have admin in the discord server this
bot is being used.

"""

from bot.bot import DizznemBot
from discord import Color, Embed, Member
from discord.ext import commands
from log import logger  # noqa: F401
from user import User
from utils.numbers import convert_money_str


class Admin(commands.Cog):
    """Admin commands."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initialize Admin.

        Args:
            bot (DizznemBot): Dizznem Bot.
        """
        self.bot: DizznemBot = bot

    @commands.hybrid_command(
        name="setmoney", description="Set money for a user (admin command).",
    )
    async def set_money(
        self, ctx: commands.Context, member: Member, amount: str,
    ) -> None:
        """Set money for a user.

        Args:
            ctx (commands.Context): Context.
            member (Member): Member to set money for.
            amount (str): Money amount.
        """
        if ctx.author.id != self.bot.admin_id:
            embed: Embed = Embed(
                title="Error",
                color=Color.red(),
                description="You do not have access to this command.",
            )
            await ctx.send(embed=embed)
            return

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

        user: User = User.create_if_not_exists(user_id=member.id, username=member.name)
        user.money = amount_float

        embed: Embed = Embed(
            title="Placeholder",
            color=Color.green(),
            description=f"Added {amount_float}.",
        )

        await ctx.send(embed=embed)


async def setup(bot: DizznemBot) -> None:
    """Setup for Admin.

    Args:
        bot (DizznemBot): Dizznem Bot.
    """
    await bot.add_cog(Admin(bot))
