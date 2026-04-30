"""Tests for utils/money/trivia.py."""

from utils.money.trivia import TRIVIA_LIST, VALID_ANSWERS, get_random_question


class TestValidAnswers:
    def test_valid_answers_contains_abcd(self) -> None:
        assert VALID_ANSWERS == frozenset({"a", "b", "c", "d"})

    def test_valid_answers_does_not_contain_e(self) -> None:
        assert "e" not in VALID_ANSWERS


class TestTriviaList:
    def test_all_questions_have_required_keys(self) -> None:
        for entry in TRIVIA_LIST:
            assert "question" in entry
            assert "choices" in entry
            assert "answer" in entry

    def test_all_answers_are_valid(self) -> None:
        for entry in TRIVIA_LIST:
            assert entry["answer"] in VALID_ANSWERS

    def test_all_questions_have_four_choices(self) -> None:
        for entry in TRIVIA_LIST:
            assert len(entry["choices"]) == 4

    def test_all_questions_are_non_empty_strings(self) -> None:
        for entry in TRIVIA_LIST:
            assert isinstance(entry["question"], str)
            assert len(entry["question"]) > 0

    def test_covers_all_answer_letters(self) -> None:
        answers_used = {entry["answer"] for entry in TRIVIA_LIST}
        assert answers_used == VALID_ANSWERS


class TestGetRandomQuestion:
    def test_returns_three_values(self) -> None:
        result = get_random_question()
        assert len(result) == 3

    def test_question_is_string(self) -> None:
        question, _, _ = get_random_question()
        assert isinstance(question, str)

    def test_choices_is_list_of_four(self) -> None:
        _, choices, _ = get_random_question()
        assert isinstance(choices, list)
        assert len(choices) == 4

    def test_answer_is_valid(self) -> None:
        _, _, answer = get_random_question()
        assert answer in VALID_ANSWERS

    def test_returns_different_questions(self) -> None:
        # Run 20 times — statistically near-impossible to always get the same one
        results = {get_random_question()[0] for _ in range(20)}
        assert len(results) > 1