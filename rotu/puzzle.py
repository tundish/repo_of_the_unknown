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
from graphlib import TopologicalSorter
import operator
import uuid

from balladeer import Drama
from balladeer import Entity
from balladeer import Fruition
from balladeer import WorldBuilder


@dataclasses.dataclass
class Strand:
    label: str
    puzzles: dataclasses.InitVar = []
    drama: dict[uuid.UUID, Drama] = dataclasses.field(default_factory=dict)
    sorter: TopologicalSorter = dataclasses.field(default_factory=TopologicalSorter)

    def __post_init__(self, puzzles):
        self.drama.update({i.uid: i for i in puzzles})
        self.sorter.prepare()

    @property
    def ready(self):
        done = [
            i for i in self.drama.values()
            if i.get_state(Fruition) in {
                Fruition.withdrawn, Fruition.defaulted, Fruition.cancelled, Fruition.completion
            }
        ]
        print(f"{done=}")
        return self.sorter.get_ready()


class Puzzle(Drama):

    class Item(Entity):
        states: tuple[str | enum.Enum] = dataclasses.field(default_factory=tuple)

    def __init__(self, *args, items: list[Item] = [], spots: dict = {}, **kwargs):
        self.items = tuple(items)
        self.spots = tuple(spots.items())
        super().__init__(*args, **kwargs)

    def build(self, world: WorldBuilder, **kwargs):
        for item in self.items:
            item.states, rules = {}, item.states
            for rule in rules:
                try:
                    state = operator.attrgetter(rule)(world.map)
                    item.set_state(state)
                except TypeError:
                    item.set_state(rule)
            yield item

