"""Leaderboard view."""

from discord import Embed, Interaction, Message, SelectOption
from discord.ui import View, select
from utils.misc.leaderboard import build_leaderboard_embed


class LeaderboardView(View):
    """View for switching between leaderboard categories."""

    def __init__(self) -> None:
        """Initialize the leaderboard view."""
        super().__init__(timeout=120)
        self.message: Message | None = None

    async def on_timeout(self) -> None:
        """Disable select on timeout."""
        for item in self.children:
            item.disabled = True  # type: ignore[union-attr]
        if self.message:
            await self.message.edit(view=self)

    @select(
        placeholder="Select a category...",
        options=[
            SelectOption(label="Balance", value="balance", emoji="💰", default=True),
            SelectOption(label="Net Worth", value="networth", emoji="📊"),
            SelectOption(label="Prestige", value="prestige", emoji="⭐"),
        ],
    )
    async def select_category(self, interaction: Interaction, select: select) -> None:
        """Handle category selection.

        Args:
            interaction (Interaction): The interaction.
            select (select): The select menu.
        """
        category: str = select.values[0]

        for option in select.options:
            option.default = option.value == category

        embed: Embed = build_leaderboard_embed(category)
        await interaction.response.edit_message(embed=embed, view=self)
