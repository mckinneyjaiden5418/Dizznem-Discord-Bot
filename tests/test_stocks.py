"""Tests for utils/money/stocks.py."""

import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING

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

if TYPE_CHECKING:
    from user import User


@pytest.fixture
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


@pytest.fixture
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
    """Tests for ensure_stocks_tables."""

    def test_creates_stock_prices_table(self, db: Path) -> None:
        """Test that the stock_prices table is created."""
        with sqlite3.connect(db) as conn:
            tables: list[tuple[str]] = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'",
            ).fetchall()
        table_names: list[str] = [t[0] for t in tables]
        assert "stock_prices" in table_names

    def test_creates_user_stocks_table(self, db: Path) -> None:
        """Test that the user_stocks table is created."""
        with sqlite3.connect(db) as conn:
            tables: list[tuple[str]] = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'",
            ).fetchall()
        table_names: list[str] = [t[0] for t in tables]
        assert "user_stocks" in table_names

    def test_seeds_default_prices(self, db: Path) -> None:
        """Test that default stock prices are seeded into the database."""
        prices: list[tuple[str, float]] = get_all_prices(db)
        names: list[str] = [p[0] for p in prices]
        for stock_name in DEFAULT_PRICES:
            assert stock_name in names


class TestGetPrice:
    """Tests for get_price."""

    def test_returns_price_for_valid_stock(self, db: Path) -> None:
        """Test that get_price returns a valid stock price."""
        price: float | None = get_price(db, "Dizznem")
        assert price == DEFAULT_PRICES["Dizznem"]

    def test_returns_none_for_invalid_stock(self, db: Path) -> None:
        """Test that get_price returns None for an invalid stock."""
        price: float | None = get_price(db, "FakeStock")
        assert price is None


class TestGetAllPrices:
    """Tests for get_all_prices."""

    def test_returns_all_stocks(self, db: Path) -> None:
        """Test that get_all_prices returns every available stock."""
        prices: list[tuple[str, float]] = get_all_prices(db)
        assert len(prices) == len(DEFAULT_PRICES)

    def test_each_row_has_three_values(self, db: Path) -> None:
        """Test that each returned price row contains three values."""
        prices: list[tuple[str, float]] = get_all_prices(db)
        for row in prices:
            assert len(row) == 3  # noqa: PLR2004


class TestIsMarketOpen:
    """Tests for is_market_open."""

    def test_returns_bool(self) -> None:
        """Test that is_market_open returns a boolean."""
        result: bool = is_market_open()
        assert isinstance(result, bool)


class TestStockMap:
    """Tests for STOCK_MAP."""

    def test_all_stocks_have_entries(self) -> None:
        """Test that every default stock exists in STOCK_MAP."""
        for name in DEFAULT_PRICES:
            assert name in STOCK_MAP

    def test_stock_map_not_empty(self) -> None:
        """Test that STOCK_MAP is not empty."""
        assert len(STOCK_MAP) > 0


class TestBuyStock:
    """Tests for buy_stock."""

    def test_successful_purchase(self, funded_user: tuple) -> None:
        """Test that buying a stock succeeds under normal conditions."""
        db, user_id, username = funded_user
        success, msg = buy_stock(db, user_id, username, "Dizznem", 1)
        assert success is True
        assert "Dizznem" in msg

    def test_insufficient_funds_fails(self, db: Path) -> None:
        """Test that stock purchase fails when the user has insufficient funds."""
        with sqlite3.connect(db) as conn:
            conn.execute(
                "INSERT INTO users (id, name, money) VALUES (?, ?, ?)",
                (1, "broke", 0.0),
            )
        success, msg = buy_stock(db, 1, "broke", "Dizznem", 1)
        assert success is False
        assert "Insufficient" in msg

    def test_invalid_stock_fails(self, funded_user: tuple) -> None:
        """Test that purchasing an invalid stock fails."""
        db, user_id, username = funded_user
        success, msg = buy_stock(db, user_id, username, "FakeStock", 1)
        assert success is False
        assert "does not exist" in msg

    def test_deducts_money_on_purchase(self, funded_user: tuple) -> None:
        """Test that the user's balance is reduced after purchasing a stock."""
        from user import USER_CACHE  # noqa: PLC0415

        db, user_id, username = funded_user
        price: float = get_price(db, "Dizznem")  # type: ignore[assignment]
        buy_stock(db, user_id, username, "Dizznem", 1)

        user: User = USER_CACHE[user_id]
        assert user.money == pytest.approx(100_000.0 - price)


class TestSellStock:
    """Tests for sell_stock."""

    def test_cannot_sell_stock_not_owned(self, funded_user: tuple) -> None:
        """Test that selling a stock not owned fails."""
        db, user_id, username = funded_user
        success, msg = sell_stock(db, user_id, username, "Dizznem", 1)
        assert success is False
        assert "only own" in msg

    def test_sell_after_buy_succeeds(self, funded_user: tuple) -> None:
        """Test that selling a stock after purchase succeeds."""
        db, user_id, username = funded_user
        buy_stock(db, user_id, username, "Dizznem", 5)
        success, msg = sell_stock(db, user_id, username, "Dizznem", 5)
        assert success is True
        assert "Dizznem" in msg

    def test_cannot_sell_more_than_owned(self, funded_user: tuple) -> None:
        """Test that selling more shares than are owned fails."""
        db, user_id, username = funded_user
        buy_stock(db, user_id, username, "Dizznem", 2)
        success, _msg = sell_stock(db, user_id, username, "Dizznem", 10)
        assert success is False


class TestGetUserStocks:
    """Tests for get_user_stocks."""

    def test_empty_portfolio(self, funded_user: tuple) -> None:
        """Test that a new user has an empty stock portfolio."""
        db, user_id, _ = funded_user
        holdings = get_user_stocks(db, user_id)
        assert holdings == []

    def test_portfolio_after_purchase(self, funded_user: tuple) -> None:
        """Test that the portfolio reflects purchased stocks."""
        db, user_id, username = funded_user
        buy_stock(db, user_id, username, "Dizznem", 3)
        holdings = get_user_stocks(db, user_id)
        assert len(holdings) == 1
        name, qty, value = holdings[0]
        assert name == "Dizznem"
        assert qty == 3  # noqa: PLR2004
        assert value > 0
