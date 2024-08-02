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
        return {
            k: [i[1] for i in v]
            for k, v in itertools.groupby(
                sorted(spot for strand in strands for spot in strand.spots),
                key=operator.itemgetter(0)
            )
        }

    """
    def __init__(
        self,
        *speech: tuple[Speech],
        config=None,
        assets: Grouping = Grouping(list),
        strands: list[Strand] = None,
        **kwargs,
    ):
        super().__init__(*speech, config=config, assets=assets, world=world, **kwargs)
        self.strands = deque(copy.deepcopy(strands) or [Strand.default(*speech)])
        spots = self.spots(self.strands)
        m = Map(spots=spots, config=config, strands=self.strands)
        world = World(map=m, config=config, assets=assets, strands=self.strands)
    """

    def __deepcopy__(self, memo):
        # TODO: Does Puzzle.build do a copy into each entity?
        config = copy.deepcopy(self.config, memo)
        w = copy.deepcopy(self.world)
        rv = self.__class__(*self.speech, config=config, assets=self.assets, strands=self.strands, world=w)
        rv.world.entities = copy.deepcopy(rv.world.entities)
        rv.world.map.transits = copy.deepcopy(rv.world.map.transits)
        return rv

    def build(self, *speech: tuple[type], strands, **kwargs) -> Generator[Strand]:
        if strands:
            yield from (strand.make() for strand in strands)
        else:
            yield Strand.default(*speech)

    def make(self, strands: list[Strand] = [], **kwargs):
        spots = self.gather_spots(strands)
        m = Map(spots=spots, config=self.config)
        self.strands = deque(self.build(*self.speech, strands=strands))
        active = [puzzle for strand in self.strands for puzzle in strand.active]
        self.world = World(map=m, config=self.config, assets=self.assets, strands=self.strands)
        return self

    @property
    def context(self):
        return next((reversed(sorted(self.drama, key=operator.attrgetter("state")))), None)

    def action(self, text: str, *args, **kwargs):
        drama = self.context
        actions = drama.actions(
            text,
            context=self.director,
            ensemble=drama.ensemble,
            prefix=drama.prefixes[0],
        )
        fn, args, kwargs = drama.pick(actions)
        if not fn:
            return None

        try:
            drama.speech.extend(drama(fn, *args, **kwargs))
        except Exception as e:
            warnings.warn(e)

        return fn, args, kwargs

    def turn(self, *args, **kwargs):
        self.context.interlude(*args, **kwargs)
        return self

    def __enter__(self):
        drama = self.context

        # Director selection
        scripts = drama.scripts(self.assets.get(Loader.Scene, []))
        scene, specs, roles = self.director.selection(scripts, drama.ensemble)
        assert isinstance(scene, Loader.Scene), f"{type(scene)} is not a Scene"

        # TODO: Entity aspects

        # Collect waiting speech
        try:
            speech = [drama.speech.popleft()]
        except AttributeError:
            speech = drama.speech.copy()
            drama.speech.clear()
        except IndexError:
            speech = []

        blocks = list(self.director.rewrite(scene, roles, speech))

        rv = Turn(scene, specs, roles, speech, blocks, self.director.notes.copy())

        # Directive handlers
        n = 0
        for block, (key, note) in zip(blocks, self.director.notes.items()):
            for m in note.maps:
                for (action, entity, entities) in m.get("directives", []):
                    method = getattr(drama, f"{drama.prefixes[1]}{action}", None)
                    if isinstance(method, Callable):
                        try:
                            method(entity, *entities, identifier=key, **rv._asdict())
                        except Exception as e:
                            warnings.warn(f"Error in directive handler {method}")
                            warnings.warn(str(e))
                    n += 1

        drama.set_state(Detail.none)
        return rv

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.director.notes.clear()
        return False

class Map(MapBuilder):
    def __init__(self, spots: dict, config=None, strands=None, **kwargs):
        self.strands = strands
        super().__init__(spots, config=config, **kwargs)

    def build(self, active: list[Puzzle] = [], **kwargs) -> Generator[Transit]:
        "Generate new map transits whenever a puzzle becomes freshly active."
        for puzzle in active:
            if puzzle.get_state(Fruition) is None:
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

    def build(self, **kwargs) -> Generator[Entity]:
        "Generate new world entities whenever a puzzle becomes freshly active."
        active = [puzzle for strand in self.strands for puzzle in strand.active]
        for puzzle in active:
            if puzzle.get_state(Fruition) is None:
                for item in puzzle.build(self.map):
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
        if any(puzzle.get_state(Fruition) is None for puzzle in active):
            self.world.map.transits.extend(list(self.world.map.build(strands=self.strands)))
            self.world.entities.extend(list(self.world.build(strands=self.strands)))

        for puzzle in active:
            if puzzle.get_state(Fruition) is None:
                puzzle.set_state(Fruition.inception)

        """
        self.world.typewise = Grouping.typewise(self.world.entities)
        try:
            self.context.interlude(*args, **kwargs)
        except AttributeError:
            warnings.warn("Turn exhausted context")
        """
        return self
