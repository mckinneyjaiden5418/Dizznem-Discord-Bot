"""YouTube voice channel commands."""

import asyncio
from collections import deque
from typing import TYPE_CHECKING

import yt_dlp
from bot.bot import DizznemBot
from discord import (
    Color,
    Embed,
    FFmpegPCMAudio,
    Member,
    PCMVolumeTransformer,
    StageChannel,
    VoiceChannel,
    VoiceClient,
)
from discord.ext import commands, tasks
from log import logger

if TYPE_CHECKING:
    from yt_dlp.extractor.common import _InfoDict

YDL_OPTIONS: dict = {
    "format": "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "source_address": "0.0.0.0",  # noqa: S104
}

FFMPEG_OPTIONS: dict = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -reconnect_at_eof 1",  # noqa: E501
    "options": "-vn -bufsize 64k",
}

AUTO_DISCONNECT_SECONDS: int = 300  # 5 minutes
MAX_QUEUE_DISPLAY: int = 10
MAX_EMBED_FIELD_LENGTH: int = 1000
MAX_TITLE_LENGTH: int = 50


class YouTube(commands.Cog):
    """YouTube voice channel commands."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initialize the cog.

        Args:
            bot (DizznemBot): Dizznem Bot.
        """
        self.bot: DizznemBot = bot
        self.queue: deque[dict] = deque()
        self.current: dict | None = None
        self.voice_client: VoiceClient | None = None
        self._idle_time: int = 0
        self._auto_disconnect.start()

    def cog_unload(self) -> None:
        """Stop background tasks on unload."""
        self._auto_disconnect.cancel()

    async def _fetch_info(self, query: str) -> dict | None:
        """Fetch video info from YouTube.

        Args:
            query (str): Search query or URL.

        Returns:
            dict | None: Video info dict, or None if not found.
        """
        is_url: bool = query.startswith(("http://", "https://"))

        def _extract() -> dict | None:
            with yt_dlp.YoutubeDL(
                YDL_OPTIONS,  # pyright: ignore[reportArgumentType]
            ) as ydl:
                try:
                    search_query: str = query if is_url else f"ytsearch:{query}"
                    info: _InfoDict = ydl.extract_info(search_query, download=False)
                    if is_url:
                        return info  # pyright: ignore[reportReturnType]
                    if info and "entries" in info and info["entries"]:
                        return info["entries"][0]
                    return None  # noqa: TRY300
                except (
                    yt_dlp.utils.DownloadError  # pyright: ignore[reportAttributeAccessIssue]
                ) as e:
                    logger.error(f"yt-dlp error: {e}")
                    return None

        return await asyncio.to_thread(_extract)

    def _get_audio_url(self, info: dict) -> str | None:
        """Extract the best audio URL from video info.

        Args:
            info (dict): Video info dict from yt-dlp.

        Returns:
            str | None: Direct audio stream URL.
        """
        formats: list = info.get("formats", [])
        audio_formats: list[dict] = [
            f
            for f in formats
            if f.get("acodec") != "none" and f.get("vcodec") == "none"
        ]
        if audio_formats:
            return audio_formats[-1]["url"]
        return info.get("url")

    def _play_next(self, ctx: commands.Context) -> None:
        """Play the next song in the queue, fetching a fresh URL before playing.

        Args:
            ctx (commands.Context): Context.
        """
        if not self.queue or not self.voice_client:
            self.current = None
            return

        self.current = self.queue.popleft()

        async def _start_playing() -> None:
            """Fetch fresh URL and start playback."""
            if self.current is None:
                return

            fresh_info: dict | None = await self._fetch_info(
                self.current["webpage_url"],
            )
            if fresh_info is None:
                logger.error(f"Failed to re-fetch info for {self.current['title']}")
                await self._send_next_playing(ctx)
                return

            audio_url: str | None = self._get_audio_url(fresh_info)
            if audio_url is None or not self.voice_client:
                self.current = None
                return

            source: PCMVolumeTransformer[FFmpegPCMAudio] = PCMVolumeTransformer(
                FFmpegPCMAudio(
                    audio_url,
                    **FFMPEG_OPTIONS,
                ),
                volume=0.5,
            )

            def after_playing(error: Exception | None) -> None:
                if error:
                    logger.error(f"Audio playback error: {error}")
                asyncio.run_coroutine_threadsafe(
                    self._send_next_playing(ctx),
                    self.bot.loop,
                )

            self.voice_client.play(source, after=after_playing)

        asyncio.run_coroutine_threadsafe(_start_playing(), self.bot.loop)

    async def _send_next_playing(self, ctx: commands.Context) -> None:
        """Send now playing message and advance queue.

        Args:
            ctx (commands.Context): Context.
        """
        self._play_next(ctx)
        if self.current:
            embed = Embed(
                title="🎵 Now Playing",
                color=Color.red(),
                description=f"**[{self.current['title']}]({self.current['webpage_url']})**",
            )
            embed.set_thumbnail(url=self.current.get("thumbnail"))
            embed.add_field(
                name="Duration",
                value=_format_duration(self.current.get("duration", 0)),
                inline=True,
            )
            await ctx.send(embed=embed)

    @tasks.loop(seconds=30)
    async def _auto_disconnect(self) -> None:
        """Disconnect from VC if nothing has been playing for a while."""
        if self.voice_client is None or not self.voice_client.is_connected():
            self._idle_time = 0
            return

        if self.voice_client.is_playing() or self.voice_client.is_paused():
            self._idle_time = 0
            return

        self._idle_time += 30
        if self._idle_time >= AUTO_DISCONNECT_SECONDS:
            self.queue.clear()
            self.current = None
            await self.voice_client.disconnect()
            self.voice_client = None
            self._idle_time = 0
            logger.info("Auto-disconnected from VC due to inactivity.")

    @_auto_disconnect.before_loop
    async def before_auto_disconnect(self) -> None:
        """Wait until bot is ready before starting the loop."""
        await self.bot.wait_until_ready()

    @commands.hybrid_command(name="play", description="Play a YouTube video in VC")
    async def play(self, ctx: commands.Context, *, query: str) -> None:
        """Play a YouTube video by title or URL.

        Args:
            ctx (commands.Context): Context.
            query (str): Video title or URL to search for.
        """
        if not isinstance(ctx.author, Member) or ctx.author.voice is None:
            await ctx.send(
                embed=Embed(
                    title="❌ Not in VC",
                    color=Color.red(),
                    description="You need to be in a voice channel to use this command.",
                ),
                ephemeral=True,
            )
            return

        await ctx.defer()

        info: dict | None = await self._fetch_info(query)
        if info is None:
            await ctx.send(
                embed=Embed(
                    title="❌ Not Found",
                    color=Color.red(),
                    description=f"Could not find a video for **{query}**.",
                ),
            )
            return

        voice_channel: VoiceChannel | StageChannel | None = ctx.author.voice.channel
        if self.voice_client is None or not self.voice_client.is_connected():
            self.voice_client = (
                await voice_channel.connect()  # pyright: ignore[reportOptionalMemberAccess]
            )
        elif self.voice_client.channel != voice_channel:
            await self.voice_client.move_to(voice_channel)

        self.queue.append(info)

        if not self.voice_client.is_playing() and not self.voice_client.is_paused():
            self._play_next(ctx)
            embed = Embed(
                title="🎵 Now Playing",
                color=Color.red(),
                description=f"**[{info['title']}]({info['webpage_url']})**",
            )
        else:
            embed = Embed(
                title="➕ Added to Queue",  # noqa: RUF001
                color=Color.og_blurple(),
                description=f"**[{info['title']}]({info['webpage_url']})**",
            )
            embed.add_field(
                name="Position",
                value=f"**#{len(self.queue)}** in queue",
                inline=True,
            )

        embed.set_thumbnail(url=info.get("thumbnail"))
        embed.add_field(
            name="Duration",
            value=_format_duration(info.get("duration", 0)),
            inline=True,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="skip", description="Skip the current song")
    async def skip(self, ctx: commands.Context) -> None:
        """Skip the current song.

        Args:
            ctx (commands.Context): Context.
        """
        if self.voice_client is None or not self.voice_client.is_playing():
            await ctx.send(
                embed=Embed(
                    title="❌ Nothing Playing",
                    color=Color.red(),
                    description="There is nothing currently playing.",
                ),
                ephemeral=True,
            )
            return

        self.voice_client.stop()
        await ctx.send(
            embed=Embed(
                title="⏭️ Skipped",
                color=Color.og_blurple(),
                description="Skipped the current song.",
            ),
        )

    @commands.hybrid_command(name="pause", description="Pause the current song")
    async def pause(self, ctx: commands.Context) -> None:
        """Pause the current song.

        Args:
            ctx (commands.Context): Context.
        """
        if self.voice_client is None or not self.voice_client.is_playing():
            await ctx.send(
                embed=Embed(
                    title="❌ Nothing Playing",
                    color=Color.red(),
                    description="There is nothing currently playing.",
                ),
                ephemeral=True,
            )
            return

        self.voice_client.pause()
        await ctx.send(
            embed=Embed(
                title="⏸️ Paused",
                color=Color.og_blurple(),
                description="Paused the current song.",
            ),
        )

    @commands.hybrid_command(name="resume", description="Resume the current song")
    async def resume(self, ctx: commands.Context) -> None:
        """Resume the current song.

        Args:
            ctx (commands.Context): Context.
        """
        if self.voice_client is None or not self.voice_client.is_paused():
            await ctx.send(
                embed=Embed(
                    title="❌ Nothing Paused",
                    color=Color.red(),
                    description="There is nothing currently paused.",
                ),
                ephemeral=True,
            )
            return

        self.voice_client.resume()
        await ctx.send(
            embed=Embed(
                title="▶️ Resumed",
                color=Color.og_blurple(),
                description="Resumed the current song.",
            ),
        )

    @commands.hybrid_command(
        name="stop",
        description="Stop playback and clear the queue",
    )
    async def stop(self, ctx: commands.Context) -> None:
        """Stop playback, clear the queue and disconnect.

        Args:
            ctx (commands.Context): Context.
        """
        self.queue.clear()
        self.current = None
        self._idle_time = 0
        if self.voice_client:
            await self.voice_client.disconnect()
            self.voice_client = None

        await ctx.send(
            embed=Embed(
                title="⏹️ Stopped",
                color=Color.og_blurple(),
                description="Stopped playback and cleared the queue.",
            ),
        )

    @commands.hybrid_command(name="queue", description="View the current song queue")
    async def queue_cmd(self, ctx: commands.Context) -> None:
        """Show the current queue.

        Args:
            ctx (commands.Context): Context.
        """
        if not self.current and not self.queue:
            await ctx.send(
                embed=Embed(
                    title="📋 Queue",
                    color=Color.og_blurple(),
                    description="The queue is empty.",
                ),
            )
            return

        embed = Embed(title="📋 Queue", color=Color.og_blurple())

        if self.current:
            title: str = self.current["title"]
            if len(title) > MAX_TITLE_LENGTH:
                title = title[: MAX_TITLE_LENGTH - 3] + "..."
            embed.add_field(
                name="🎵 Now Playing",
                value=f"**[{title}]({self.current['webpage_url']})**",
                inline=False,
            )

        if self.queue:
            queue_lines: list[str] = []
            total_length: int = 0
            for i, item in enumerate(self.queue):
                if i >= MAX_QUEUE_DISPLAY:
                    break
                title = item["title"]
                if len(title) > MAX_TITLE_LENGTH:
                    title = title[: MAX_TITLE_LENGTH - 3] + "..."
                line: str = f"`{i + 1}.` **[{title}]({item['webpage_url']})**"
                total_length += len(line) + 1  # +1 for newline
                if total_length > MAX_EMBED_FIELD_LENGTH:
                    queue_lines.append("*...and more*")
                    break
                queue_lines.append(line)

            embed.add_field(
                name="Up Next",
                value="\n".join(queue_lines),
                inline=False,
            )
            if len(self.queue) > MAX_QUEUE_DISPLAY:
                embed.set_footer(
                    text=f"...and {len(self.queue) - MAX_QUEUE_DISPLAY} more",
                )

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="nowplaying", description="Show the current song")
    async def nowplaying(self, ctx: commands.Context) -> None:
        """Show the currently playing song.

        Args:
            ctx (commands.Context): Context.
        """
        if not self.current:
            await ctx.send(
                embed=Embed(
                    title="❌ Nothing Playing",
                    color=Color.red(),
                    description="Nothing is currently playing.",
                ),
                ephemeral=True,
            )
            return

        embed = Embed(
            title="🎵 Now Playing",
            color=Color.red(),
            description=f"**[{self.current['title']}]({self.current['webpage_url']})**",
        )
        embed.set_thumbnail(url=self.current.get("thumbnail"))
        embed.add_field(
            name="Duration",
            value=_format_duration(self.current.get("duration", 0)),
            inline=True,
        )
        embed.add_field(
            name="Queue Length",
            value=f"**{len(self.queue)}** song(s) remaining",
            inline=True,
        )
        await ctx.send(embed=embed)


def _format_duration(seconds: int) -> str:
    """Format seconds into mm:ss or hh:mm:ss.

    Args:
        seconds (int): Duration in seconds.

    Returns:
        str: Formatted duration string.
    """
    seconds = int(seconds)
    hours: int
    remainder: int
    minutes: int
    secs: int
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02}:{secs:02}"
    return f"{minutes}:{secs:02}"


async def setup(bot: DizznemBot) -> None:
    """Load the cog.

    Args:
        bot (DizznemBot): Dizznem Bot.
    """
    await bot.add_cog(YouTube(bot))
