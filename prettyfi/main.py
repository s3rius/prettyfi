#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Small program to sort files according to the configuration
you provide. It can be any kind of command to run on your pc.
"""

import argparse
import subprocess
from pathlib import Path
from typing import Any, Dict

from prettyfi.config import SorterConfig
from prettyfi.exceptions import CommandNotFound, UnknownRuleFormat


def parse_args() -> Dict[str, Any]:
    """
    parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Simple utility to make your files prettier."
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        dest="config",
        default=None,
        help="path to configuration file",
    )
    parser.add_argument("files", type=Path, nargs="+", help="Files to sort")

    return {
        key: val for key, val in parser.parse_args().__dict__.items() if val is not None
    }


def sort_file(file: Path, rule: str) -> None:
    """
    Actually call the command on file.
    """
    try:
        subprocess.call(rule.format(file=str(file)), shell=True)
    except FileNotFoundError as exc:
        raise CommandNotFound(rule) from exc


def main() -> None:
    """
    Program entrypoint.
    """
    args = parse_args()
    sorter_conf = SorterConfig(**args)
    try:
        sorter_conf.startup_actions()
        for file in args["files"]:
            if rule := sorter_conf.get_rule(file.name):
                sort_file(file, rule)
            else:
                print(f"I don't know what to do with {file.name}")
    except UnknownRuleFormat as exception:
        print("Unknown rule format on line " f"{exception.line_num}: {exception.line}")
        print("Rule format is:")
        print('\t.ext $ program_to_run "{file}"')
    except CommandNotFound as exception:
        print("Program from the rule not installed.")
        print(f"RULE: {exception.rule}")
    except KeyboardInterrupt:
        print("Command interrupted.")


if __name__ == "__main__":
    main()
