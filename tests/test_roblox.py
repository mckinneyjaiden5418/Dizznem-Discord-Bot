"""Tests for utils/money/roblox.py."""

from utils.money.roblox import check_answer, nicknames


class TestCheckAnswer:
    """Tests for check_answer."""

    def test_correct_exact_answer(self) -> None:
        """Test that exact answers are recognized as correct."""
        assert check_answer("fischeran", "fischeran") is True

    def test_wrong_answer(self) -> None:
        """Test that an incorrect answer is rejected."""
        assert check_answer("fischeran", "goku") is False

    def test_case_insensitive(self) -> None:
        """Test that answer matching is case insensitive."""
        assert check_answer("fischeran", "FISCHERAN") is True

    def test_strips_whitespace(self) -> None:
        """Test that whitespace is ignored in answers."""
        assert check_answer("fischeran", "  fischeran  ") is True

    def test_nickname_resolves_correctly(self) -> None:
        """Test that nicknames resolve correctly to the expected answer."""
        assert check_answer("fischeran", "fisch") is True

    def test_wrong_nickname_fails(self) -> None:
        """Test that an incorrect nickname is rejected."""
        assert check_answer("fischeran", "pd") is False


class TestNicknames:
    """Tests for nicknames."""

    def test_known_nickname_resolved(self) -> None:
        """Test that a known nickname resolves to the correct value."""
        assert nicknames("fisch") == "fischeran"

    def test_pd_resolves(self) -> None:
        """Test that 'pd' resolves to the expected item."""
        assert nicknames("pd") == "phoenix down"

    def test_wka_resolves(self) -> None:
        """Test that 'wka' resolves to the expected item."""
        assert nicknames("wka") == "white kings amulet"

    def test_ff_resolves(self) -> None:
        """Test that 'ff' resolves to the expected item."""
        assert nicknames("ff") == "fairfrozen"

    def test_philosophers_stone_alternate_spelling(self) -> None:
        """Test that alternate spellings resolve correctly."""
        assert nicknames("philosopher's stone") == "philosophers stone"

    def test_unknown_name_returns_itself(self) -> None:
        """Test that unknown valid names return themselves."""
        assert nicknames("fischeran") == "fischeran"

    def test_unknown_name_no_match(self) -> None:
        """Test that totally unknown names are returned unchanged."""
        assert nicknames("totallyrandom") == "totallyrandom"

    def test_case_insensitive_lookup(self) -> None:
        """Test that nickname lookup ignores case."""
        assert nicknames("FISCH") == "fischeran"

    def test_lava_serpent_alias(self) -> None:
        """Test that 'lava serpent' resolves to the proper alias."""
        assert nicknames("lava serpent") == "lava snake"

    def test_tundra_dragon_alias(self) -> None:
        """Test that 'tundra dragon' resolves to the proper alias."""
        assert nicknames("tundra dragon") == "ice dragon"
