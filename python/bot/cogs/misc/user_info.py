"""User info bot commands."""

from bot.bot import DizznemBot
from discord import Color, Embed, Member
from discord.ext import commands
from log import logger  # noqa: F401
from user import User
from utils.misc.leaderboard import (
    USERS_DB_PATH,
    build_leaderboard_embed,
    get_all_ranks,
    get_level_rank,
)
from utils.misc.leaderboard_views import LeaderboardView
from utils.numbers import format_number, get_net_worth


class UserInfo(commands.Cog):
    """User info bot commands."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initiate UserInfo.

        Args:
            bot (commands.Bot): Dizznem Bot.
        """
        self.bot: commands.Bot = bot

    def messages_for_level(self, level: int) -> float:
        """Total messages required to reach a given level.

        Args:
            level (int): Level to calculate messages for.

        Returns:
            float: Total messages required to reach the level.
        """
        return 2 * (level**2) + (50 * level) + 100

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
        avatar_url: str = (
            member.display_avatar.url if member else ctx.author.display_avatar.url
        )
        user: User = User.create_if_not_exists(user_id=user_id, username=username)

        level: int = user.level
        message_count: int = user.message_count
        level_rank: int | None = get_level_rank(USERS_DB_PATH, user_id)
        rank_display: str = f"**#{level_rank}**" if level_rank else "**Unranked**"

        total_for_current: float = self.messages_for_level(level - 1)
        total_for_next: float = self.messages_for_level(level)
        messages_into_level: float = message_count - total_for_current
        messages_needed_this_level: float = total_for_next - total_for_current

        progress_percent: float = min(
            messages_into_level / messages_needed_this_level,
            1.0,
        )
        progress_bar_length: int = 20
        filled_blocks: int = int(progress_percent * progress_bar_length)
        empty_blocks: int = progress_bar_length - filled_blocks
        progress_bar: str = "█" * filled_blocks + "░" * empty_blocks

        embed: Embed = Embed(
            title=f"{display_name}'s Level Stats",
            color=Color.og_blurple(),
        )
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(
            name="📈 Level",
            value=f"**{format_number(number=level)}**",
            inline=True,
        )
        embed.add_field(
            name="🏆 Server Rank",
            value=rank_display,
            inline=True,
        )
        embed.add_field(
            name="💬 Messages",
            value=f"**{format_number(number=message_count)}**",
            inline=True,
        )
        embed.add_field(
            name="🚀 Progress to Next Level",
            value=(
                f"**{format_number(number=messages_into_level)}**"
                f" / **{format_number(number=messages_needed_this_level)}** messages"
            ),
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
    async def profile(
        self,
        ctx: commands.Context,
        member: Member | None = None,
    ) -> None:
        """Profile command.

        Args:
            ctx (commands.Context): Context.
            member (Member | None): Member if mentioned.
        """
        user_id: int = member.id if member else ctx.author.id
        username: str = member.name if member else ctx.author.name
        display_name: str = member.display_name if member else ctx.author.display_name
        avatar_url: str = (
            member.display_avatar.url if member else ctx.author.display_avatar.url
        )

        user: User = User.create_if_not_exists(user_id=user_id, username=username)

        level: int = user.level
        message_count: int = user.message_count

        total_for_current: float = self.messages_for_level(level - 1)
        total_for_next: float = self.messages_for_level(level)
        messages_into_level: float = message_count - total_for_current
        messages_needed_this_level: float = total_for_next - total_for_current

        progress_percent: float = min(
            messages_into_level / messages_needed_this_level, 1.0,
        )
        progress_bar_length: int = 20
        filled_blocks: int = int(progress_percent * progress_bar_length)
        progress_bar: str = "█" * filled_blocks + "░" * (
            progress_bar_length - filled_blocks
        )

        balance: float = user.money
        total_networth: float = get_net_worth(user=user, db_path=USERS_DB_PATH)
        stock_value: float = total_networth - balance

        ranks: dict[str, int | None] = get_all_ranks(USERS_DB_PATH, user_id)

        def fmt_rank(rank: int | None) -> str:
            return f"#{rank}" if rank else "Unranked"

        embed: Embed = Embed(
            color=Color.og_blurple(),
        )
        embed.set_author(name=f"{display_name}'s Profile", icon_url=avatar_url)
        embed.set_thumbnail(url=avatar_url)

        embed.add_field(name="👤 Username", value=f"**{username}**", inline=True)
        embed.add_field(
            name="⭐ Prestige",
            value=f"**{format_number(user.prestige)}**",
            inline=True,
        )
        embed.add_field(
            name="📈 Level",
            value=f"**{format_number(level)}**",
            inline=True,
        )
        embed.add_field(
            name="💬 Messages",
            value=f"**{format_number(message_count)}**",
            inline=True,
        )
        embed.add_field(
            name="🚀 Next Level In",
            value=f"**{format_number(messages_needed_this_level - messages_into_level)} messages**",
            inline=True,
        )
        embed.add_field(
            name="🔹 Progress",
            value=f"{progress_bar} **{int(progress_percent * 100)}%**",
            inline=False,
        )
        embed.add_field(
            name="💰 Balance",
            value=f"**${format_number(balance)}**",
            inline=True,
        )
        embed.add_field(
            name="📈 Stock Value",
            value=f"**${format_number(stock_value)}**",
            inline=True,
        )
        embed.add_field(
            name="📊 Net Worth",
            value=f"**${format_number(total_networth)}**",
            inline=True,
        )
        embed.add_field(
            name="🏆 Server Rankings",
            value=(
                f"💰 Balance: **{fmt_rank(ranks['balance'])}**\n"
                f"📊 Net Worth: **{fmt_rank(ranks['networth'])}**\n"
                f"⭐ Prestige: **{fmt_rank(ranks['prestige'])}**\n"
                f"📈 Level: **{fmt_rank(ranks['level'])}**"
            ),
            inline=False,
        )
        embed.set_footer(text=f"User ID: {user_id}")
        await ctx.send(embed=embed)

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
