"""Tests for utils/numbers.py."""

import pytest
from utils.numbers import convert_money_str, format_duration, format_number


class TestFormatNumber:
    """Tests for format_number function."""

    def test_whole_number_removes_decimal(self) -> None:
        """Test that whole numbers are formatted without a decimal point."""
        assert format_number(1000) == "1,000"

    def test_decimal_is_kept(self) -> None:
        """Test that decimal numbers are formatted with a decimal point."""
        assert format_number(1000.50) == "1,000.50"

    def test_zero(self) -> None:
        """Test that zero is formatted correctly."""
        assert format_number(0) == "0"

    def test_large_number(self) -> None:
        """Test that large numbers are formatted with commas."""
        assert format_number(1_000_000) == "1,000,000"

    def test_cents_only(self) -> None:
        """Test that numbers with only cents are formatted correctly."""
        assert format_number(0.99) == "0.99"

    def test_negative(self) -> None:
        """Test that negative numbers are formatted correctly."""
        assert format_number(-500) == "-500"


class TestConvertMoneyStr:
    """Tests for convert_money_str function."""

    def test_plain_integer_string(self) -> None:
        """Test that plain integer strings are converted correctly."""
        assert convert_money_str("1000") == 1000.0  # noqa: PLR2004

    def test_plain_float_string(self) -> None:
        """Test that plain float strings are converted correctly."""
        assert convert_money_str("9.99") == 9.99  # noqa: PLR2004

    def test_dollar_sign_stripped(self) -> None:
        """Test that dollar signs are stripped correctly."""
        assert convert_money_str("$500") == 500.0  # noqa: PLR2004

    def test_commas_stripped(self) -> None:
        """Test that commas are stripped correctly."""
        assert convert_money_str("1,000,000") == 1_000_000.0  # noqa: PLR2004

    def test_dollar_sign_and_commas(self) -> None:
        """Test that both dollar signs and commas are stripped correctly."""
        assert convert_money_str("$1,500.75") == 1500.75  # noqa: PLR2004

    def test_whitespace_stripped(self) -> None:
        """Test that whitespace is stripped correctly."""
        assert convert_money_str("  100  ") == 100.0  # noqa: PLR2004

    def test_int_passthrough(self) -> None:
        """Test that integers are passed through correctly."""
        assert convert_money_str(500) == 500  # type: ignore[arg-type]  # noqa: PLR2004

    def test_float_passthrough(self) -> None:
        """Test that floats are passed through correctly."""
        assert convert_money_str(3.14) == 3.14  # type: ignore[arg-type]  # noqa: PLR2004

    def test_invalid_string_raises(self) -> None:
        """Test that invalid strings raise a ValueError."""
        with pytest.raises(ValueError):  # noqa: PT011
            convert_money_str("abc")

    def test_empty_string_raises(self) -> None:
        """Test that empty strings raise a ValueError."""
        with pytest.raises(ValueError):  # noqa: PT011
            convert_money_str("")


class TestFormatDuration:
    """Tests for format_duration function."""

    def test_seconds_only(self) -> None:
        """Test that durations with only seconds are formatted correctly."""
        assert format_duration(45) == "45 seconds"

    def test_one_second(self) -> None:
        """Test that durations with one second are formatted correctly."""
        assert format_duration(1) == "1 second"

    def test_minutes_and_seconds(self) -> None:
        """Test that durations with minutes and seconds are formatted correctly."""
        assert format_duration(90) == "1 minute, 30 seconds"

    def test_one_minute(self) -> None:
        """Test that durations with one minute are formatted correctly."""
        assert format_duration(60) == "1 minute"

    def test_hours_minutes_seconds(self) -> None:
        """Test that durations with hours, minutes, and seconds are formatted correctly."""
        assert format_duration(3661) == "1 hour, 1 minute, 1 second"

    def test_one_hour(self) -> None:
        """Test that durations with one hour are formatted correctly."""
        assert format_duration(3600) == "1 hour"

    def test_full_day(self) -> None:
        """Test that durations with a full day are formatted correctly."""
        assert format_duration(86400) == "1 day"

    def test_weekly_cooldown(self) -> None:
        """Test that durations with a weekly cooldown are formatted correctly."""
        assert format_duration(604800) == "7 days"

    def test_zero_returns_zero_seconds(self) -> None:
        """Test that zero durations return zero seconds."""
        assert format_duration(0) == "0 seconds"
