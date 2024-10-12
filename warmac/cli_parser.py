"""
warmac.cli_parser
~~~~~~~~~~~~~~~~~

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

Command line interface logic for warmac.
"""  # noqa: D205, D400

from __future__ import annotations

import argparse
import contextlib
import shutil
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import Final, NoReturn

# The default time to collect orders until
DEFAULT_TIME: Final = 10
# The current version of WarMAC
_VERSION: Final = "0.0.5"


class CustomHelpFormat(argparse.RawDescriptionHelpFormatter):
    """
    Custom help formatter for :py:class:`cli_parser.WarMACParser`.

    Extend :py:class:`argparse.RawDescriptionHelpFormatter` to
    reimplement a few methods. Reimplementations include removing the
    command metavar tuples, removing the duplicate option metavars,
    and correcting the over-indentation on the help menu.
    """

    def __init__(
        self,
        prog: str,
        indent_increment: int = 2,
        max_help_position: int = 24,
        width: int | None = None,
    ) -> None:
        """
        Construct a :py:class:`.CustomHelpFormat` object.

        :param prog: The name of the program.
        :param indent_increment: How much space should come before the
            options on the help screen, defaults to 2.
        :param max_help_position: The width between ``indent_increment``
            and the help text, defaults to 24.
        :param width: The maximum width that the help screen is able to
            occupy in the terminal, defaults to None.
        """
        super().__init__(prog, indent_increment, max_help_position, width)

    def _format_action_invocation(self, action: argparse.Action) -> str:
        """
        Remove duplicate metavar for options with short and long form.

        Override the ``HelpFormatter._format_action_invocation``
        method to remove the duplicate help metavar for options that
        have both a short-form and a long-form argument.

        :param action: The action in which to be formatted.
        :return: The appropriately formatted string.
        """
        # Return super's invocation option_string is None or nargs is 0
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        # Get the default metavar for optionals
        default = self._get_default_metavar_for_optional(action)
        # Return the option strings joined with only one metavar
        return (
            f"{', '.join(action.option_strings)} {self._format_args(action, default)}"
        )

    def _format_action(self, action: argparse.Action) -> str:
        """
        Remove command metavar tuple and fix metavar indentation.

        Override the ``HelpFormatter._format_action``
        method to remove the command metavar tuple and fix the
        spacings between the option and its associated metavar.

        :param action: The action in which to be formatted.
        :return: ``HelpFormatter._format_action(action)``. If the action
            is a ``_SubParsersAction``, the metavar tuple will be
            excluded, and the leading indentation will be corrected.
        """
        # Fix indentation for subclasses
        result = super()._format_action(action)
        return (
            f"{'':{self._current_indent}}{result.lstrip()}"
            if isinstance(action, argparse._SubParsersAction)
            else result
        )

    def _iter_indented_subactions(
        self,
        action: argparse.Action,
    ) -> Generator[argparse.Action, None, None]:
        """
        Fix leading indentation for command names in the help menu.

        Override the ``HelpFormatter._iter_indented_subactions``
        method to fix the leading indentation for command names in
        the help menu.

        :param action: The action to be yielded from.
        :yield: Actions from a list returned by
            ``action._get_subactions``.
        """
        # Overrides the superclass _iter_indented_subactions method
        # Fixes indentation on command metavar
        if isinstance(action, argparse._SubParsersAction):
            with contextlib.suppress(AttributeError):
                # Yield from actions list if action has _get_subactions
                yield from action._get_subactions()
        else:
            # Yield from superclass' _iter_indented_subactions method
            yield from super()._iter_indented_subactions(action)


def str_to_int_bounds_check(val: str, min_val: int, max_val: int) -> int:
    """
    Return ``val`` as an integer if ``min_val <= val <  max_val``.

    Cast ``val`` to an integer. If ``val`` is not an integer or
    is not ``min_val <= val < max_val``, then raise an
    :py:exc:`argparse.ArgumentTypeError`.

    :param val: The user's input as a string.
    :param min_val: The minimum value that ``int(val)`` can be.
    :param max_val: The maximum value that ``int(val)`` can be.
    :raises argparse.ArgumentTypeError: Raised if ``val`` is not an
        integer or is not ``min_val <= int(val) < max_val``.
    :return: Return ``val`` as an integer.
    """
    with contextlib.suppress(ValueError):
        if min_val <= (casted_int := int(val)) < max_val:
            return casted_int
    msg = f'"{val}" is not an integer in the valid range of [{min_val}, {max_val}).'
    raise argparse.ArgumentTypeError(msg)


