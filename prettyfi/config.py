#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Default configuration for several filetypes.
"""
from pathlib import Path
from typing import Dict, Optional

from pydantic import BaseConfig, BaseModel, Field

from prettyfi.exceptions import UnknownRuleFormat

default_rules = {
    ".py": 'black "{file}" && isort "{file}"',
    ".toml": 'toml-sort --in-place "{file}"',
    ".json": 'jq . "{file}" > "{file}_tmp" && mv "{file}_tmp" "{file}"',
    ".sql": 'sqlformat -k upper "{file}" > "{file}_tmp" && mv "{file}_tmp" "{file}"',
    ".xml": (
        'xmllint --format "{file}" --output "{file}_tmp" && mv "{file}_tmp" "{file}"'
    ),
    ".tf": 'terraform fmt "{file}"',
    ".rs": 'rustfmt --edition 2018 "{file}"',
    ".md": 'mdformat "{file}"',
}

default_config_path = Path("~/.prettyfirc").expanduser()


class SorterConfig(BaseModel):
    """
    Sorter settings
    """

    config: Path = Field(default_config_path)
    rules: Dict[str, str] = default_rules
    recursive: bool = False

    def get_rule(self, filename: str) -> Optional[str]:
        """
        Find rule by filename.
        """
        for pattern, rule in self.rules.items():
            if filename.endswith(pattern):
                return rule
        return None

    def startup_actions(self) -> None:
        """
        Actions to collect user rules and create
        default config file if it not exits.
        """
        if self.config == default_config_path and not self.config.exists():
            with self.config.expanduser().open("w") as f:
                for pattern, rule in default_rules.items():
                    f.write(f"{pattern} $ {rule}\n")
        self.update_rules()

    def update_rules(self) -> None:
        """
        Parse and apply your custom rules to the config.
        """
        for index, line in enumerate(self.config.expanduser().open()):
            try:
                pattern, command = line.strip().split("$")
                self.rules[pattern.strip()] = command.strip()
            except ValueError:
                raise UnknownRuleFormat(index + 1, line.strip())

    class Config(BaseConfig):
        orm_mode = True
