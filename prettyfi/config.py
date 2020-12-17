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
}

default_config_path = Path("~/.prettyfirc")


class SorterConfig(BaseModel):
    """
    Sorter settings
    """

    config: Path = Field(default_config_path)
    rules: Dict[str, str] = default_rules

    def get_rule(self, filename: str) -> Optional[str]:
        """
        Find rule by filename.
        """
        for pattern, rule in self.rules.items():
            if filename.endswith(pattern):
                return rule
        return None

    def startup_actions(self) -> None:
        if self.config == default_config_path and not self.config.expanduser().exists():
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
