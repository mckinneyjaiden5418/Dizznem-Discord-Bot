"""Tests for utils/misc/inspiration.py."""

import sqlite3
from pathlib import Path
from typing import Any

import pytest
from utils.misc.inspiration import (
    DEFAULT_QUOTES,
    add_quote,
    ensure_inspiration_db,
    get_random_quote,
    validate_quote,
)


@pytest.fixture
def db(tmp_path: Path) -> Path:
    """Create a temporary inspiration database."""
    db_path: Path = tmp_path / "inspiration.db"
    ensure_inspiration_db(db_path)
    return db_path


class TestEnsureInspirationDb:
    """Tests for ensure_inspiration_db."""

    def test_creates_db_file(self, tmp_path: Path) -> None:
        """Test that the inspiration database file is created."""
        db_path: Path = tmp_path / "inspiration.db"
        ensure_inspiration_db(db_path)
        assert db_path.exists()

    def test_seeds_default_quotes(self, db: Path) -> None:
        """Test that default quotes are seeded into the database."""
        quote: str | None = get_random_quote(db)
        assert quote in DEFAULT_QUOTES

    def test_does_not_duplicate_on_second_call(self, db: Path) -> None:
        """Test that calling ensure_inspiration_db again does not duplicate quotes."""
        ensure_inspiration_db(db)

        with sqlite3.connect(db) as conn:
            count: int = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        assert count == len(DEFAULT_QUOTES)


class TestGetRandomQuote:
    """Tests for get_random_quote."""

    def test_returns_string(self, db: Path) -> None:
        """Test that get_random_quote returns a string."""
        quote: str | None = get_random_quote(db)
        assert isinstance(quote, str)

    def test_returns_none_on_empty_db(self, tmp_path: Path) -> None:
        """Test that get_random_quote returns None when the database has no quotes."""
        db_path: Path = tmp_path / "empty.db"
        ensure_inspiration_db(db_path)

        with sqlite3.connect(db_path) as conn:
            conn.execute("DELETE FROM messages")

        assert get_random_quote(db_path) is None

    def test_returns_a_known_quote(self, db: Path) -> None:
        """Test that get_random_quote returns one of the seeded quotes."""
        quote: str | None = get_random_quote(db)
        assert quote in DEFAULT_QUOTES


class TestAddQuote:
    """Tests for add_quote."""

    def test_adds_quote_to_db(self, db: Path) -> None:
        """Test that add_quote stores a new quote in the database."""
        add_quote(db, "Test quote for testing purposes.")
        with sqlite3.connect(db) as conn:
            rows: list[Any] = conn.execute("SELECT message FROM messages").fetchall()
        messages: list[Any] = [r[0] for r in rows]
        assert "Test quote for testing purposes." in messages

    def test_count_increases_after_add(self, db: Path) -> None:
        """Test that the quote count increases after adding a new quote."""
        before: int = (
            sqlite3.connect(db).execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        )
        add_quote(db, "Another test quote here.")
        after: int = (
            sqlite3.connect(db).execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        )
        assert after == before + 1


class TestValidateQuote:
    """Tests for validate_quote."""

    def test_valid_quote_passes(self) -> None:
        """Test that a valid quote passes validation."""
        valid, _ = validate_quote("This is a perfectly fine quote.")
        assert valid is True

    def test_too_short_fails(self) -> None:
        """Test that quotes that are too short fail validation."""
        valid, msg = validate_quote("short")
        assert valid is False
        assert "short" in msg.lower()

    def test_too_long_fails(self) -> None:
        """Test that quotes that are too long fail validation."""
        valid, msg = validate_quote("a" * 301)
        assert valid is False
        assert "long" in msg.lower()

    def test_too_many_line_breaks_fails(self) -> None:
        """Test that quotes with too many line breaks fail validation."""
        valid, msg = validate_quote("line\nline\nline\nline\nline")
        assert valid is False
        assert "line break" in msg.lower()

    def test_mostly_symbols_fails(self) -> None:
        """Test that quotes made mostly of symbols fail validation."""
        valid, _ = validate_quote("!@#$%^&*()!@#$%^&*()")
        assert valid is False

    def test_strips_whitespace_before_validation(self) -> None:
        """Test that whitespace is stripped before quote validation."""
        valid, _ = validate_quote("   This is a perfectly fine quote.   ")
        assert valid is True

    def test_empty_error_message_on_valid(self) -> None:
        """Test that valid quotes return an empty error message."""
        _, msg = validate_quote("This is a perfectly fine quote.")
        assert msg == ""
