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
import enum
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
from balladeer import Traffic
from balladeer import WorldBuilder
from busker.stager import Stager

import rotu
from rotu.drama import Exploration
from rotu.drama import Interaction


class StoryWeaver(StoryBuilder):

    @staticmethod
    def initialize_puzzle(realm, name):
        self.entities = list(self.build(**kwargs))
        self.typewise = Grouping.typewise(self.entities)

    @staticmethod
    def item_state(spec: str | int, pool: list[enum.Enum], default=0):
        try:
            name, value = spec.lower().split(".")
        except AttributeError:
            return spec

        lookup = {cls.__name__.lower(): cls for cls in pool + [Fruition, Traffic]}

        try:
            cls = lookup[name]
            return cls[value]
        except KeyError as e:
            return default

    @staticmethod
    def item_type(name: str, default=Entity):
        name = name or ""
        return {
            cls.__name__.lower(): cls for cls in (Drama, Entity, Exploration, Interaction, Transit)
        }.get(name.lower(), default)

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

        self.drama: dict[tuple[str, str], Drama] = {
            (realm, name): self.build_drama(realm, name) for (realm, name) in self.stager.active
        } or {(None, None): Drama(*speech, config=self.config, world=world)}

    def __deepcopy__(self, memo):
        speech = copy.deepcopy(self.speech, memo)
        config = copy.deepcopy(self.config, memo)
        assets = copy.deepcopy(self.assets, memo)
        rv = self.__class__(*speech, config=config, assets=assets)
        return rv

    def build_drama(self, realm: str, name: str):
        puzzle = self.stager.gather_puzzle(realm, name)
        drama_type = self.item_type(puzzle.get("type"), default=Drama)
        drama = drama_type(
            *self.speech,
            config=self.config,
            world=self.world,
            name=puzzle.get("name"),
            type=drama_type.__name__,
            links=set(puzzle.get("chain", {}).keys()),
            sketch=puzzle.get("sketch", ""),
            aspect=puzzle.get("aspect", ""),
            revert=puzzle.get("revert", ""),
        )
        self.drama[(realm, name)] = drama

        for item in puzzle.get("items"):
            item_type = self.item_type(item.get("type"))
            pool = [self.world.map.home, self.world.map.into, self.world.map.exit, self.world.map.spot]
            states = [self.item_state(i, pool=pool) for i in item.get("states", [])]
            entity = item_type(
                name=item.get("name"),
                type=item_type.__name__,
                links={puzzle.get("name")},
                sketch=item.get("sketch", ""),
                aspect=item.get("aspect", ""),
                revert=item.get("revert", ""),
            ).set_state(*states)

            if item_type is Transit:
                self.world.map.transits.append(entity)
            else:
                self.world.entities.append(entity)

        self.world.typewise = Grouping.typewise(self.world.entities)


class Story(StoryWeaver):

    @property
    def context(self):
        drama = [self.drama[(realm, name)] for realm, name in self.stager.active] or list(self.drama.values())
        return next((reversed(sorted(drama, key=operator.attrgetter("state")))), None)

    def turn(self, *args, **kwargs):
        for realm, name in self.stager.active:
            try:
                drama = self.drama[(realm, name)]
            except KeyError:
                drama = self.build_drama(realm, name)

            # self.assertEqual(events, [("rotu", "b", "Fruition.inception")])
            if state := drama.get_state(Fruition) in {
                Fruition.withdrawn, Fruition.defaulted, Fruition.cancelled, Fruition.completion
            }:
                events = list(self.stager.terminate(realm, name, state.value))
                print(f"{events=}")

        try:
            self.context.interlude(*args, **kwargs)
        except AttributeError:
            warnings.warn("Turn exhausted context")
        return self
