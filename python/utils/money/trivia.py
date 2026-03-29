"""Trivia utilities."""

import random

from discord import Color, Embed

TRIVIA_LIST: list[dict] = [
    # First 25 questions with answer choice 'a'
    {
        "question": "What is the capital of France?",
        "choices": ["Paris", "London", "Berlin", "Madrid"],
        "answer": "a",
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "choices": ["Mars", "Venus", "Jupiter", "Saturn"],
        "answer": "a",
    },
    {
        "question": "What is the largest ocean on Earth?",
        "choices": ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"],
        "answer": "a",
    },
    {
        "question": "Who wrote 'To Kill a Mockingbird'?",
        "choices": [
            "Harper Lee",
            "Mark Twain",
            "Ernest Hemingway",
            "F. Scott Fitzgerald",
        ],
        "answer": "a",
    },
    {
        "question": "What is the smallest prime number?",
        "choices": ["2", "3", "5", "7"],
        "answer": "a",
    },
    {
        "question": "What is the chemical symbol for gold?",
        "choices": ["Au", "Ag", "Pb", "Fe"],
        "answer": "a",
    },
    {
        "question": "Which country is known as the Land of the Rising Sun?",
        "choices": ["Japan", "China", "Thailand", "India"],
        "answer": "a",
    },
    {
        "question": "What is the hardest natural substance on Earth?",
        "choices": ["Diamond", "Gold", "Iron", "Platinum"],
        "answer": "a",
    },
    {
        "question": "Who painted the Mona Lisa?",
        "choices": [
            "Leonardo da Vinci",
            "Vincent van Gogh",
            "Pablo Picasso",
            "Claude Monet",
        ],
        "answer": "a",
    },
    {
        "question": "What is the largest planet in our solar system?",
        "choices": ["Jupiter", "Saturn", "Uranus", "Neptune"],
        "answer": "a",
    },
    {
        "question": "What is the capital of Italy?",
        "choices": ["Rome", "Paris", "Berlin", "Madrid"],
        "answer": "a",
    },
    {
        "question": "Which element has the atomic number 1?",
        "choices": ["Hydrogen", "Helium", "Lithium", "Beryllium"],
        "answer": "a",
    },
    {
        "question": "What is the tallest mountain in the world?",
        "choices": ["Mount Everest", "K2", "Kangchenjunga", "Lhotse"],
        "answer": "a",
    },
    {
        "question": "Who is the author of '1984'?",
        "choices": ["George Orwell", "Aldous Huxley", "Ray Bradbury", "Jules Verne"],
        "answer": "a",
    },
    {
        "question": "What is the largest mammal in the world?",
        "choices": ["Blue Whale", "Elephant", "Giraffe", "Hippopotamus"],
        "answer": "a",
    },
    {
        "question": "What is the capital of Spain?",
        "choices": ["Madrid", "Barcelona", "Seville", "Valencia"],
        "answer": "a",
    },
    {
        "question": "Which planet is closest to the sun?",
        "choices": ["Mercury", "Venus", "Earth", "Mars"],
        "answer": "a",
    },
    {
        "question": "What is the longest river in the world?",
        "choices": ["Nile", "Amazon", "Yangtze", "Mississippi"],
        "answer": "a",
    },
    {
        "question": "Who discovered penicillin?",
        "choices": [
            "Alexander Fleming",
            "Marie Curie",
            "Louis Pasteur",
            "Isaac Newton",
        ],
        "answer": "a",
    },
    {
        "question": "What is the capital of Germany?",
        "choices": ["Berlin", "Munich", "Frankfurt", "Hamburg"],
        "answer": "a",
    },
    {
        "question": "What is the largest desert in the world?",
        "choices": ["Sahara", "Gobi", "Kalahari", "Arctic"],
        "answer": "a",
    },
    {
        "question": "Who wrote 'Pride and Prejudice'?",
        "choices": ["Jane Austen", "Charlotte Bronte", "Emily Bronte", "Mary Shelley"],
        "answer": "a",
    },
    {
        "question": "What is the chemical symbol for water?",
        "choices": ["H2O", "CO2", "O2", "N2"],
        "answer": "a",
    },
    {
        "question": "Which country is known for the maple leaf?",
        "choices": ["Canada", "USA", "UK", "Australia"],
        "answer": "a",
    },
    {
        "question": "What is the capital of Canada?",
        "choices": ["Ottawa", "Toronto", "Vancouver", "Montreal"],
        "answer": "a",
    },
    # Next 25 questions with answer choice 'b'
    {
        "question": "What is the capital of Australia?",
        "choices": ["Sydney", "Canberra", "Melbourne", "Brisbane"],
        "answer": "b",
    },
    {
        "question": "Which planet is known as the Earth's twin?",
        "choices": ["Mars", "Venus", "Jupiter", "Saturn"],
        "answer": "b",
    },
    {
        "question": "What is the smallest continent?",
        "choices": ["Europe", "Australia", "Antarctica", "South America"],
        "answer": "b",
    },
    {
        "question": "Who wrote 'The Great Gatsby'?",
        "choices": [
            "Ernest Hemingway",
            "F. Scott Fitzgerald",
            "Mark Twain",
            "John Steinbeck",
        ],
        "answer": "b",
    },
    {
        "question": "What is the largest bone in the human body?",
        "choices": ["Tibia", "Femur", "Humerus", "Radius"],
        "answer": "b",
    },
    {
        "question": "What is the chemical symbol for silver?",
        "choices": ["Au", "Ag", "Pb", "Fe"],
        "answer": "b",
    },
    {
        "question": "Which country is known as the Land of the Free?",
        "choices": ["Canada", "USA", "UK", "Australia"],
        "answer": "b",
    },
    {
        "question": "What is the softest mineral on Earth?",
        "choices": ["Diamond", "Talc", "Gold", "Iron"],
        "answer": "b",
    },
    {
        "question": "Who painted the Starry Night?",
        "choices": [
            "Leonardo da Vinci",
            "Vincent van Gogh",
            "Pablo Picasso",
            "Claude Monet",
        ],
        "answer": "b",
    },
    {
        "question": "What is the second largest planet in our solar system?",
        "choices": ["Jupiter", "Saturn", "Uranus", "Neptune"],
        "answer": "b",
    },
    {
        "question": "What is the capital of Greece?",
        "choices": ["Rome", "Athens", "Berlin", "Madrid"],
        "answer": "b",
    },
    {
        "question": "Which element has the atomic number 2?",
        "choices": ["Hydrogen", "Helium", "Lithium", "Beryllium"],
        "answer": "b",
    },
    {
        "question": "What is the second tallest mountain in the world?",
        "choices": ["Mount Everest", "K2", "Kangchenjunga", "Lhotse"],
        "answer": "b",
    },
    {
        "question": "Who is the author of 'Brave New World'?",
        "choices": ["George Orwell", "Aldous Huxley", "Ray Bradbury", "Jules Verne"],
        "answer": "b",
    },
    {
        "question": "What is the second largest mammal in the world?",
        "choices": ["Blue Whale", "Elephant", "Giraffe", "Hippopotamus"],
        "answer": "b",
    },
    {
        "question": "What is the capital of Portugal?",
        "choices": ["Madrid", "Lisbon", "Seville", "Valencia"],
        "answer": "b",
    },
    {
        "question": "Which planet is second closest to the sun?",
        "choices": ["Mercury", "Venus", "Earth", "Mars"],
        "answer": "b",
    },
    {
        "question": "What is the second longest river in the world?",
        "choices": ["Nile", "Amazon", "Yangtze", "Mississippi"],
        "answer": "b",
    },
    {
        "question": "Who discovered the theory of relativity?",
        "choices": [
            "Alexander Fleming",
            "Albert Einstein",
            "Louis Pasteur",
            "Isaac Newton",
        ],
        "answer": "b",
    },
    {
        "question": "What is the capital of Russia?",
        "choices": ["Berlin", "Moscow", "Frankfurt", "Hamburg"],
        "answer": "b",
    },
    {
        "question": "What is the second largest desert in the world?",
        "choices": ["Sahara", "Gobi", "Kalahari", "Arctic"],
        "answer": "b",
    },
    {
        "question": "Who wrote 'Wuthering Heights'?",
        "choices": ["Jane Austen", "Charlotte Bronte", "Emily Bronte", "Mary Shelley"],
        "answer": "b",
    },
    {
        "question": "What is the chemical symbol for carbon dioxide?",
        "choices": ["H2O", "CO2", "O2", "N2"],
        "answer": "b",
    },
    {
        "question": "Which country is known for the kangaroo?",
        "choices": ["Canada", "Australia", "UK", "USA"],
        "answer": "b",
    },
    {
        "question": "What is the capital of Brazil?",
        "choices": ["Ottawa", "Brasilia", "Vancouver", "Montreal"],
        "answer": "b",
    },
    # Next 25 questions with answer choice 'c'
    {
        "question": "What is the capital of Egypt?",
        "choices": ["Sydney", "Canberra", "Cairo", "Brisbane"],
        "answer": "c",
    },
    {
        "question": "Which planet is known as the Blue Planet?",
        "choices": ["Mars", "Venus", "Earth", "Saturn"],
        "answer": "c",
    },
    {
        "question": "What is the largest continent?",
        "choices": ["Europe", "Australia", "Asia", "South America"],
        "answer": "c",
    },
    {
        "question": "Who wrote 'Moby Dick'?",
        "choices": [
            "Ernest Hemingway",
            "F. Scott Fitzgerald",
            "Herman Melville",
            "John Steinbeck",
        ],
        "answer": "c",
    },
    {
        "question": "What is the smallest bone in the human body?",
        "choices": ["Femur", "Tibia", "Stapes", "Radius"],
        "answer": "c",
    },
    {
        "question": "What is the chemical symbol for lead?",
        "choices": ["Au", "Ag", "Pb", "Fe"],
        "answer": "c",
    },
    {
        "question": "Which country is known as the Land of the Midnight Sun?",
        "choices": ["Canada", "USA", "Norway", "Australia"],
        "answer": "c",
    },
    {
        "question": "What is the hardest mineral on Earth?",
        "choices": ["Gold", "Talc", "Diamond", "Iron"],
        "answer": "c",
    },
    {
        "question": "Who painted the Last Supper?",
        "choices": [
            "Leonardo da Vinci",
            "Vincent van Gogh",
            "Pablo Picasso",
            "Claude Monet",
        ],
        "answer": "c",
    },
    {
        "question": "What is the third largest planet in our solar system?",
        "choices": ["Jupiter", "Saturn", "Uranus", "Neptune"],
        "answer": "c",
    },
    {
        "question": "What is the capital of Turkey?",
        "choices": ["Rome", "Athens", "Ankara", "Madrid"],
        "answer": "c",
    },
    {
        "question": "Which element has the atomic number 3?",
        "choices": ["Hydrogen", "Helium", "Lithium", "Beryllium"],
        "answer": "c",
    },
    {
        "question": "What is the third tallest mountain in the world?",
        "choices": ["Mount Everest", "K2", "Kangchenjunga", "Lhotse"],
        "answer": "c",
    },
    {
        "question": "Who is the author of 'Fahrenheit 451'?",
        "choices": ["George Orwell", "Aldous Huxley", "Ray Bradbury", "Jules Verne"],
        "answer": "c",
    },
    {
        "question": "What is the third largest mammal in the world?",
        "choices": ["Blue Whale", "Elephant", "Giraffe", "Hippopotamus"],
        "answer": "c",
    },
    {
        "question": "What is the capital of Argentina?",
        "choices": ["Madrid", "Lisbon", "Buenos Aires", "Valencia"],
        "answer": "c",
    },
    {
        "question": "Which planet is third closest to the sun?",
        "choices": ["Mercury", "Venus", "Earth", "Mars"],
        "answer": "c",
    },
    {
        "question": "What is the third longest river in the world?",
        "choices": ["Nile", "Amazon", "Yangtze", "Mississippi"],
        "answer": "c",
    },
    {
        "question": "Who discovered gravity?",
        "choices": [
            "Alexander Fleming",
            "Albert Einstein",
            "Isaac Newton",
            "George Washington",
        ],
        "answer": "c",
    },
    {
        "question": "What is the capital of China?",
        "choices": ["Berlin", "Moscow", "Beijing", "Hamburg"],
        "answer": "c",
    },
    {
        "question": "What is the third largest desert in the world?",
        "choices": ["Sahara", "Gobi", "Kalahari", "Arctic"],
        "answer": "c",
    },
    {
        "question": "Who wrote 'Frankenstein'?",
        "choices": ["Jane Austen", "Charlotte Bronte", "Mary Shelley", "Emily Bronte"],
        "answer": "c",
    },
    {
        "question": "What is the chemical symbol for oxygen?",
        "choices": ["H2O", "CO2", "O2", "N2"],
        "answer": "c",
    },
    {
        "question": "Which country is known for the Eiffel Tower?",
        "choices": ["Canada", "USA", "France", "Australia"],
        "answer": "c",
    },
    {
        "question": "What is the capital of Mexico?",
        "choices": ["Ottawa", "Brasilia", "Mexico City", "Montreal"],
        "answer": "c",
    },
    # Final 25 questions with answer choice 'd'
    {
        "question": "What is the capital of India?",
        "choices": ["Sydney", "Canberra", "Cairo", "New Delhi"],
        "answer": "d",
    },
    {
        "question": "Which planet is known as the Ringed Planet?",
        "choices": ["Mars", "Venus", "Earth", "Saturn"],
        "answer": "d",
    },
    {
        "question": "What is the second smallest continent?",
        "choices": ["South America", "Australia", "Antarctica", "Europe"],
        "answer": "d",
    },
    {
        "question": "Who wrote 'The Catcher in the Rye'?",
        "choices": [
            "Ernest Hemingway",
            "F. Scott Fitzgerald",
            "Herman Melville",
            "J.D. Salinger",
        ],
        "answer": "d",
    },
    {
        "question": "What is the second smallest bone in the human body?",
        "choices": ["Femur", "Tibia", "Stapes", "Incus"],
        "answer": "d",
    },
    {
        "question": "What is the chemical symbol for iron?",
        "choices": ["Au", "Ag", "Pb", "Fe"],
        "answer": "d",
    },
    {
        "question": "Which country is known as the Land of Fire and Ice?",
        "choices": ["Canada", "USA", "Norway", "Iceland"],
        "answer": "d",
    },
    {
        "question": "What is the second hardest mineral on Earth?",
        "choices": ["Diamond", "Talc", "Gold", "Corundum"],
        "answer": "d",
    },
    {
        "question": "Who painted the Scream?",
        "choices": [
            "Leonardo da Vinci",
            "Vincent van Gogh",
            "Pablo Picasso",
            "Edvard Munch",
        ],
        "answer": "d",
    },
    {
        "question": "What is the fourth largest planet in our solar system?",
        "choices": ["Jupiter", "Saturn", "Uranus", "Neptune"],
        "answer": "d",
    },
    {
        "question": "What is the capital of Japan?",
        "choices": ["Rome", "Athens", "Ankara", "Tokyo"],
        "answer": "d",
    },
    {
        "question": "Which element has the atomic number 4?",
        "choices": ["Hydrogen", "Helium", "Lithium", "Beryllium"],
        "answer": "d",
    },
    {
        "question": "What is the fourth tallest mountain in the world?",
        "choices": ["Mount Everest", "K2", "Kangchenjunga", "Lhotse"],
        "answer": "d",
    },
    {
        "question": "Who is the author of 'The Time Machine'?",
        "choices": ["George Orwell", "Aldous Huxley", "Ray Bradbury", "H.G. Wells"],
        "answer": "d",
    },
    {
        "question": "What is the fourth largest mammal in the world?",
        "choices": ["Blue Whale", "Elephant", "Giraffe", "Hippopotamus"],
        "answer": "d",
    },
    {
        "question": "What is the capital of South Korea?",
        "choices": ["Madrid", "Lisbon", "Buenos Aires", "Seoul"],
        "answer": "d",
    },
    {
        "question": "Which planet is fourth closest to the sun?",
        "choices": ["Mercury", "Venus", "Earth", "Mars"],
        "answer": "d",
    },
    {
        "question": "What is the fourth longest river in the world?",
        "choices": ["Nile", "Amazon", "Yangtze", "Mississippi"],
        "answer": "d",
    },
    {
        "question": "Who discovered radioactivity?",
        "choices": [
            "Alexander Fleming",
            "Albert Einstein",
            "Louis Pasteur",
            "Marie Curie",
        ],
        "answer": "d",
    },
    {
        "question": "What is the capital of Italy?",
        "choices": ["Berlin", "Moscow", "Beijing", "Rome"],
        "answer": "d",
    },
    {
        "question": "What is the fourth largest desert in the world?",
        "choices": ["Sahara", "Gobi", "Kalahari", "Arabian"],
        "answer": "d",
    },
    {
        "question": "Who wrote 'Dracula'?",
        "choices": ["Jane Austen", "Charlotte Bronte", "Emily Bronte", "Bram Stoker"],
        "answer": "d",
    },
    {
        "question": "What is the chemical symbol for nitrogen?",
        "choices": ["H2O", "CO2", "O2", "N2"],
        "answer": "d",
    },
    {
        "question": "Which country is known for the Great Wall?",
        "choices": ["Canada", "USA", "France", "China"],
        "answer": "d",
    },
    {
        "question": "What is the capital of Russia?",
        "choices": ["Ottawa", "Brasilia", "Mexico City", "Moscow"],
        "answer": "d",
    },
    # Custom questions
    {
        "question": "Who is a cuck in the Dizznem comm?",
        "choices": ["Dizznem", "Wack", "Water", "Hunter"],
        "answer": "b",
    },
    {
        "question": "Who is the most inspirational person in Dizznem comm?",
        "choices": ["Dizznem", "Kwintin", "Karma SB", "Flizz"],
        "answer": "c",
    },
    {
        "question": "Who coded Dizznem bot?",
        "choices": ["Dizznem", "AI", "Fiverr hire", "Karma SB"],
        "answer": "d",
    },
    {
        "question": "Who is the most handsome person in Dizznem comm?",
        "choices": ["Karma SB", "Kwintin", "Dizznem", "Flizz"],
        "answer": "a",
    },
    {
        "question": "Who is the most retarded person in Dizznem comm?",
        "choices": ["Karma SB", "Dizznem", "Woomer", "Burn"],
        "answer": "b",
    },
    {
        "question": "Who is the most intelligent person in Dizznem comm?",
        "choices": ["Woomer", "Dizznem", "Karma SB", "Ultra"],
        "answer": "c",
    },
    {
        "question": "What is Dizznem's favorite word?",
        "choices": ["wrong option", "wrong option", "wrong option", "Ni--er"],
        "answer": "d",
    },
]

VALID_ANSWERS: frozenset[str] = frozenset({"a", "b", "c", "d"})


def get_random_question() -> tuple[str, list[str], str]:
    """Get a random trivia question.

    Returns:
        tuple[str, list[str], str]: (question, choices, answer)
    """
    entry: dict = random.choice(TRIVIA_LIST)  # noqa: S311
    return entry["question"], entry["choices"], entry["answer"]


def build_trivia_embed(question: str, choices: list[str]) -> Embed:
    """Build a trivia question embed.

    Args:
        question (str): The trivia question.
        choices (list[str]): The four answer choices.

    Returns:
        Embed: The trivia embed.
    """
    labels: list[str] = ["🇦", "🇧", "🇨", "🇩"]
    choice_text: str = "\n".join(
        f"{labels[i]} **{choice}**" for i, choice in enumerate(choices)
    )
    return Embed(
        title="🧠 Trivia",
        color=Color.og_blurple(),
        description=f"**{question}**\n\n{choice_text}\n\n*You have 15 seconds to answer.*",
    )
