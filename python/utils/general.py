"""General util."""
import asyncio

from discord import Message
from discord.ext import commands


def reset_cd(ctx: commands.Context) -> None:
    """Reset command cooldown.

    Args:
        ctx (commands.Context): Context.
    """
    if ctx.command is not None:
        ctx.command.reset_cooldown(ctx)

async def get_user_answer(
    bot: commands.Bot,
    ctx: commands.Context,
    timeout: int = 15,
) -> str | None:
    """Wait for a user's message answer.

    Returns:
        str | None: User's message content or None if timed out.
    """
    def check(message: Message) -> bool:
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        msg: Message = await bot.wait_for("message", check=check, timeout=timeout)
        return msg.content  # noqa: TRY300
    except asyncio.TimeoutError:
        return None
