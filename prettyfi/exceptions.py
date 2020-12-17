#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic prettyfi exceptions.
"""


class UnknownRuleFormat(Exception):
    """
    Raised when one of the rules in config file has incorrect format
    """

    def __init__(self, line_num: int, line: str):
        """__init__.

        :param line_num: number of line with incorrect value
        :param line: line itself
        """
        super().__init__()
        self.line_num = line_num
        self.line = line


class CommandNotFound(Exception):
    """
    Raised when rule is applied but command from rule
    isn't found.
    """

    def __init__(self, rule: str):
        """__init__.

        :param rule: rule applied to file.
        """
        super().__init__()
        self.rule = rule
