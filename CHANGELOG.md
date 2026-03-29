# Dizznem Bot Changelog

## [2.0.0] - 2025-3-29
### Added
- Whole new/refactored backend!
- Dizznem Bot now has a YouTube feature!
    - $play "video title" to play a video
    - Alternatively, you can do $play (video link)
    - $skip to skip a video.
    - $pause to pause a video.
    - $resume to resume a paused video.
    - $stop stops the playback, clears the queue, and disconnects.
    - $queue shows the queue.
    - $nowplaying shows what is currently playing.
    - See notes section in changelog for more information about this feature.
- New response commands.
- There was another big feature I had 95% complete but apparently I have to wait over a week to get it approved so that's coming in a later update.
- Some other things that I just don't feel like typing out go figure it out yourself.

### Changed
- All output replaced with embeds with small exceptions such as AI responses.
- New XP formula.
- The way some cooldowns work.
- $give/transfer maximum transfer amount increased to $5,000,000.
- $weekly now gives you a random amount of money and has been nerfed, but scales with prestige now.
- Stock market overhaul
    - Stocks now point to real life stocks (no more +200% days for Subaru sorry).
        - If you find out what stock each stock is associated with I'll give you a reward.
    - You can only buy whole shares, might change in the future, currently undecided.
    - To buy/sell stocks do $buystock {stock_name} or $sellstock {stock_name}.
    - I'll be able to add more stocks in the future very easily due to this overhaul, so yay!
    - Some other changes I don't feel like typing out just check it out, the rest is self explanatory.
- Dizznem Bot AI slight changes to personality.
- $profile & $level show more information.
- All leaderboard commands condensed to just $leaderboard with a dropdown option to see different leaderboards.
- $store has a more GUI like approach.

### Fixed
- Possible sources of data loss.

### Removed
- All data reset except for...
    - Level related data.
    - $inspiration database.
    - $count database.
- Marvel Rivals tracker ($tracker).
    - May get re-added in the future -- would've delayed release.
- Register command ($register).
    - Not needed anymore.

### Notes
- Your level will start at 1. If you had a lot of messages on Dizznem Bot 1.0.0, you may level up rapidly for a bit until the bot syncs you to the correct level.
- User data that was not reset dates back to 11/21/25.
- YouTube feature will likely have quite a few bugs due to limited testing. Report any bugs to me and I'll work on fixing them.
- YouTube feature will get more refined in a future update (such as vote skipping), I just wanted to get the feature out for 2.0.0.
- YouTube feature probably has a bug where it'll stop playing something randomly, but I wanted to get this out today so I'll fix this later haha.

## [1.0.0] - 2025-3-30
### Added
- Original Dizznem Bot release!