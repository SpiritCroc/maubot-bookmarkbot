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
from typing import Optional, Match, Dict, List, Set, Union, Any

from attr import dataclass
from jinja2 import Template as JinjaTemplate

from mautrix.types import RoomID, UserID, EventType

from maubot import MessageEvent

from .template import Template


@dataclass
class Rule:
    source_rooms: Set[RoomID]
    target_room: RoomID
    users: Set[UserID]
    reaction: str

    def match(self, evt: MessageEvent) -> Optional[Match]:
        if len(self.source_rooms) > 0 and evt.room_id not in self.source_rooms:
            return None
        if len(self.users) > 0 and evt.sender not in self.users:
            return None
        match = self.reaction == evt.content.relates_to.key
        if match:
            return match
        return None

    async def execute(self, evt: MessageEvent, relates_evt: MessageEvent) -> None:
        content = relates_evt.content
        await evt.client.send_message_event(self.target_room, EventType.ROOM_MESSAGE, content)
