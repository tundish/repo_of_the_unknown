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

import dataclasses
import enum

from balladeer import Drama
from balladeer import Entity


@dataclasses.dataclass
class Strand:
    label: str
    drama: list[Drama] = dataclasses.field(default_factory=list)


class Puzzle(Drama):

    class Item(Entity):
        states: tuple[str | enum.Enum] = dataclasses.field(default_factory=tuple)

    def __init__(self, *args, items: list[Item] = [], spots: dict = {}, **kwargs):
        self.items = tuple(items)
        self.spots = tuple(spots.items())
        super().__init__(*args, **kwargs)

    def build(self, **kwargs):
        yield
        return

