"""General util."""
from discord.ext import commands


def reset_cd(ctx: commands.Context) -> None:
    """Reset command cooldown.

    Args:
        ctx (commands.Context): Context.
    """
    if ctx.command is not None:
        ctx.command.reset_cooldown(ctx)