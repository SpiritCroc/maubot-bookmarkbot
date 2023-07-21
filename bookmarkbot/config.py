# reminder - A maubot plugin that reacts to messages that match predefined rules.
# Copyright (C) 2019 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import List, Union, Dict, Any
import re

from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from mautrix.types import EventType

from .rule import Rule


class Config(BaseProxyConfig):
    rules: Dict[str, Rule]

    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("rules")

    def parse_data(self) -> None:
        self.rules = {}

        self.rules = {name: self._make_rule(name, rule)
                      for name, rule in self["rules"].items()}

    def _make_rule(self, name: str, rule: Dict[str, Any]) -> Rule:
        try:
            return Rule(source_rooms=set(rule.get("source_rooms", [])),
                        target_room=rule["target_room"],
                        reaction=rule["reaction"],
                        users=set(rule.get("users", [])))
        except Exception as e:
            raise ConfigError(f"Failed to load {name}") from e

class ConfigError(Exception):
    pass
