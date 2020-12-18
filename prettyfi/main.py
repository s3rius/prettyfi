#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Small program to sort files according to the configuration
you provide. It can be any kind of command to run on your pc.
"""

import argparse
import subprocess
from pathlib import Path
from typing import Any, Dict, List

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
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        default=False,
        help="Recursively traverse directories",
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


def prettify_files(files: List[Path], config: SorterConfig) -> None:
    """
    Acrual prettier.
    If recursive option is set, it will traverse every dir recursively.
    """
    for file in files:
        if file.is_dir() and config.recursive:
            prettify_files(list(file.iterdir()), config)
            continue

        if rule := config.get_rule(file.name):
            print(f"formatting {file.expanduser()}")
            sort_file(file, rule)


def main() -> None:
    """
    Program entrypoint.
    """
    args = parse_args()
    sorter_conf = SorterConfig(**args)
    try:
        prettify_files(args["files"], sorter_conf)
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
