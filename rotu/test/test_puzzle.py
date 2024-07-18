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

import unittest

from balladeer import StoryBuilder
from balladeer import MapBuilder
from balladeer import WorldBuilder

from rotu.puzzle import Puzzle
from rotu.puzzle import Strand


class StrandTests(unittest.TestCase):

    def test_defaults(self):
        self.assertRaises(TypeError, Strand)
        self.assertRaises(TypeError, Puzzle.Rule)
        s = Strand(label="test")
        self.assertFalse(s.tasks)

    def test_simple(self):
        s = Strand(label="test", drama=[Puzzle(name="test")])
        self.assertEqual(s.drama[0].rules, tuple())
        self.assertIsNone(s.drama[0].spots)

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
        pass

    def test_simple(self):
        world = self.World(map=self.Map(spots={}), assets={})
        story = self.Story("Test", world=world)

        self.assertEqual(len(story.drama), 1)
        self.assertFalse(story.world.statewise)
        self.assertFalse(story.world.typewise)

        print(f"{story.world.statewise=}")
