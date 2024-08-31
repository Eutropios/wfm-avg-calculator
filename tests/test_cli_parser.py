"""
tests.test_cli_parser
~~~~~~~~~~~~~~~~~~~~~

WarMAC — https://github.com/Eutropios/WarMAC
Copyright (C) 2024  Noah Jenner

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-----------------------------------------------------------------------

Test file for cli_parser.py
"""  # noqa: D205, D400

from __future__ import annotations

import argparse
import sys

import pytest

from warmac import cli_parser


# Valid params
def test_input_cast_to_int_with_valid_params() -> None:
    expected_output = 5
    assert cli_parser.int_checking("5", 1, 10) == expected_output


# Input == min
def test_input_val_equal_to_min_val() -> None:
    expected_output = 1
    assert cli_parser.int_checking("1", 1, 10) == expected_output


# Input == max
def test_input_val_equal_to_max_val() -> None:
    expected_output = 10
    assert cli_parser.int_checking("10", 1, 10) == expected_output


# Input > max
def test_above_max_value_input_throws_error() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        cli_parser.int_checking("11", 1, 10)


# Input < min
def test_below_min_value_input_throws_error() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        cli_parser.int_checking("0", 1, 10)


# Input is a float
def test_float_input_throws_error() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        cli_parser.int_checking("1.5", 1, 10)


# Input is a mixed string
def test_mixed_string_input_throws_error() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        cli_parser.int_checking("33foobar", 1, 10)


# Input is a boolean
def test_boolean_input_throws_error() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        cli_parser.int_checking("True", 1, 10)


# Input is None
def test_none_input_throws_error() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        cli_parser.int_checking("None", 1, 10)


# min > max
def test_min_greater_than_max_throws_error() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        cli_parser.int_checking("5", 10, 1)


# Input == min == max
def test_input_equals_min_equals_max() -> None:
    expected_output = 5
    assert cli_parser.int_checking("5", 5, 5) == expected_output


# Input != (min == max)
def test_input_not_eq_min_equals_max_throws_error() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        cli_parser.int_checking("6", 5, 5)


if __name__ == "__main__":
    sys.exit(pytest.main())