class WarMACParser(argparse.ArgumentParser):
    """
    Extend :py:class:`argparse.ArgumentParser` to reimplement the error
    method.

    Extend :py:class:`argparse.ArgumentParser` to reimplement the error
    method so it exits with status code 2, and prints to stderr.
    """  # noqa: D205

    def error(self, message: str) -> NoReturn:
        """
        Modify exit message for :py:class:`argparse.ArgumentError`.

        Modify exit message for :py:class:`argparse.ArgumentError`
        occurrences to print to stderr, and return an exit code of 2.

        :param message: The message provided by the standard
            :py:class:`argparse.ArgumentParser` class.
        :return: A value is never returned by this function.
        """
        self.exit(1, f"{self.usage}: error: {message}\n")
        # change above code to print to stderr, then print cli help to
        # stdout, then exit with code 1


def _create_parser() -> WarMACParser:
    """
    Create the command-line parser for the program.

    Create a :py:class:`.WarMACParser` object that includes global
    --help and --version options. Create subparsers for multiple
    commands to be used within the program.

    :return: The constructed :py:class:`.WarMACParser` object.
    """
    # Min width that help text should take up in usage
    help_min_width: Final = 34
    # Min value of help_min_width and terminal's width
    default_width = min(help_min_width, shutil.get_terminal_size().columns - 2)
    # Platforms the user can choose from
    platforms: Final = ("pc", "ps4", "xbox", "switch")

    parser = WarMACParser(
        usage="warmac <command> [options]",
        description=(
            "A program to fetch the average market cost of an item in Warframe."
        ),
        epilog=(
            "More help can be found at: "
            "https://warmac.readthedocs.io/en/latest/usage/warmac.html"
        ),
        formatter_class=lambda prog: CustomHelpFormat(
            prog=prog,  # first arg in CL, which is the file's name
            max_help_position=default_width,
        ),
        add_help=False,  # don't add default help msg
    )
    parser._positionals.title = "commands"  # changing positional header

    # ------- Main Parser Arguments -------
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this message and exit.",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        help="Show the program's version number and exit.",
        version=f"warmac {_VERSION}",
    )

    # ======= Sub-Commands =======
    subparsers = parser.add_subparsers(dest="subparser", metavar="")

    # ------- Average Subcommand -------
    avg_parser = subparsers.add_parser(
        "average",
        help="Calculate the average platinum price of an item.",
        description=(
            "Calculate the average platinum price of an item. Able to find the median,"
            " mean, mode, and geometric mean of the specified item."
        ),
        formatter_class=lambda prog: CustomHelpFormat(
            prog=prog,
            max_help_position=default_width,
            # prog refers to the first argument passed in the command
            # line, which is the name of the file in this case.
        ),
        add_help=False,
        usage=(
            "warmac average [-s <stat>] [-p <platform>] [-t <days>] [-m | -r] [-b] "
            "[-v] item"
        ),
    )
    # ---- Average default settings ----

    # The statistic types that the average command can use
    avg_funcs: Final = ("median", "mean", "mode", "geometric")
    # The minimum time that str_to_int_bounds_check checks against
    min_time_range: Final = 1
    # The maximum time that str_to_int_bounds_check checks against
    max_time_range: Final = 60
    # NOTE: Potential to make function more "pure" by passing these two
    # variables in as parameters. A config file may help too.

    # Option characters used: s, p, t, m, r, b, v, h

    avg_parser.add_argument(
        "item",
        type=lambda s: s.strip(),
        help=(
            "Item to find the statistic of. If the item spans multiple words, please"
            " enclose the item within quotation marks."
        ),
    )

    avg_parser.add_argument(
        "-s",
        "--stats",
        default="median",
        type=lambda s: s.lower().strip(),
        choices=avg_funcs,
        help=(
            "Specifies which statistic to return; Can be one of "
            f"({', '.join(avg_funcs)}). (Default: median)"
        ),
        metavar="<stat>",
        dest="statistic",
    )

    avg_parser.add_argument(
        "-p",
        "--platform",
        default="pc",
        type=lambda s: s.lower().strip(),
        choices=platforms,
        help=(
            "Which platform to fetch the item's orders for. Must be one of "
            f"({', '.join(platforms)}). (Default: pc)"
        ),
        metavar="<platform>",
    )

    avg_parser.add_argument(
        "-t",
        "--timerange",
        default=DEFAULT_TIME,
        type=lambda x: str_to_int_bounds_check(x, min_time_range, max_time_range),
        help=(
            "Number of days to consider for calculating the average. Value given "
            "indicates how far back to start the statistic's calculation. Must be in "
            f"range [{min_time_range}, {max_time_range}]. (Default: {DEFAULT_TIME})"
        ),
        metavar="<days>",
        dest="timerange",
    )
    max_or_rad = avg_parser.add_mutually_exclusive_group()

    max_or_rad.add_argument(
        "-m",
        "--maxrank",
        action="store_true",
        help=(
            "Calculate the price statistic of the mod/arcane at its maximum rank "
            "instead of when it is unranked. Does nothing if used with an item that is "
            "not a mod. Cannot be used together with the --radiant option."
        ),
        dest="maxrank",
    )

    max_or_rad.add_argument(
        "-r",
        "--radiant",
        action="store_true",
        help=(
            "Calculate the price statistic of the relic at a radiant refinement instead"
            " of at an intact refinement. Does nothing if used with an item that is not"
            " a relic. Cannot be used together with the --maxrank option."
        ),
        dest="radiant",
    )

    avg_parser.add_argument(
        "-b",
        "--buyers",
        action="store_true",
        help=(
            "Calculate the price statistic of the item based on orders from buyers "
            "instead of orders from sellers."
        ),
        dest="use_buyers",
    )

    avg_parser.add_argument(
        "-d",
        "--detailed-report",
        action="store_true",
        help=(
            "Print additional market information about the requested item, along with "
            "the specified parameters."
        ),
        dest="detailed_report",
    )

    avg_parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this message and exit.",
    )

    # ---- Help Subcommand ----

    help_parser = subparsers.add_parser(
        "help",
        help="Show help for subcommands.",
        description=(
            "Show help for subcommands. A subcommand can be passed to receive help text"
            " on that subparser."
        ),
        formatter_class=lambda prog: CustomHelpFormat(
            prog=prog,
            max_help_position=default_width,
            # prog refers to the first argument passed in the command
            # line, which is the name of the file in this case.
        ),
        add_help=False,
        usage="warmac help subcommand",
    )
    _possible_subcommands = ("average", "help")

    help_parser.add_argument(
        "subcommand",
        type=lambda s: s.strip().lower(),
        choices=_possible_subcommands,
        nargs="?",
        help="Subcommand to show help for.",
        metavar="subcommand",
    )

    help_parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this message and exit.",
    )

    return parser


def handle_input(args: list[str] | None = None) -> argparse.Namespace:
    """
    Create a :py:class:`.WarMACParser` and parse arguments.

    Create :py:class:`.WarMACParser` object, parse command-line
    arguments, and return the parsed arguments as an
    :py:class:`argparse.Namespace` object. Exits early if only "warmac"
    is called or if the subcommand "help" is used.

    :param args: Substituted command line arguments, defaults to None
    :return: The parsed command-line arguments.
    """
    parser = _create_parser()
    parsed_args = parser.parse_args(args)
    if not parsed_args.subparser:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if parsed_args.subparser == "help":
        if parsed_args.subcommand:
            # This returns nothing. It exits after printing help
            parser.parse_args([parsed_args.subcommand, "--help"])
        parser.print_help(sys.stderr)
        sys.exit(0)

    return parsed_args
