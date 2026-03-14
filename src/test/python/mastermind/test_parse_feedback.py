"""Tests for assisted._parse_feedback — pure function, no JVM needed."""

import pytest
from mastermind.gamemode.assisted import _parse_feedback


class TestValidFormats:
    def test_xbyw_format(self):
        assert _parse_feedback("2b1w", d=4) == 21

    def test_xy_format_no_letters(self):
        assert _parse_feedback("21", d=4) == 21

    def test_space_separated(self):
        assert _parse_feedback("2 1", d=4) == 21

    def test_zero_blacks_zero_whites(self):
        assert _parse_feedback("0b0w", d=4) == 0

    def test_full_black(self):
        assert _parse_feedback("4b0w", d=4) == 40

    def test_zero_blacks_with_whites(self):
        assert _parse_feedback("0b3w", d=4) == 3

    def test_leading_trailing_whitespace(self):
        assert _parse_feedback("  2b1w  ", d=4) == 21

    def test_uppercase_letters(self):
        assert _parse_feedback("2B1W", d=4) == 21

    def test_mixed_case(self):
        assert _parse_feedback("2B1w", d=4) == 21

    def test_xb_only_no_w(self):
        # e.g. "2b1" — b present, w absent — regex allows this
        assert _parse_feedback("2b1", d=4) == 21

    def test_exact_sum_equals_d(self):
        assert _parse_feedback("2b2w", d=4) == 22

    def test_one_digit_d(self):
        assert _parse_feedback("1b0w", d=1) == 10


class TestInvalidFormats:
    def test_empty_string(self):
        assert _parse_feedback("", d=4) is None

    def test_letters_only(self):
        assert _parse_feedback("abcd", d=4) is None

    def test_only_one_number(self):
        assert _parse_feedback("2", d=4) is None

    def test_three_numbers(self):
        assert _parse_feedback("2b1w3", d=4) is None

    def test_sum_exceeds_d(self):
        assert _parse_feedback("3b2w", d=4) is None

    def test_whites_alone_exceed_d(self):
        assert _parse_feedback("0b5w", d=4) is None

    def test_negative_not_representable(self):
        # Can't enter a negative digit via the regex, but a value > 9 is also invalid format
        assert (
            _parse_feedback("10b0w", d=10) is None
        )  # two-digit blacks → regex won't match


class TestEncoding:
    """Verify the black*10 + white encoding for a range of inputs."""

    @pytest.mark.parametrize(
        "black,white,d",
        [
            (0, 0, 4),
            (1, 0, 4),
            (0, 1, 4),
            (3, 1, 4),
            (4, 0, 4),
            (0, 4, 4),
            (1, 3, 4),
        ],
    )
    def test_encoding(self, black, white, d):
        raw = f"{black}b{white}w"
        assert _parse_feedback(raw, d) == black * 10 + white
