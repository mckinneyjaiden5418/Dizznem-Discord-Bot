"""Tests for user.py."""

import sqlite3
from pathlib import Path

import pytest

from user import User, init_db


@pytest.fixture()
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


@pytest.fixture()
def user(db: Path) -> User:
    """Return a basic test user."""
    return User.create_if_not_exists(user_id=1, username="karma")


class TestUserCreation:
    def test_creates_new_user(self, user: User) -> None:
        assert user.id == 1
        assert user.name == "karma"

    def test_default_money_is_zero(self, user: User) -> None:
        assert user.money == 0.0

    def test_default_level_is_zero(self, user: User) -> None:
        assert user.level == 0

    def test_default_prestige_is_zero(self, user: User) -> None:
        assert user.prestige == 0

    def test_default_message_count_is_zero(self, user: User) -> None:
        assert user.message_count == 0

    def test_returns_same_user_from_cache(self, user: User) -> None:
        same_user: User = User.create_if_not_exists(user_id=1, username="karma")
        assert user is same_user


class TestDirtyTracking:
    def test_not_dirty_on_creation(self, user: User) -> None:
        assert not user.dirty

    def test_dirty_after_money_change(self, user: User) -> None:
        user.money += 1000
        assert user.dirty

    def test_dirty_after_level_change(self, user: User) -> None:
        user.level += 1
        assert user.dirty

    def test_dirty_after_prestige_change(self, user: User) -> None:
        user.prestige += 1
        assert user.dirty

    def test_not_dirty_after_save(self, user: User) -> None:
        user.money += 1000
        user.save()
        assert not user.dirty


class TestLevelUp:
    def test_levels_up_at_threshold(self, user: User) -> None:
        # Level 0 requires 100 messages to level up: 2*(0^2) + 50*0 + 100 = 100
        user.message_count = 100
        user.level_up_if_able()
        assert user.level == 1

    def test_does_not_level_up_below_threshold(self, user: User) -> None:
        user.message_count = 99
        user.level_up_if_able()
        assert user.level == 0

    def test_level_1_threshold(self, user: User) -> None:
        # Level 1 requires: 2*(1^2) + 50*1 + 100 = 152 messages
        user.level = 1
        user.message_count = 152
        user.level_up_if_able()
        assert user.level == 2

    def test_level_up_increases_level_by_one(self, user: User) -> None:
        user.message_count = 100
        user.level_up_if_able()
        assert user.level == 1

    def test_required_messages_formula(self) -> None:
        for level in range(5):
            expected: float = 2 * (level**2) + (50 * level) + 100
            assert expected > 0


class TestSave:
    def test_save_persists_money(self, db: Path, user: User) -> None:
        user.money = 99999.0
        user.save()

        with sqlite3.connect(db) as conn:
            row = conn.execute("SELECT money FROM users WHERE id = 1").fetchone()
        assert row[0] == 99999.0

    def test_save_persists_level(self, db: Path, user: User) -> None:
        user.level = 5
        user.save()

        with sqlite3.connect(db) as conn:
            row = conn.execute("SELECT level FROM users WHERE id = 1").fetchone()
        assert row[0] == 5

    def test_save_persists_prestige(self, db: Path, user: User) -> None:
        user.prestige = 3
        user.save()

        with sqlite3.connect(db) as conn:
            row = conn.execute("SELECT prestige FROM users WHERE id = 1").fetchone()
        assert row[0] == 3