"""Roblox util."""

import random
from pathlib import Path


def question(game: str) -> tuple[Path, str, str]:
    """Get question.

    Args:
        game (str): ABA or Rogue Lineage

    Returns:
        tuple[Path, str, str]: Image path, question, and answer.
    """
    if game == "rogue":
        categories: list[str] = ["race", "artifact", "creature"]
        category: str = random.choice(categories)  # noqa: S311
        questions: dict[str, str] = {
            "race": "What race is this?",
            "artifact": "What artifact is this?",
            "creature": "What creature is this?",
        }
        question: str = questions[category]
    elif game == "aba":
        category = "character"
        question = "What character is this?"

    category_path: Path = (
        Path(__file__).parent.parent.parent.parent / "data" / "images" / category
    )
    files: list[Path] = list(category_path.iterdir())
    image_path: Path = random.choice(files)  # noqa: S311
    answer: str = image_path.stem

    return image_path, question, answer


def check_answer(answer: str, user_answer: str) -> bool:
    """Check if answer was right.

    Args:
        answer (str): Correct answer.
        user_answer (str): User's answer.

    Returns:
        bool: True if user answered correctly.
    """
    user_answer = nicknames(user_answer)
    user_answer.lower().strip()
    return answer == user_answer


def nicknames(name: str) -> str:
    """Get nickname if nickname was used.

    Args:
        name (str): Possible nickname.

    Returns:
        str: Nickname changed to correct answer if applicable.
    """
    nicknames: dict[str, str] = {
        "fisch": "fischeran",
        "metal scroom": "metascroom",
        "mscroom": "metascroom",
        "pd": "phoenix down",
        "wka": "white kings amulet",
        "ff": "fairfrozen",
        "philo": "philosophers stone",
        "philosopher's stone": "philosophers stone",
        "lannis": "lannis amulet",
        "sc": "spider cloak",
        "z scroom": "zombie scroom",
        "redacted": "evil eye",
        "mori": "mori turret",
        "sigil shrieker": "sealed shrieker",
        "sigil shriekers": "sealed shrieker",
        "lava serpent": "lava snake",
        "tundra dragon": "ice dragon",
        "mscroom key": "metascroom key",
        "cons": "construct",
        "insanity monster": "satanic manipulation",
    }
    return nicknames.get(name.lower(), name)
