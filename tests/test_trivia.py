"""Tests for utils/money/trivia.py."""

from utils.money.trivia import TRIVIA_LIST, VALID_ANSWERS, get_random_question


class TestValidAnswers:
    """Tests for VALID_ANSWERS."""

    def test_valid_answers_contains_abcd(self) -> None:
        """Test that VALID_ANSWERS contains the expected letters."""
        assert frozenset({"a", "b", "c", "d"}) == VALID_ANSWERS

    def test_valid_answers_does_not_contain_e(self) -> None:
        """Test that VALID_ANSWERS does not include invalid answer options."""
        assert "e" not in VALID_ANSWERS


class TestTriviaList:
    """Tests for TRIVIA_LIST."""

    def test_all_questions_have_required_keys(self) -> None:
        """Test that every trivia entry has the required keys."""
        for entry in TRIVIA_LIST:
            assert "question" in entry
            assert "choices" in entry
            assert "answer" in entry

    def test_all_answers_are_valid(self) -> None:
        """Test that every trivia answer is valid."""
        for entry in TRIVIA_LIST:
            assert entry["answer"] in VALID_ANSWERS

    def test_all_questions_have_four_choices(self) -> None:
        """Test that every trivia question has exactly four choices."""
        for entry in TRIVIA_LIST:
            assert len(entry["choices"]) == 4  # noqa: PLR2004

    def test_all_questions_are_non_empty_strings(self) -> None:
        """Test that every trivia question is a non-empty string."""
        for entry in TRIVIA_LIST:
            assert isinstance(entry["question"], str)
            assert len(entry["question"]) > 0

    def test_covers_all_answer_letters(self) -> None:
        """Test that the trivia list covers all valid answer letters."""
        answers_used: set[str] = {entry["answer"] for entry in TRIVIA_LIST}
        assert answers_used == VALID_ANSWERS


class TestGetRandomQuestion:
    """Tests for get_random_question."""

    def test_returns_three_values(self) -> None:
        """Test that get_random_question returns three values."""
        result: tuple[str, list[str], str] = get_random_question()
        assert len(result) == 3  # noqa: PLR2004

    def test_question_is_string(self) -> None:
        """Test that the returned question is a string."""
        question, _, _ = get_random_question()
        assert isinstance(question, str)

    def test_choices_is_list_of_four(self) -> None:
        """Test that returned choices are a list of four elements."""
        _, choices, _ = get_random_question()
        assert isinstance(choices, list)
        assert len(choices) == 4  # noqa: PLR2004

    def test_answer_is_valid(self) -> None:
        """Test that the returned answer is valid."""
        _, _, answer = get_random_question()
        assert answer in VALID_ANSWERS

    def test_returns_different_questions(self) -> None:
        """Test that get_random_question can return different questions over repeated calls."""
        # Run 20 times — statistically near-impossible to always get the same one
        results: set[str] = {get_random_question()[0] for _ in range(20)}
        assert len(results) > 1
