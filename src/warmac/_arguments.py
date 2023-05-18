"""
warmac._arguments 1.5.8
~~~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

File that contains the argument parser for WarMac.
For information on the main program, please see main.py

Date of Creation: January 22, 2023
Date Last Modified: May 13, 2023
Version of Python required for module: >=3.6.0
""" # noqa: D205,D400

import argparse as argp
import shutil
from statistics import harmonic_mean, mean, median, mode

_AVG_FUNCTIONS = {
    "mean": mean,
    "median": median,
    "mode": mode,
    "harmonic": harmonic_mean,
}
_DESCRIPTION = "A program to fetch the average market cost of an item in Warframe."
_HELP_MIN_WIDTH = 100
_PLATFORMS = ("pc", "ps4", "xbox", "switch")
_UPPER_TIME_BOUNDS = 750
_VERSION = "1.5.8"

class _WarMACParser(argp.RawTextHelpFormatter, argp.RawDescriptionHelpFormatter):
    """Extends argparse.RawDescriptionHelpFormatter and argparse.RawTextHelpFormatter."""

def _int_checking(inp: str) -> int:
    """
    Take string and check if it's an integer greater than 0 and less than 750.

    :param inp: argument parser's time range value to be checked against
    :type inp: str
    :raises ArgumentTypeError: if input is a string, or if inp <= 0, or if input >= _UPPER_BOUNDS
    :return: returns inp if inp > 0 and if inp < _UPPER_BOUNDS
    :rtype: int
    """
    try:
        new_inp = int(inp)
    except ValueError:
        msg = "Input mismatch error. Please use an integer greater than 0."
        raise argp.ArgumentTypeError (msg) from None
    if new_inp <= 0 or new_inp >= _UPPER_TIME_BOUNDS:
        msg = "Invalid integer. Please use an integer greater than 0."
        raise argp.ArgumentTypeError (msg)
    return new_inp

def _create_parser() -> argp.ArgumentParser:
    """
    Return ArgumentParser with the appropriate documentation and functionality.

    :return: ArgumentParser with appropriate documentation and functionality
    :rtype: argparse.ArgumentParser
    """
    width = min(_HELP_MIN_WIDTH, shutil.get_terminal_size().columns - 2)
    parser = argp.ArgumentParser(formatter_class=lambda prog:
                                 _WarMACParser(prog, max_help_position=width),
                                 description=_DESCRIPTION, add_help=False)

    parser.add_argument("-h", "--help", action="help", help="Show this message and exit.")
    parser.add_argument("--version", action="version", help="Show the program's version number"
                        " and exit.", version="%(prog)s" f" {_VERSION}")

    # Optional Arguments
    parser.add_argument("-a", "--avg_type", default="mean", type=lambda s: s.lower().strip(),
                        choices=_AVG_FUNCTIONS, metavar="", help="Specifies the type of average to"
                        f" return; Can be one of {', '.join(_AVG_FUNCTIONS)}. (Default: mean)")

    parser.add_argument("-b", "--buyers", action="store_true", help="Take the average platinum"
                        " price from buyer orders instead of seller orders.", dest="use_buyers")

    parser.add_argument("-e", "--extra-info", action="store_true", help="Prints the highest and"
                        " lowest prices in the order list, as well as the number of orders that"
                        " were fetched.", dest="extra")

    parser.add_argument("-p", "--platform", default="pc", type=lambda s: s.lower().strip(),
                        choices=_PLATFORMS, metavar="", help="Specifies which platform to fetch"
                        f" orders for; Can be one of {', '.join(_PLATFORMS)}. (Default: pc)")

    parser.add_argument("-r", "--range", default=60, type=_int_checking, help="Specifies in days"
                        " how old the retrieved orders can be. Must be greater than 0 and less"
                        " than 750. (Default: 60)", metavar="", dest="time_range")

    parser.add_argument("-v", "--verbose", action="store_true", help="Prints the average price of"
                        " the item, alongside a short message for the user.", dest="verbose")

    # Positional Arguments
    parser.add_argument("item", type=lambda s: s.lower().strip(), help="the item to search for")
    return parser
