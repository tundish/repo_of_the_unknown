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

from balladeer import Drama
from balladeer import Entity
from balladeer import Fruition
from balladeer import Grouping
from balladeer import Loader
from balladeer import MapBuilder
from balladeer import Speech
from balladeer import StoryBuilder
from balladeer import Transit
from balladeer import WorldBuilder
from busker.stager import Stager

import rotu
from rotu.drama import Interaction


class StoryWeaver(StoryBuilder):

    def __init__(
        self,
        *speech: tuple[Speech],
        config=None,
        assets: Grouping = Grouping(list),
        **kwargs,
    ):
        staging = [i.data for i in assets[Loader.Staging]]
        self.stager = Stager(staging).prepare()

        spots = self.stager.gather_state()
        m = MapBuilder(spots=spots)
        world = WorldBuilder(map=m, config=config, assets=assets)
        super().__init__(*speech, config=config, assets=assets, world=world, **kwargs)

    def __deepcopy__(self, memo):
        speech = copy.deepcopy(self.speech, memo)
        config = copy.deepcopy(self.config, memo)
        assets = copy.deepcopy(self.assets, memo)
        rv = self.__class__(*speech, config=config, assets=assets)
        return rv


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

    def make(self, **kwargs):
        self.drama = dict()
        return self

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
