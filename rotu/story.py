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
import copy
import itertools
import operator
import random
import warnings

from balladeer import Fruition
from balladeer import Grouping
from balladeer import MapBuilder
from balladeer import Speech
from balladeer import StoryBuilder
from balladeer import WorldBuilder

import rotu
from rotu.drama import Interaction
from rotu.puzzle import Puzzle
from rotu.puzzle import Strand


class StoryWeaver(StoryBuilder):

    @staticmethod
    def spots(strands: list[Strand]) -> dict[str, list]:
        return {
            k: [i[1] for i in v]
            for k, v in itertools.groupby(
                sorted(spot for strand in strands for spot in strand.spots),
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
        self.strands = deque(strands or [Strand.default(*speech)])
        super().__init__(*speech, config=config, assets=assets, world=None)

    def __deepcopy__(self, memo):
        return self.__class__(*self.speech, config=self.config, assets=self.assets, strands=self.strands)

    def make(self, **kwargs):
        spots = self.spots(self.strands)
        m = MapBuilder(spots=spots)
        self.world = WorldBuilder(map=m, config=self.config, assets=self.assets)
        return self.turn()


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
        for puzzle in active:
            if puzzle.get_state(Fruition) is None:
                puzzle.set_state(Fruition.inception)
                for item in puzzle.items:
                    if "Transit" in item.types:
                        self.world.map.transits.append(item)
                    else:
                        self.world.entities.append(item)
        self.world.typewise = Grouping.typewise(self.world.entities)
        try:
            self.context.interlude(*args, **kwargs)
        except AttributeError:
            warnings.warn("Turn exhausted context")
        return self
