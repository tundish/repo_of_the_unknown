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
import dataclasses
from graphlib import TopologicalSorter
import uuid

from balladeer import Drama
from balladeer import Fruition
from balladeer import Speech

from rotu.puzzle import Puzzle


@dataclasses.dataclass(unsafe_hash=True)
class Strand:
    label: str
    puzzles: dataclasses.InitVar = []
    drama: dict[str, Drama] = dataclasses.field(default=None)
    sorter: TopologicalSorter = dataclasses.field(compare=False, default=None)

    def __post_init__(self, puzzles):
        self.make(puzzles=puzzles)

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

    def build(self, puzzles: list = [], *args, **kwargs) -> Generator[tuple[str, Puzzle]]:
        # Generate replicas of initial puzzles
        # TODO: replace uuid, etc
        yield from (
            (
                puzzle.names[0] if puzzle.names else puzzle.uid,
                puzzle.make(items=puzzle.items)
            )
            for puzzle in puzzles
        )

    def make(self, puzzles=[], **kwargs):
        puzzles = puzzles or self.drama.values()

        self.drama = dict(self.build(puzzles=puzzles))

        self.sorter = TopologicalSorter()
        for key, drama in self.drama.items():
            self.sorter.add(key, *drama.links)

        self.sorter.prepare()
        self._active = {i: self.drama.get(i) for i in self.sorter.get_ready()}
        return self
