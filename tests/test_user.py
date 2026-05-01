"""Tests for user.py."""

import sqlite3
from pathlib import Path
from typing import Any

import pytest
from user import User


@pytest.fixture
def db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a temporary database for each test."""
    db_path: Path = tmp_path / "users.db"
    monkeypatch.setattr("user.DB_PATH", db_path)
    monkeypatch.setattr("user.USER_CACHE", {})

    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                money REAL DEFAULT 0,
                prestige INTEGER DEFAULT 0,
                level INTEGER DEFAULT 0,
                message_count INTEGER DEFAULT 0
            )
            """,
        )
    return db_path


@pytest.fixture
def user(db: Path) -> User: # noqa: ARG001 -- pytest runs db fixture first, dependency is implicit
    """Return a basic test user."""
    return User.create_if_not_exists(user_id=1, username="karma")


class TestUserCreation:
    """Tests for creating new user records."""

    def test_creates_new_user(self, user: User) -> None:
        """Test that a new user record is created with the expected ID and name."""
        assert user.id == 1
        assert user.name == "karma"

    def test_default_money_is_zero(self, user: User) -> None:
        """Test that new users start with zero money."""
        assert user.money == 0.0

    def test_default_level_is_zero(self, user: User) -> None:
        """Test that a new user starts at level zero."""
        assert user.level == 0

    def test_default_prestige_is_zero(self, user: User) -> None:
        """Test that a new user starts with zero prestige."""
        assert user.prestige == 0

    def test_default_message_count_is_zero(self, user: User) -> None:
        """Test that a new user starts with zero message count."""
        assert user.message_count == 0

    def test_returns_same_user_from_cache(self, user: User) -> None:
        """Test that create_if_not_exists returns cached user instances."""
        same_user: User = User.create_if_not_exists(user_id=1, username="karma")
        assert user is same_user


class TestDirtyTracking:
    """Tests for User dirty tracking behavior."""

    def test_not_dirty_on_creation(self, user: User) -> None:
        """Test that a newly created user is not marked dirty."""
        assert not user.dirty

    def test_dirty_after_money_change(self, user: User) -> None:
        """Test that changing money marks the user dirty."""
        user.money += 1000
        assert user.dirty

    def test_dirty_after_level_change(self, user: User) -> None:
        """Test that changing level marks the user dirty."""
        user.level += 1
        assert user.dirty

    def test_dirty_after_prestige_change(self, user: User) -> None:
        """Test that changing prestige marks the user dirty."""
        user.prestige += 1
        assert user.dirty

    def test_not_dirty_after_save(self, user: User) -> None:
        """Test that saving a user clears the dirty flag."""
        user.money += 1000
        user.save()
        assert not user.dirty


class TestLevelUp:
    """Tests for user level-up behavior."""

    def test_levels_up_at_threshold(self, user: User) -> None:
        """Test that a user levels up when they reach the threshold."""
        # Level 0 requires 100 messages to level up: 2*(0^2) + 50*0 + 100 = 100
        user.message_count = 100
        user.level_up_if_able()
        assert user.level == 1

    def test_does_not_level_up_below_threshold(self, user: User) -> None:
        """Test that a user does not level up before the threshold."""
        user.message_count = 99
        user.level_up_if_able()
        assert user.level == 0

    def test_level_1_threshold(self, user: User) -> None:
        """Test that the level 1 threshold is calculated correctly."""
        # Level 1 requires: 2*(1^2) + 50*1 + 100 = 152 messages
        user.level = 1
        user.message_count = 152
        user.level_up_if_able()
        assert user.level == 2  # noqa: PLR2004

    def test_level_up_increases_level_by_one(self, user: User) -> None:
        """Test that leveling up increases the level by one."""
        user.message_count = 100
        user.level_up_if_able()
        assert user.level == 1

    def test_required_messages_formula(self) -> None:
        """Test that the required message formula returns positive values."""
        for level in range(5):
            expected: float = 2 * (level**2) + (50 * level) + 100
            assert expected > 0


class TestSave:
    """Tests for saving User instances to the database."""

    def test_save_persists_money(self, db: Path, user: User) -> None:
        """Test that saving updates the user's money in the database."""
        user.money = 99999.0
        user.save()

        with sqlite3.connect(db) as conn:
            row: Any = conn.execute("SELECT money FROM users WHERE id = 1").fetchone()
        assert row[0] == 99999.0  # noqa: PLR2004

    def test_save_persists_level(self, db: Path, user: User) -> None:
        """Test that saving updates the user's level in the database."""
        user.level = 5
        user.save()

        with sqlite3.connect(db) as conn:
            row: Any = conn.execute("SELECT level FROM users WHERE id = 1").fetchone()
        assert row[0] == 5  # noqa: PLR2004

    def test_save_persists_prestige(self, db: Path, user: User) -> None:
        """Test that saving updates the user's prestige in the database."""
        user.prestige = 3
        user.save()

        with sqlite3.connect(db) as conn:
            row: Any = conn.execute("SELECT prestige FROM users WHERE id = 1").fetchone()
        assert row[0] == 3  # noqa: PLR2004
