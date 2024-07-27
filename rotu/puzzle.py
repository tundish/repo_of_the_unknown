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
import warnings

from balladeer import Drama
from balladeer import Entity
from balladeer import Fruition
from balladeer import WorldBuilder
from balladeer import Speech


@dataclasses.dataclass
class Strand:
    label: str
    puzzles: dataclasses.InitVar = []
    drama: dict[str, Drama] = dataclasses.field(default_factory=dict)
    sorter: TopologicalSorter = dataclasses.field(default_factory=TopologicalSorter)

    def __post_init__(self, puzzles):
        self.drama.update({i.names[0] if i.names else i.uid: i for i in puzzles})

        for key, drama in self.drama.items():
            self.sorter.add(key, *drama.links)

        self.sorter.prepare()
        self._active = {i: self.drama.get(i) for i in self.sorter.get_ready()}

    @classmethod
    def default(cls, *speech: tuple[Speech], label="init"):
        return cls(
            label=label,
            puzzles=[
                Puzzle(
                    *speech,
                    spots={"here": ["here"]},
                    items=[Puzzle.Item(type="Focus", init=("spot.here",))]
                )
            ]
        )

    @property
    def active(self):
        for key in list(self._active.keys()):
            try:
                if self.drama[key].get_state(Fruition) in {
                    Fruition.withdrawn, Fruition.defaulted, Fruition.cancelled, Fruition.completion
                }:
                    del self._active[key]
                    self.sorter.done(key)
            except (AttributeError, KeyError, ValueError):
                continue

        self._active.update({i: self.drama.get(i) for i in self.sorter.get_ready()})
        return list(self._active.values())

    @property
    def spots(self) -> list[tuple[str, str]]:
        return [
            (name, term)
            for drama in self.drama.values()
            for name, terms in drama.spots
            for term in terms
        ]


class Puzzle(Drama):

    @dataclasses.dataclass(kw_only=True, unsafe_hash=True)
    class Item(Entity):
        init: tuple[str | enum.Enum] = dataclasses.field(default_factory=tuple, compare=False)

    def __init__(self, *args, items: list[Item] = [], spots: dict = {}, **kwargs):
        self.items = tuple(items)
        self.spots = tuple(spots.items())
        super().__init__(*args, **kwargs)

    def build(self, world: WorldBuilder, **kwargs):
        for item in self.items:
            item.init, rules = {}, item.init
            for rule in rules:
                try:
                    state = operator.attrgetter(rule)(world.map)
                    item.set_state(state)
                except TypeError:
                    item.set_state(rule)
            yield item

    @property
    def focus(self):
        return next((reversed(sorted(self.world.typewise["Focus"], key=operator.attrgetter("state")))), None)

