"""
tests.testing_playground
~~~~~~~~~~~~~~~~~~~~~~~~

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

This file exists to test screw around with implementation details.
"""  # noqa: D205, D400

from warmac import cli_parser

# print(cli_parser.str_to_int_bounds_check("5", -1, 4, "timerange"))
# cli_parser.handle_input(["average"])
cli_parser.handle_input(["help", "average"])
