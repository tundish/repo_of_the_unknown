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
from balladeer import Traffic
from balladeer import MapBuilder
from balladeer import WorldBuilder

from rotu.main import Story
from rotu.puzzle import Puzzle
from rotu.puzzle import Strand


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
                    Puzzle(name="A", spots={"a": ["spot a"]}),
                    Puzzle(name="F", links={"A"}),
                    Puzzle(name="G", links={"A"}),
                    Puzzle(
                        name="D", links={"F", "G"},
                        spots={"d": ["spot d"]},
                        items=(
                            Puzzle.Item(type="Transit", states=("exit.a", "into.d", Traffic.flowing)),
                            Puzzle.Item(type="Lamp", states=("spot.d")),
                        ),
                    )
                ]
            ),
            Strand(
                label="strand two",
                puzzles=[
                    Puzzle(
                        name="E", spots={"a": ["spot a again"]},
                        items=(
                            Puzzle.Item(type="Matches", states=("spot.a")),
                        ),
                    ),
                    Puzzle(name="B", links={"E"}),
                    Puzzle(
                        name="C", links={"E"},
                        spots={"c": ["spot c"]},
                        items=[
                            Puzzle.Item(type="Transit", states=("exit.a", "into.c", Traffic.flowing)),
                        ]
                    ),
                    Puzzle(name="H", links={"B", "C"}),
                ],
            )
        ]

        spots = Story.spots(strands)
        self.assertEqual(list(spots), ["a", "c", "d"])
        self.assertEqual(spots["a"], ["spot a", "spot a again"])

        m = PuzzleTests.Map(spots=spots)
        world = PuzzleTests.World(map=m, assets={})
        story = Story("Test", world=world, strands=strands)

        self.assertTrue(issubclass(story.world.map.spot, enum.Enum))
        self.assertEqual(len(story.world.map.spot), 3)

        self.assertFalse(story.world.specs, story.world.assets)
        self.assertFalse(story.world.statewise)

        self.assertFalse(story.world.entities)
        self.assertFalse(story.world.typewise)
        self.assertFalse(story.world.map.transits)

        self.assertIsNone(story.context.get_state(Fruition))

        story.turn()

        self.assertIn(story.context, (strands[0].drama["A"], strands[1].drama["E"]))
        self.assertEqual(story.context.get_state(Fruition), Fruition.inception)
