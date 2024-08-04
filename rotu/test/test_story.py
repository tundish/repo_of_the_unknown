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
import enum
import unittest

from balladeer import Entity
from balladeer import Transit

from rotu.main import strands
from rotu.puzzle import Puzzle
from rotu.story import Story


class StoryTests(unittest.TestCase):

    def setUp(self):
        self.story = Story(strands=strands)
        self.assertTrue(self.story.strands)
        self.assertTrue(issubclass(self.story.world.map.spot, enum.Enum))

        self.assertTrue(self.story.world.entities)
        self.assertTrue(self.story.world.map.transits)
        self.assertGreater(len(self.story.world.map.spot), 1, list(self.story.world.map.spot))

    def test_story_copy_drama(self):
        b = copy.deepcopy(self.story)
        self.assertNotEqual(self.story.uid, b.uid, vars(self.story))
        self.assertIsNot(self.story.director, b.director, vars(self.story.director))

        self.assertFalse(self.story.drama)
        self.assertTrue(self.story.context)

        witness = []
        for strand in self.story.strands:
            for drama in strand.drama.values():
                self.assertEqual(sorted(set(drama.names)), sorted(drama.names), drama.names)
                with self.subTest(a=self.story, b=b, drama=drama):
                    self.assertNotIn(
                        id(drama), [id(i) for strand in b.strands for i in strand.drama.values()],
                        strand.drama
                    )
                    witness.append(drama)

        self.assertTrue(witness)

    def test_story_copy_map(self):
        a = copy.deepcopy(self.story)
        b = copy.deepcopy(self.story)

        self.assertEqual(
            [drama.name for s in a.strands for drama in s.drama.values()],
            [drama.name for s in b.strands for drama in s.drama.values()]
        )

        for entity in a.world.entities:
            with self.subTest(a=a, b=b, entity=entity):
                self.assertFalse(any(entity.names is i.names for i in b.world.entities), entity.names)
                self.assertFalse(any(entity.states is i.states for i in b.world.entities))
                self.assertFalse(any(entity.types is i.types for i in b.world.entities))

        self.assertTrue(a.world.map)
        self.assertTrue(b.world.map)

        self.assertIsNot(a.world, b.world)
        self.assertIsNot(a.world.map, b.world.map)

        self.assertGreater(len(a.world.map.spot), 1, list(a.world.map.spot))

        self.assertIsNot(a.world.map.spot, b.world.map.spot)
        self.assertEqual([str(i) for i in a.world.map.spot], [str(i) for i in b.world.map.spot])

        self.assertIsNot(a.world.map.exit, b.world.map.exit)
        self.assertEqual([str(i) for i in a.world.map.exit], [str(i) for i in b.world.map.exit])

        self.assertIsNot(a.world.map.into, b.world.map.into)
        self.assertEqual([str(i) for i in a.world.map.into], [str(i) for i in b.world.map.into])

        self.assertIsNot(a.world.map.home, b.world.map.home)
        self.assertEqual([str(i) for i in a.world.map.home], [str(i) for i in b.world.map.home])

        self.assertTrue(a.world.map.transits)
        self.assertTrue(b.world.map.transits, a.world.map.transits)
        for transit in a.world.map.transits:
            with self.subTest(a=a, b=b, transit=transit):
                self.assertFalse(any(transit.names is i.names for i in b.world.map.transits), transit.names)
                self.assertFalse(any(transit.states is i.states for i in b.world.map.transits))
                self.assertFalse(any(transit.types is i.types for i in b.world.map.transits))

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
