"""Tests for utils/money/stocks.py."""

import sqlite3
from pathlib import Path

import pytest

from utils.money.stocks import (
    DEFAULT_PRICES,
    STOCK_MAP,
    buy_stock,
    ensure_stocks_tables,
    get_all_prices,
    get_price,
    get_user_stocks,
    is_market_open,
    sell_stock,
)


@pytest.fixture()
def db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Set up a temporary stocks database with a fresh user cache."""
    db_path: Path = tmp_path / "users.db"

    monkeypatch.setattr("user.DB_PATH", db_path)
    monkeypatch.setattr("user.USER_CACHE", {})

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

    ensure_stocks_tables(db_path)
    return db_path


@pytest.fixture()
def funded_user(db: Path) -> tuple[Path, int, str]:
    """Insert a user with money and return (db_path, user_id, username)."""
    user_id: int = 999
    username: str = "karma"

    with sqlite3.connect(db) as conn:
        conn.execute(
            "INSERT INTO users (id, name, money) VALUES (?, ?, ?)",
            (user_id, username, 100_000.0),
        )

    return db, user_id, username


class TestEnsureStocksTables:
    def test_creates_stock_prices_table(self, db: Path) -> None:
        with sqlite3.connect(db) as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'",
            ).fetchall()
        table_names = [t[0] for t in tables]
        assert "stock_prices" in table_names

    def test_creates_user_stocks_table(self, db: Path) -> None:
        with sqlite3.connect(db) as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'",
            ).fetchall()
        table_names = [t[0] for t in tables]
        assert "user_stocks" in table_names

    def test_seeds_default_prices(self, db: Path) -> None:
        prices = get_all_prices(db)
        names = [p[0] for p in prices]
        for stock_name in DEFAULT_PRICES:
            assert stock_name in names


class TestGetPrice:
    def test_returns_price_for_valid_stock(self, db: Path) -> None:
        price: float | None = get_price(db, "Dizznem")
        assert price == DEFAULT_PRICES["Dizznem"]

    def test_returns_none_for_invalid_stock(self, db: Path) -> None:
        price: float | None = get_price(db, "FakeStock")
        assert price is None


class TestGetAllPrices:
    def test_returns_all_stocks(self, db: Path) -> None:
        prices = get_all_prices(db)
        assert len(prices) == len(DEFAULT_PRICES)

    def test_each_row_has_three_values(self, db: Path) -> None:
        for row in get_all_prices(db):
            assert len(row) == 3


class TestIsMarketOpen:
    def test_returns_bool(self) -> None:
        result: bool = is_market_open()
        assert isinstance(result, bool)


class TestStockMap:
    def test_all_stocks_have_entries(self) -> None:
        for name in DEFAULT_PRICES:
            assert name in STOCK_MAP

    def test_stock_map_not_empty(self) -> None:
        assert len(STOCK_MAP) > 0


class TestBuyStock:
    def test_successful_purchase(self, funded_user: tuple) -> None:
        db, user_id, username = funded_user
        success, msg = buy_stock(db, user_id, username, "Dizznem", 1)
        assert success is True
        assert "Dizznem" in msg

    def test_insufficient_funds_fails(self, db: Path) -> None:
        with sqlite3.connect(db) as conn:
            conn.execute(
                "INSERT INTO users (id, name, money) VALUES (?, ?, ?)",
                (1, "broke", 0.0),
            )
        success, msg = buy_stock(db, 1, "broke", "Dizznem", 1)
        assert success is False
        assert "Insufficient" in msg

    def test_invalid_stock_fails(self, funded_user: tuple) -> None:
        db, user_id, username = funded_user
        success, msg = buy_stock(db, user_id, username, "FakeStock", 1)
        assert success is False
        assert "does not exist" in msg

    def test_deducts_money_on_purchase(self, funded_user: tuple) -> None:
        from user import USER_CACHE

        db, user_id, username = funded_user
        price: float = get_price(db, "Dizznem")  # type: ignore[assignment]
        buy_stock(db, user_id, username, "Dizznem", 1)

        user = USER_CACHE[user_id]
        assert user.money == pytest.approx(100_000.0 - price)


class TestSellStock:
    def test_cannot_sell_stock_not_owned(self, funded_user: tuple) -> None:
        db, user_id, username = funded_user
        success, msg = sell_stock(db, user_id, username, "Dizznem", 1)
        assert success is False
        assert "only own" in msg

    def test_sell_after_buy_succeeds(self, funded_user: tuple) -> None:
        db, user_id, username = funded_user
        buy_stock(db, user_id, username, "Dizznem", 5)
        success, msg = sell_stock(db, user_id, username, "Dizznem", 5)
        assert success is True
        assert "Dizznem" in msg

    def test_cannot_sell_more_than_owned(self, funded_user: tuple) -> None:
        db, user_id, username = funded_user
        buy_stock(db, user_id, username, "Dizznem", 2)
        success, msg = sell_stock(db, user_id, username, "Dizznem", 10)
        assert success is False


class TestGetUserStocks:
    def test_empty_portfolio(self, funded_user: tuple) -> None:
        db, user_id, _ = funded_user
        holdings = get_user_stocks(db, user_id)
        assert holdings == []

    def test_portfolio_after_purchase(self, funded_user: tuple) -> None:
        db, user_id, username = funded_user
        buy_stock(db, user_id, username, "Dizznem", 3)
        holdings = get_user_stocks(db, user_id)
        assert len(holdings) == 1
        name, qty, value = holdings[0]
        assert name == "Dizznem"
        assert qty == 3
        assert value > 0