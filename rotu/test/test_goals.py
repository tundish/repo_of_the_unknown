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

from balladeer import discover_assets

import rotu
from rotu.main import World


class GoalTests(unittest.TestCase):

    def setUp(self):
        self.assets = discover_assets(rotu, "")
        self.world = World(assets=self.assets)

    def test_build_story(self):
        self.fail(self.world.specs)
