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
from typing import Type, Tuple, Dict
import time

from attr import dataclass

from mautrix.types import EventType, MessageType, UserID, RoomID
from mautrix.util.config import BaseProxyConfig

from maubot import Plugin, MessageEvent
from maubot.handlers import event

from .config import Config, ConfigError


class BookmarkBot(Plugin):

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    async def start(self) -> None:
        await super().start()
        self.on_external_config_update()

    def on_external_config_update(self) -> None:
        self.config.load_and_update()
        try:
            self.config.parse_data()
        except ConfigError:
            self.log.exception("Failed to load config")

    @event.on(EventType.REACTION)
    async def event_handler(self, evt: MessageEvent) -> None:
        if evt.sender == self.client.mxid:
            return
        for name, rule in self.config.rules.items():
            match = rule.match(evt)
            self.log.info(f"a match {match}")
            if match is not None:
                try:
                    resolved = await self.client.get_event(evt.room_id, evt.content.relates_to.event_id)
                    await rule.execute(evt, resolved)
                except Exception:
                    self.log.exception(f"Failed to execute {name} in {evt.room_id}")
                return
