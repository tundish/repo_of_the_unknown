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

from balladeer import Fruition
from balladeer import Grouping
from balladeer import StoryBuilder
from balladeer import MapBuilder
from balladeer import WorldBuilder

from rotu.main import Story
from rotu.puzzle import Puzzle
from rotu.puzzle import Strand


class PuzzleTests(unittest.TestCase):

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
                Puzzle.Item(states=("home.inventory", Fruition.inception)),
            ),
        )
        m = self.Map(spots=puzzle.spots)
        world = self.World(map=m, assets={})

        rv = list(puzzle.build(world=world))
        self.assertEqual(len(rv), len(puzzle.items), rv)

        entity = rv[0]
        self.assertEqual(entity.get_state(world.map.home).label, "inventory")
        self.assertEqual(entity.get_state("Home").label, "inventory")
        self.assertEqual(entity.get_state("Fruition"), Fruition.inception)


class StrandTests(unittest.TestCase):

    def test_default_item(self):
        r = Puzzle.Item()
        self.assertFalse(r.states)
        r.set_state(1)
        self.assertEqual(r.states, {"int": 1})

    def test_default_strand(self):
        self.assertRaises(TypeError, Strand)
        s = Strand(label="test")
        self.assertEqual(s.drama, {})

    def test_init(self):
        s = Strand(label="test", puzzles=[Puzzle(name="test")])
        self.assertEqual(next(iter(s.drama.values())).items, tuple())
        self.assertEqual(next(iter(s.drama.values())).spots, tuple())

    def test_simple(self):
        strand = Strand(
            label="single test strand",
            puzzles=[
                Puzzle(name="a"),
                Puzzle(name="b", links={"a"}),
                Puzzle(name="c", links={"a"}),
                Puzzle(name="d", links={"b", "c"}),
            ]
        )
        self.assertIn(Fruition.completion, {Fruition.completion})
        self.assertEqual(strand.active[0], strand.drama["a"])

        strand.drama["a"].set_state(Fruition.completion)
        self.assertEqual(strand.active, [strand.drama["b"], strand.drama["c"]], strand.active)

        strand.drama["b"].set_state(Fruition.completion)
        strand.drama["c"].set_state(Fruition.completion)
        self.assertEqual(strand.active[0], strand.drama["d"])


class TurnTests(unittest.TestCase):

    def test_two_strands(self):
        strands = [
            Strand(
                label="strand one",
                puzzles=[
                    Puzzle(name="a", spots={"a": ["spot a"]}),
                    Puzzle(name="f", links={"a"}),
                    Puzzle(name="g", links={"a"}),
                    Puzzle(name="d", links={"f", "g"}, spots={"d": ["spot d"]}),
                ]
            ),
            Strand(
                label="strand two",
                puzzles=[
                    Puzzle(name="e", spots={"a": ["spot a again"]}),
                    Puzzle(name="b", links={"e"}),
                    Puzzle(name="c", links={"e"}, spots={"c": ["spot c"]}),
                    Puzzle(name="h", links={"b", "c"}),
                ]
            )
        ]

        spots = Story.spots(strands)
        print(f"{spots=}")
        world = PuzzleTests.World(map=PuzzleTests.Map(spots={}), assets={})
        story = PuzzleTests.Story("Test", world=world)

        self.assertEqual(len(story.drama), 1)
        self.assertFalse(story.world.specs)
        self.assertFalse(story.world.statewise)
        self.assertFalse(story.world.typewise)

        self.assertTrue(issubclass(story.world.map.spot, enum.Enum))
        self.assertFalse(list(story.world.map.spot))

        story.turn()
