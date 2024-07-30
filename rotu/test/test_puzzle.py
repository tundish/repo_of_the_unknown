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

import enum
import unittest

from balladeer import Entity
from balladeer import Fruition
from balladeer import Grouping
from balladeer import StoryBuilder
from balladeer import Traffic
from balladeer import MapBuilder
from balladeer import WorldBuilder

from rotu.main import Story
from rotu.puzzle import Puzzle
from rotu.strand import Strand


class PuzzleTests(unittest.TestCase):

    class Map(MapBuilder):
        pass

    class World(WorldBuilder):
        specs = set()
        def build(self, **kwargs):
            return
            yield

    class Story(StoryBuilder):
        def turn(self, *args, **kwargs):
            self.world.typewise = Grouping.typewise(self.world.entities)
            return super().turn(*args, **kwargs)

    def test_default_item(self):
        r = Puzzle.Item()
        self.assertFalse(r.states)
        r.set_state(1)
        self.assertEqual(r.states, {"int": 1})

    def test_simple_puzzle(self):
        puzzle = Puzzle(
            name="single spot",
            spots={
                "inventory": ["inventory", "carrying"],
            },
            items=(
                Puzzle.Item(init=("home.inventory", Fruition.inception)),
            ),
        )
        m = self.Map(spots=puzzle.spots)
        world = self.World(map=m, assets={})

        rv = list(puzzle.build(world.map))
        self.assertEqual(len(rv), len(puzzle.items), rv)
        self.assertIsInstance(puzzle.names[0], str)

        entity = rv[0]
        self.assertEqual(entity.get_state(world.map.home).label, "inventory")
        self.assertEqual(entity.get_state("Home").label, "inventory")
        self.assertEqual(entity.get_state("Fruition"), Fruition.inception)
