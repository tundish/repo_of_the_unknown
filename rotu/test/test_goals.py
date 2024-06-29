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

from collections import Counter
from types import SimpleNamespace
import unittest

from balladeer import discover_assets
from balladeer import Entity

import rotu
from rotu.main import factory
from rotu.main import World


class GoalTests(unittest.TestCase):

    inputs = SimpleNamespace(
        a=(
            ("goal_00a", "yes"),
            ("goal_00a", ""),
            ("goal_01a", "yes"),
            ("goal_01a", ""),
            ("goal_02a", "yes"),
            ("goal_02a", ""),
            ("goal_24a", "yes"),
            ("goal_24a", ""),
        ),
    )

    def setUp(self):
        self.assets = discover_assets(rotu, "")

    def test_build_story(self):
        witness = Counter()
        story = factory(assets=self.assets)
        for n, (g, i) in enumerate(self.inputs.a):
            with self.subTest(i=i, n=n):
                with story.turn() as turn:
                    witness[tuple(turn.blocks)] += 1
                    ensemble = story.context.ensemble
                    options = story.context.options(ensemble)
                    self.assertIn(turn.scene.path.parent.name, turn.roles["GOAL"].types)
                    self.assertEqual(turn.roles["GOAL"].name, g, turn.roles)
                    if i:
                        self.assertIn(i, options)
                    story.action(i)
