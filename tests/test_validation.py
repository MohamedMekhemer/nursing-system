import pytest

from validation import validate_age, validate_name


def test_valid_age_is_converted_to_integer():
    assert validate_age("25") == 25


def test_non_integer_age_is_rejected():
    with pytest.raises(ValueError):
        validate_age("abc")


def test_age_outside_range_is_rejected():
    with pytest.raises(ValueError):
        validate_age("150")


def test_name_is_stripped():
    assert validate_name("  Ahmed  ") == "Ahmed"


def test_empty_name_is_rejected():
    with pytest.raises(ValueError):
        validate_name(" ")