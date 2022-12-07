#! /usr/bin/env python3

"""Print an explanation of the arguments this script receives

Examples:

# Basic mode simply prints the arguments this script receives
$ argtest.py foo
foo
$ foo=bar
$ argtest.py $foo
bar
"""


import argparse
import sys
import unicodedata
import shlex

from rich.table import Table
from rich.console import Console


def arg_print(argv, escape=False):
    if escape:
        print(shlex.join(argv))
    else:
        print(" ".join(argv))


def _arg_table(arg: str):
    """Display a single argument (string) in a table"""
    arg_table = Table(title=arg, safe_box=False)
    arg_table.add_column("Char.")
    arg_table.add_column("Repr.")
    arg_table.add_column("Name")
    for c in arg:
        arg_table.add_row(c, repr(c), unicodedata.name(c))
    return arg_table


def argv_table(argv: list[str]):
    """Display each argument in argv in a table"""
    argv_str = " ".join(argv)
    grid = Table(
        show_header=False,
        show_footer=False,
        show_lines=False,
        show_edge=False,
        box=None,
        safe_box=False,
    )
    for arg in argv:
        grid.add_column(justify="center")
    grid.add_row(*[_arg_table(arg) for arg in argv])

    print(f"Received {len(argv)} arguments:\n{argv_str}")
    print()
    Console().print(grid)


def main():
    args = parse_args()
    # By default, use the full sys.argv. But we also provide the option to ignore
    # "self" args -- script name, and flags for this script
    argv = sys.argv if args.include_own_args else args.args
    if args.verbose:
        argv_table(argv=argv)
    else:
        arg_print(argv=argv)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("args", nargs="*")
    parser.add_argument("-i", "--include-own-args", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
