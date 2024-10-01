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

from balladeer import discover_assets
from balladeer import Entity
from balladeer import Fruition
from balladeer import Grouping
from balladeer import Loader
from balladeer import Stager
from balladeer import Traffic
from balladeer import Transit

import rotu
from rotu.drama import Resident
from rotu.story import Story


class StoryTests(unittest.TestCase):

    def setUp(self):
        assets = discover_assets(rotu, "")
        self.assertTrue(assets[Loader.Staging])
        self.story = Story(assets=assets)
