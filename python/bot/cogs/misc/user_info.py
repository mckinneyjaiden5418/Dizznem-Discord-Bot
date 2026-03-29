"""User info bot commands."""

from bot.bot import DizznemBot
from discord import Color, Embed, Member
from discord.ext import commands
from log import logger  # noqa: F401
from user import User
from utils.misc.leaderboard import build_leaderboard_embed
from utils.misc.leaderboard_views import LeaderboardView
from utils.numbers import format_number


class UserInfo(commands.Cog):
    """User info bot commands."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initiate UserInfo.

        Args:
            bot (commands.Bot): Dizznem Bot.
        """
        self.bot: commands.Bot = bot

    @commands.hybrid_command(
        name="level",
        description="Get your level and related information",
        aliases=["lvl"],
    )
    async def level(self, ctx: commands.Context, member: Member | None = None) -> None:
        """Level command.

        Args:
            ctx (commands.Context): Context.
            member (Member | None): Member if mentioned.
        """
        user_id: int = member.id if member else ctx.author.id
        username: str = member.name if member else ctx.author.name
        display_name: str = member.display_name if member else ctx.author.display_name
        avatar_url: str = member.display_avatar.url if member else ctx.author.display_avatar.url
        user: User = User.create_if_not_exists(user_id=user_id, username=username)

        level: int = user.level
        message_count: int = user.message_count
        required_messages: float = 2 * (level**2) + (50 * level) + 100

        progress_percent: float = min(message_count / required_messages, 1)
        progress_bar_length: int = 20
        filled_blocks: int = int(progress_percent * progress_bar_length)
        empty_blocks: int = progress_bar_length - filled_blocks
        progress_bar: str = "█" * filled_blocks + "░" * empty_blocks

        embed: Embed = Embed(
            title=f"{display_name}'s Level Stats",
            color=Color.og_blurple(),
        )
        embed.set_thumbnail(
            url=avatar_url,
        )
        embed.add_field(
            name="📈 Level",
            value=f"**{format_number(number=level)}**",
            inline=True,
        )
        embed.add_field(
            name="💬 Messages",
            value=f"**{format_number(number=message_count)}**",
            inline=True,
        )
        embed.add_field(
            name="🚀 Messages Required for Next Level",
            value=f"**{format_number(number=required_messages)}**",
            inline=False,
        )
        embed.add_field(
            name="🔹 Progress",
            value=f"{progress_bar} **{int(progress_percent * 100)}%**",
            inline=False,
        )
        embed.set_footer(text=f"User ID: {user_id}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="profile",
        description="Get your profile",
    )
    async def profile(self, ctx: commands.Context, member: Member | None = None) -> None:
        """Profile command.

        Args:
            ctx (commands.Context): Context.
            member (Member | None): Member if mentioned.
        """

    @commands.hybrid_command(
        name="leaderboard",
        description="View various user leaderboards",
        aliases=["lb"],
    )
    async def leaderboard(self, ctx: commands.Context) -> None:
        """Leaderboard command.

        Args:
            ctx (commands.Context): Context.
        """
        embed: Embed = build_leaderboard_embed("balance")
        view: LeaderboardView = LeaderboardView()
        view.message = await ctx.send(embed=embed, view=view)


async def setup(bot: DizznemBot) -> None:
    """Setup for UserInfo.

    Args:
        bot (commands.Bot): Dizznem Bot
    """
    await bot.add_cog(UserInfo(bot))
