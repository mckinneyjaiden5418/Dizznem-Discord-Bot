# Dizznem Bot

A Discord bot for the Dizznem community built with discord.py. Features an economy system, stock market, YouTube playback, trivia, leaderboards, and more.

---

## Features

- **Economy** — Balance, daily/weekly rewards, gambling, transfers, net worth
- **Stock Market** — Buy and sell stocks tied to real-world tickers via Yahoo Finance
- **Store** — Spend your money on fun server actions and prestige
- **Trivia** — General trivia, ABA trivia, and Rogue Lineage trivia for money
- **YouTube** — Play YouTube audio in voice channels with a queue system
- **Leaderboards** — Rankings by balance, net worth, prestige, and level
- **Profile & Levels** — Track messages, level up, and view your server rank
- **Inspiration** — Daily inspirational quotes sent automatically at 8 PM EST
- **AI Chat** — Talk to Dizznem Bot AI powered by DeepSeek
- **Reddit** - Browse Reddit posts and user info (not done yet, about to be added)
- **More** - A lot more features that I don't feel like listing out

---

## Setup

### Requirements

- Python 3.12+
- FFmpeg (for YouTube audio)
- libopus (for Discord voice)

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/Dizznem-Discord-Bot.git
cd Dizznem-Discord-Bot
```

### 2. Install system dependencies

```bash
sudo apt-get update && sudo apt-get install ffmpeg libopus0 libopus-dev -y
```

If FFmpeg is unavailable via apt (e.g. on a dev container), use the static build:

```bash
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-armhf-static.tar.xz
tar xf ffmpeg-release-armhf-static.tar.xz
sudo mv ffmpeg-*-armhf-static/ffmpeg /usr/local/bin/ffmpeg
rm -rf ffmpeg-*
```

Use `arm64` instead of `armhf` for 64-bit Raspberry Pi OS, or `amd64` for x86.

### 3. Install Python dependencies

```bash
pip install -r python/requirements.txt --break-system-packages
```

### 4. Configure environment variables

Create a `.env` file inside the `python/` directory:

```bash
cd python
nano .env
```

Fill in the following:

```dotenv
DISCORD_BOT_TOKEN=        # Your Discord bot token
DISCORD_BOT_TAG=          # The trigger word for AI chat (e.g. dizznem)
TEST_CHANNEL_ID=          # Channel ID the bot sends a hello message to on startup
INSPIRATION_CHANNEL_ID=   # Channel ID for daily inspiration messages
QOTD_CHANNEL_ID=          # Channel ID for question of the day
ADMIN_ID=                 # Your Discord user ID for admin commands
AI_API_KEY=               # DeepSeek API key for AI chat feature
```

### 5. Run the bot

```bash
python3 main.py
```

---

## Commands

| Command | Description |
|---|---|
| `$help` | List all commands |
| `$balance` | View your balance |
| `$networth` | View your net worth including stocks |
| `$daily` | Claim your daily reward |
| `$weekly` | Claim your weekly reward |
| `$gamble <amount>` | Gamble your money |
| `$give <user> <amount>` | Transfer money to another user |
| `$store` | Open the store |
| `$trivia` | Answer a trivia question for money |
| `$aba` | Anime Battle Arena trivia |
| `$roguelineage` | Rogue Lineage trivia |
| `$stockmarket` | View all stocks and their prices |
| `$buystock <stock>` | Buy shares of a stock |
| `$sellstock <stock>` | Sell shares of a stock |
| `$stocks` | View your stock portfolio |
| `$play <query>` | Play a YouTube video in VC |
| `$skip` | Skip the current song |
| `$pause` | Pause playback |
| `$resume` | Resume playback |
| `$stop` | Stop playback and disconnect |
| `$queue` | View the song queue |
| `$nowplaying` | Show the current song |
| `$leaderboard` | View server leaderboards |
| `$level` | View your level stats |
| `$profile` | View your full profile |
| `$inspiration` | Get an inspirational quote |
| `$count` | Increment the server count |

---

## Environment Notes

- `DISCORD_BOT_TAG` is the word that triggers the AI chat (e.g. if set to `dizznem`, saying `dizznem what's up` in chat will get a response)
- The Reddit cog requires a Reddit API key — see [reddit.com/prefs/apps](https://reddit.com/prefs/apps) to set one up
- Stock prices update automatically when the US market opens each day via Yahoo Finance
- The AI feature uses the [DeepSeek API](https://platform.deepseek.com)

---

## Made by Karma SB
