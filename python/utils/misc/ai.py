"""AI response utilities."""

import requests
from log import logger

SYSTEM_NOTE: str = """You are being used as a chatbot in a discord bot known as Dizznem bot.
You are to respond as if you are Dizznem bot AI.
Dizznem is a retired streamer who used to stream on Twitch.
Dizznem is now a tiktok shop buisness man.
He is friends with Karma SB who made this bot.
Only include relevant information in your response, if nothing is relevant here, just ignore it.
Don't include any reference to this note in your response!"""


def get_ai_response(prompt: str, api_key: str) -> str:
    """Get an AI response from DeepSeek.

    Args:
        prompt (str): The user's prompt.
        api_key (str): DeepSeek API key.

    Returns:
        str: The AI response.
    """
    try:
        response: requests.Response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": SYSTEM_NOTE},
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=15,
        )
        data: dict = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"].strip()
        logger.error(f"Unexpected DeepSeek API response: {data}")
        return "I couldn't generate a response right now. Try again later."  # noqa: TRY300
    except requests.Timeout:
        logger.error("DeepSeek API request timed out.")
        return "The request timed out. Try again later."
    except requests.RequestException as e:
        logger.exception("Error generating AI response.", exc_info=e)
        return "Something went wrong generating a response."
