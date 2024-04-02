"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Warframe Market Average Calculator (WarMAC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

Retrieves the sell price from all orders of a given item from
https://warframe.market for a specific platform, then finds the average
price in platinum of the orders.

Date of Creation: January 22, 2023
External packages required: urllib3
"""  # noqa: D205, D400

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import urllib3

from warmac import cli_parser, warmac_avg, warmac_errors

if TYPE_CHECKING:
    import argparse
    from typing import Literal

__all__ = ["cli_parser", "warmac_avg", "warmac_errors"]

#: A dictionary of all possible commands
# SUBCMD_TO_FUNC = {
#    "average": warmac_avg.average,
# }


def command_select(args: argparse.Namespace) -> None:
    """
    Select which function to use based on ``args.subparser`` field.

    Use a try block and a dictionary to execute the appropriate function
    corresponding to the field ``args.subparser``.

    :param args: The :py:class:`argparse.Namespace` containing the
        user-supplied command line information.
    :raises warmac_errors.CommandError: An error indicating that the
        desired command does not exist in :py:data:`.SUBCMD_TO_FUNC`.
    """


def main() -> Literal[0]:
    """
    Create a :py:data:`cli_parser.WarMACParser` and run associated
    command.

    Call :py:func:`cli_parser.handle_input` to create and parse a
    :py:class:`cli_parser.WarMACParser`. Arguments are then used in
    the script's execution, beginning by calling
    :py:func:`.command_select` with the parsed arguments.

    :return: Return 0 if everything returns successfully.
    """  # noqa: D205
    command_select(cli_parser.handle_input())
    return 0


if __name__ == "__main__":
    sys.exit(main())
