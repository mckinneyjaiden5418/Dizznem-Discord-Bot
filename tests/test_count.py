"""Tests for utils/misc/count.py."""

import sqlite3
from pathlib import Path

import pytest
from utils.misc.count import ensure_count_db, increment_count


@pytest.fixture
def db(tmp_path: Path) -> Path:
    """Create a temporary count database."""
    db_path: Path = tmp_path / "count.db"
    ensure_count_db(db_path)
    return db_path


class TestEnsureCountDb:
    """Tests for ensure_count_db."""

    def test_creates_db_file(self, tmp_path: Path) -> None:
        """Test that the database file is created."""
        db_path: Path = tmp_path / "count.db"
        ensure_count_db(db_path)
        assert db_path.exists()

    def test_initializes_count_at_zero(self, db: Path) -> None:
        """Test that the count initializes at zero."""
        with sqlite3.connect(db) as conn:
            count: int = conn.execute(
                "SELECT count FROM count WHERE id = 1",
            ).fetchone()[0]
        assert count == 0

    def test_does_not_reset_on_second_call(self, db: Path) -> None:
        """Test that calling ensure_count_db again does not reset the count."""
        increment_count(db)
        ensure_count_db(db)

        with sqlite3.connect(db) as conn:
            count: int = conn.execute(
                "SELECT count FROM count WHERE id = 1",
            ).fetchone()[0]
        assert count == 1


class TestIncrementCount:
    """Tests for increment_count."""

    def test_increments_from_zero(self, db: Path) -> None:
        """Test that increment_count increases a zero value to one."""
        result: int = increment_count(db)
        assert result == 1

    def test_increments_multiple_times(self, db: Path) -> None:
        """Test that increment_count correctly increments multiple times."""
        increment_count(db)
        increment_count(db)
        result: int = increment_count(db)
        assert result == 3  # noqa: PLR2004

    def test_returns_new_count(self, db: Path) -> None:
        """Test that increment_count returns the updated count value."""
        result: int = increment_count(db)
        assert isinstance(result, int)
        assert result > 0
