"""Tests for utils/money/roblox.py."""

from utils.money.roblox import check_answer, nicknames


class TestCheckAnswer:
    def test_correct_exact_answer(self) -> None:
        assert check_answer("fischeran", "fischeran") is True

    def test_wrong_answer(self) -> None:
        assert check_answer("fischeran", "goku") is False

    def test_case_insensitive(self) -> None:
        assert check_answer("fischeran", "FISCHERAN") is True

    def test_strips_whitespace(self) -> None:
        assert check_answer("fischeran", "  fischeran  ") is True

    def test_nickname_resolves_correctly(self) -> None:
        # "fisch" is a nickname for "fischeran"
        assert check_answer("fischeran", "fisch") is True

    def test_wrong_nickname_fails(self) -> None:
        assert check_answer("fischeran", "pd") is False


class TestNicknames:
    def test_known_nickname_resolved(self) -> None:
        assert nicknames("fisch") == "fischeran"

    def test_pd_resolves(self) -> None:
        assert nicknames("pd") == "phoenix down"

    def test_wka_resolves(self) -> None:
        assert nicknames("wka") == "white kings amulet"

    def test_ff_resolves(self) -> None:
        assert nicknames("ff") == "fairfrozen"

    def test_philosophers_stone_alternate_spelling(self) -> None:
        assert nicknames("philosopher's stone") == "philosophers stone"

    def test_unknown_name_returns_itself(self) -> None:
        assert nicknames("fischeran") == "fischeran"

    def test_unknown_name_no_match(self) -> None:
        assert nicknames("totallyrandom") == "totallyrandom"

    def test_case_insensitive_lookup(self) -> None:
        assert nicknames("FISCH") == "fischeran"

    def test_lava_serpent_alias(self) -> None:
        assert nicknames("lava serpent") == "lava snake"

    def test_tundra_dragon_alias(self) -> None:
        assert nicknames("tundra dragon") == "ice dragon"