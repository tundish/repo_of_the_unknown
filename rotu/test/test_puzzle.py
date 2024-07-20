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

from balladeer import Grouping
from balladeer import StoryBuilder
from balladeer import MapBuilder
from balladeer import WorldBuilder

from rotu.puzzle import Puzzle
from rotu.puzzle import Strand


class StrandTests(unittest.TestCase):

    def test_default_item(self):
        r = Puzzle.Item()
        self.assertFalse(r.states)
        r.set_state(1)
        self.assertEqual(r.states, {"int": 1})

    def test_default_strand(self):
        self.assertRaises(TypeError, Strand)
        s = Strand(label="test")
        self.assertEqual(s.drama, [])

    def test_simple(self):
        s = Strand(label="test", drama=[Puzzle(name="test")])
        self.assertEqual(s.drama[0].items, tuple())
        self.assertEqual(s.drama[0].spots, tuple())

    @unittest.skip("TODO")
    def test_base_map(self):
        self.fail()


class TurnTests(unittest.TestCase):

    class Map(MapBuilder):
        pass

    class World(WorldBuilder):
        def build(self, **kwargs):
            return
            yield

    class Story(StoryBuilder):
        def turn(self, *args, **kwargs):
            self.world.typewise = Grouping.typewise(self.world.entities)
            return super().turn(*args, **kwargs)

    def test_simple_puzzle(self):
        puzzle = Puzzle(
            name="single spot",
            spots={
                "inventory": ["inventory", "carrying"],
            },
            items=(
                Puzzle.Item(states=("home.inventory",)),
            ),
        )
        m = self.Map(spots=puzzle.spots)
        world = self.World(map=m, assets={})

        rv = list(puzzle.build(world=world))
        self.assertEqual(len(rv), len(puzzle.items), rv)

        for n, entity in enumerate(rv):
            with self.subTest(n=n, entity=entity):
                self.assertEqual(entity.get_state(world.map.home).label, "inventory")
                self.assertEqual(entity.get_state("Home").label, "inventory")

    def test_simple_strand(self):
        strands = [
            Strand(
                label="single test strand",
                drama=[
                    Puzzle(
                        name="single spot",
                        spots={
                            "inventory": ["inventory", "carrying"],
                        }
                    )
                ]
            )
        ]
        world = self.World(map=self.Map(spots={}), assets={})
        story = self.Story("Test", world=world)

        self.assertEqual(len(story.drama), 1)
        self.assertFalse(story.world.specs)
        self.assertFalse(story.world.statewise)
        self.assertFalse(story.world.typewise)

        self.assertTrue(issubclass(story.world.map.spot, enum.Enum))
        self.assertFalse(list(story.world.map.spot))

        story.turn()
