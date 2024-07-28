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
from rotu.test.test_puzzle import PuzzleTests


class StrandTests(unittest.TestCase):

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

    def test_default(self):
        story = Story()
        self.assertIsInstance(story.context, Puzzle)

        self.assertTrue(story.world.typewise)

        focus = story.context.focus
        self.assertIsInstance(focus, Entity)


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
                            Puzzle.Item(type="Transit", init=("exit.a", "into.d", Traffic.flowing)),
                            Puzzle.Item(type="Lamp", init=("spot.d")),
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
                            Puzzle.Item(name="Matches", init=("spot.a")),
                        ),
                    ),
                    Puzzle(name="B", links={"E"}),
                    Puzzle(
                        name="C", links={"E"},
                        spots={"c": ["spot c"]},
                        items=[
                            Puzzle.Item(type="Transit", init=("exit.a", "into.c", Traffic.flowing)),
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

        self.assertIn(story.context, (strands[0].drama["A"], strands[1].drama["E"]))
        self.assertEqual(story.world.entities[0].name, "Matches")
        self.assertEqual(story.world.typewise[Puzzle.Item][0].name, "Matches")
        self.assertEqual(story.context.get_state(Fruition), Fruition.inception)

        witness = set()
        for n in range(1, 9):
            with self.subTest(n=n):
                story.turn()

                context = story.context
                context.set_state(Fruition.completion)
                witness.add(context.name)
                self.assertEqual(len(witness), n, witness)
