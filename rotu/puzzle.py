#!/usr/bin/env python
# encoding: utf8

# Copyright 2024 D E Haynes

# This file is part of rotu.
#
# Rotu is free software: you can redistribute it and/or modify it under the terms of the
# GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# Rotu is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with Rotu.
# If not, see <https://www.gnu.org/licenses/>.

from collections.abc import Generator
import copy
import dataclasses
import enum
import operator
import uuid

from balladeer import Drama
from balladeer import Entity
from balladeer import Loader
from balladeer import MapBuilder


class Puzzle(Drama):

    @dataclasses.dataclass(kw_only=True, unsafe_hash=True)
    class Item(Entity):
        init: list[str | enum.Enum] = dataclasses.field(default_factory=list, compare=False)

    def __init__(self, *args, items: list[Item] = [], spots: dict = {}, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = items
        self.spots = tuple(spots.items())

    @property
    def focus(self):
        return next((reversed(sorted(self.world.typewise["Focus"], key=operator.attrgetter("state")))), None)

    def scripts(self, assets):
        return [i for i in assets if isinstance(i, Loader.Scene)]

    def build(self, m: MapBuilder, items: list[Item], **kwargs) -> Generator[Item]:
        for item in self.items:
            rv = dataclasses.replace(item, uid=uuid.uuid4())
            for rule in item.init:
                try:
                    state = operator.attrgetter(rule)(m)
                    rv.set_state(state)
                except AttributeError:
                    # No map supplied
                    continue
                except TypeError:
                    rv.set_state(rule)
            yield rv

    def make(self, m: MapBuilder=None, items=[], **kwargs):
        self.items = tuple(self.build(m, items=items))
        return self
