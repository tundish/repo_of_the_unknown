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

from collections import deque
from collections.abc import Generator
import copy
import itertools
import operator
import random
import warnings

from balladeer import Entity
from balladeer import Fruition
from balladeer import Grouping
from balladeer import MapBuilder
from balladeer import Speech
from balladeer import StoryBuilder
from balladeer import Transit
from balladeer import WorldBuilder

import rotu
from rotu.drama import Interaction
from rotu.puzzle import Puzzle
from rotu.strand import Strand


class StoryWeaver(StoryBuilder):

    @staticmethod
    def gather_spots(strands: list[Strand]) -> dict[str, list]:
        items = sorted(item for strand in strands for puzzle in strand.drama.values() for item in puzzle.spots)
        return {
            g: list(itertools.chain.from_iterable([i[1] for i in v]))
            for g, v in itertools.groupby(
                sorted(item for strand in strands for puzzle in strand.drama.values() for item in puzzle.spots.items()),
                key=operator.itemgetter(0)
            )
        }

    def __init__(
        self,
        *speech: tuple[Speech],
        config=None,
        assets: Grouping = Grouping(list),
        strands: list[Strand] = None,
        **kwargs,
    ):
        kwargs["strands"] = strands
        kwargs["speech"] = speech
        super().__init__(config=config, assets=assets, **kwargs)

    def __deepcopy__(self, memo):
        speech = copy.deepcopy(self.speech, memo)
        config = copy.deepcopy(self.config, memo)
        assets = copy.deepcopy(self.assets, memo)
        strands = [strand.make(strand.puzzles.copy()) for strand in self.strands]
        rv = self.__class__(*speech, config=config, assets=assets, strands=strands)
        return rv

    def build(self, *, speech: tuple[type], strands: list[Strand] = None, **kwargs) -> Generator[Strand]:
        if strands:
            yield from (strand.make(strand.puzzles) for strand in strands)
        else:
            yield Strand.default(*speech)

    def make(self, speech: tuple[Speech] = (), strands: list[Strand] = None, **kwargs):
        spots = self.gather_spots(strands or [])
        m = Map(spots=spots, config=self.config)

        self.strands = deque(self.build(speech=speech, strands=strands))
        self.world = World(map=m, config=self.config, assets=self.assets, strands=self.strands)

        return self.turn(**kwargs)


class Map(MapBuilder):
    def __init__(self, spots: dict, config=None, strands=None, **kwargs):
        self.strands = strands
        super().__init__(spots, config=config, **kwargs)

    def build(self, awoken: list[Puzzle] = [], **kwargs) -> Generator[Transit]:
        "Generate new map transits for freshly active puzzles."
        for puzzle in awoken:
            for item in puzzle.items:
                if "Transit" in item.types:
                    yield item


class World(WorldBuilder):
    def __init__(self, map: MapBuilder=None, config: dict  = None, assets: Grouping = None, strands=None, **kwargs):
        self.strands = strands
        super().__init__(map, config, assets=assets, **kwargs)

    """
    def __deepcopy__(self, memo):
        rv = self.__class__(
            map=copy.deepcopy(self.map),
            config=self.config and self.config.copy(),
            assets=self.assets and self.assets.copy(),
            strands=self.strands and copy.deepcopy(self.strands)
        )
        print(f"{self.__class__.__name__} deepcopy {memo}")
        return rv
    """

    def build(self, awoken: list[Puzzle] = [], **kwargs) -> Generator[Entity]:
        "Generate new world entities for freshly active puzzles."
        for puzzle in awoken:
            for item in puzzle.build(self.map, items=puzzle.items):
                if "Transit" not in item.types:
                    yield item


class Story(StoryWeaver):

    @property
    def context(self):
        active = [puzzle for strand in self.strands for puzzle in strand.active]
        if active:
            self.strands.rotate(-1)
            rv = random.choice(active)
            rv.world = self.world
        else:
            rv = next(reversed(sorted(self.drama, key=operator.attrgetter("state"))), None)
        return rv

    def turn(self, *args, **kwargs):
        active = [puzzle for strand in self.strands for puzzle in strand.active]
        awoken = [puzzle for puzzle in active if puzzle.get_state(Fruition) is None]
        self.world.map.transits.extend(list(self.world.map.build(awoken=awoken)))
        self.world.entities.extend(list(self.world.build(awoken=awoken)))
        self.world.typewise = Grouping.typewise(self.world.entities)

        for puzzle in awoken:
            puzzle.set_state(Fruition.inception)

        try:
            self.context.interlude(*args, **kwargs)
        except AttributeError:
            warnings.warn("Turn exhausted context")
        return self
