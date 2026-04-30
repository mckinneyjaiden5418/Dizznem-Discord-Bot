"""Tests for utils/numbers.py."""

import pytest

from utils.numbers import convert_money_str, format_duration, format_number


class TestFormatNumber:
    def test_whole_number_removes_decimal(self) -> None:
        assert format_number(1000) == "1,000"

    def test_decimal_is_kept(self) -> None:
        assert format_number(1000.50) == "1,000.50"

    def test_zero(self) -> None:
        assert format_number(0) == "0"

    def test_large_number(self) -> None:
        assert format_number(1_000_000) == "1,000,000"

    def test_cents_only(self) -> None:
        assert format_number(0.99) == "0.99"

    def test_negative(self) -> None:
        assert format_number(-500) == "-500"


class TestConvertMoneyStr:
    def test_plain_integer_string(self) -> None:
        assert convert_money_str("1000") == 1000.0

    def test_plain_float_string(self) -> None:
        assert convert_money_str("9.99") == 9.99

    def test_dollar_sign_stripped(self) -> None:
        assert convert_money_str("$500") == 500.0

    def test_commas_stripped(self) -> None:
        assert convert_money_str("1,000,000") == 1_000_000.0

    def test_dollar_sign_and_commas(self) -> None:
        assert convert_money_str("$1,500.75") == 1500.75

    def test_whitespace_stripped(self) -> None:
        assert convert_money_str("  100  ") == 100.0

    def test_int_passthrough(self) -> None:
        assert convert_money_str(500) == 500  # type: ignore[arg-type]

    def test_float_passthrough(self) -> None:
        assert convert_money_str(3.14) == 3.14  # type: ignore[arg-type]

    def test_invalid_string_raises(self) -> None:
        with pytest.raises(ValueError):
            convert_money_str("abc")

    def test_empty_string_raises(self) -> None:
        with pytest.raises(ValueError):
            convert_money_str("")


class TestFormatDuration:
    def test_seconds_only(self) -> None:
        assert format_duration(45) == "45 seconds"

    def test_one_second(self) -> None:
        assert format_duration(1) == "1 second"

    def test_minutes_and_seconds(self) -> None:
        assert format_duration(90) == "1 minute, 30 seconds"

    def test_one_minute(self) -> None:
        assert format_duration(60) == "1 minute"

    def test_hours_minutes_seconds(self) -> None:
        assert format_duration(3661) == "1 hour, 1 minute, 1 second"

    def test_one_hour(self) -> None:
        assert format_duration(3600) == "1 hour"

    def test_full_day(self) -> None:
        assert format_duration(86400) == "1 day"

    def test_daily_cooldown(self) -> None:
        # 86400 seconds = 1 day (matches $daily cooldown)
        assert format_duration(86400) == "1 day"

    def test_weekly_cooldown(self) -> None:
        # 604800 seconds = 7 days (matches $weekly cooldown)
        assert format_duration(604800) == "7 days"

    def test_zero_returns_zero_seconds(self) -> None:
        assert format_duration(0) == "0 seconds"