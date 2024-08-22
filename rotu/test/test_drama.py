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

from rotu.drama import Resident

from busker.stager import Stager


class ResidentTests(unittest.TestCase):

    class TestResident(Resident):
        pass

    def test_is_resident_spot(self):
        Colour = enum.Enum("Colour", ["red", "blue", "green", "yellow"])
        Spot = enum.Enum("Spot", {"kitchen": ["kitchen"], "hall": ["hallway"], "cloaks": ["cloakroom", "toilet"]})

        selector = {
            "paths": [
                "rotu/assets/scenes/01/*.scene.toml",
                "rotu/assets/scenes/02/*.scene.toml"
            ],
            "states": [
                "spot.kitchen",
                "spot.cloaks",
            ]
        }

        drama = self.TestResident(selector=selector)
        self.fail(drama)
