"""
warmac.average
~~~~~~~~~~~~~~

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

Logic for average subcommand.
"""  # noqa: D205, D400

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    class AverageArgs(TypedDict):
        """
        Typings for argparse.Namespace object for average subcommand.

        :param TypedDict: Inherits from TypedDict
        """

        # TODO(Noah): Add docstring to this class, note down members
        subparser: str
        item: str
        statistic: str
        platform: str
        timerange: int
        maxrank: bool
        radiant: bool
        use_buyers: bool
        detailed_report: bool

# pass args in, then type hint the value here with AverageArgs
