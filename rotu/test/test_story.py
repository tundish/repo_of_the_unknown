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

import copy
import unittest

from balladeer import Entity
from balladeer import Transit
from balladeer import MapBuilder
from balladeer import WorldBuilder

from rotu.main import factory
from rotu.main import strands
from rotu.puzzle import Puzzle
from rotu.story import Story


class StoryTests(unittest.TestCase):

    def setUp(self):
        self.story = Story(strands=strands)
        self.assertTrue(self.story.strands)

    def test_story_copy_drama(self):
        b = copy.deepcopy(self.story)
        self.assertNotEqual(self.story.uid, b.uid, vars(self.story))
        self.assertNotEqual(self.story.director, b.director, vars(self.story.director))

        # Side effect: each drama generates its active set
        self.assertFalse(self.story.drama)
        self.assertTrue(self.story.context)

        witness = []
        for strand in self.story.strands:
            for drama in strand.drama:
                with self.subTest(a=self.story, b=b, drama=drama):
                    self.assertNotIn(drama, [i for strand in b.strands for i in strand.drama])
                    witness.append(drama)

        self.assertTrue(witness)

    def test_story_copy_map(self):
        witness = dict()

        class Map(MapBuilder):
            def build(self):
                nonlocal witness
                witness[self] = True
                yield Transit().set_state(self.exit.a, self.into.b)
                yield Transit().set_state(self.exit.b, self.into.a)

        class World(WorldBuilder):
            def build(self):
                nonlocal witness
                witness[self] = bool(self.map)
                yield Entity()
                yield Entity()
                yield Entity()

        spots = {
            "a": ["A", "a"],
            "b": ["B", "b"],
        }
        m = Map(spots)
        self.story.world = World(map=m)
        a = self.story
        b = copy.deepcopy(a)

        self.assertEqual(3, len(a.world.entities))
        for entity in a.world.entities:
            with self.subTest(a=a, b=b, entity=entity):
                self.assertFalse(any(entity.names is i.names for i in b.world.entities))
                self.assertFalse(any(entity.states is i.states for i in b.world.entities))
                self.assertFalse(any(entity.types is i.types for i in b.world.entities))

        self.assertTrue(a.world.map)
        self.assertTrue(b.world.map)
        self.assertIs(a.world.map.spot, b.world.map.spot)
        self.assertIs(a.world.map.exit, b.world.map.exit)
        self.assertIs(a.world.map.into, b.world.map.into)
        self.assertIs(a.world.map.home, b.world.map.home)

        for transit in a.world.map.transits:
            with self.subTest(a=a, b=b, transit=transit):
                self.assertFalse(any(transit.names is i.names for i in b.world.map.transits))
                self.assertFalse(any(transit.states is i.states for i in b.world.map.transits))
                self.assertFalse(any(transit.types is i.types for i in b.world.map.transits))

        self.assertEqual(4, len(witness), witness)
        self.assertTrue(all(witness.values()), witness)

    def test_story_copy_strands(self):
        s = copy.deepcopy(self.story)
        self.assertTrue(s.strands)
        self.assertEqual(
            self.story.spots(self.story.strands),
            s.spots(s.strands),
            s.strands
        )
        self.assertEqual(len(self.story.strands), len(s.strands))
        for a in self.story.strands:
            for b in s.strands:
                with self.subTest(a=a, b=b):
                    self.assertIsNot(a.sorter, b.sorter)
                    self.assertFalse(set(a.items).intersection(set(b.items)))
                    self.assertFalse({i.uid for i in a.items}.intersection({i.uid for i in a.items}))
