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

from balladeer import discover_assets
from balladeer import Loader
from busker.stager import Stager

import rotu
from rotu.drama import Resident


class ResidentTests(unittest.TestCase):

    class TestResident(Resident):
        pass

    def test_is_resident(self):
        Colour = enum.Enum("Colour", ["red", "blue", "green", "yellow"])
        Spot = enum.Enum("Spot", {"kitchen": ["kitchen"], "hall": ["hallway"], "cloaks": ["cloakroom", "toilet"]})

        selector = {
            "states": [
                "colour.green",
                "spot.kitchen",
                "spot.cloaks",
            ]
        }

        drama = self.TestResident(selector=selector)
        self.assertIsInstance(drama.selector["states"], set)

        self.assertTrue(drama.is_resident(Colour.green))
        self.assertFalse(drama.is_resident(Colour.red))

        self.assertFalse(drama.is_resident(Colour.red, Spot.kitchen))
        self.assertTrue(drama.is_resident(Colour.green, Spot.kitchen))

    def test_scripts(self):
        selector = {
            "paths": [
                "rotu/scenes/0[01]/*.scene.toml",
            ],
        }

        assets = discover_assets(rotu, "scenes")
        scenes = assets.get(Loader.Scene, [])

        drama = self.TestResident(selector=selector)
        scripts = drama.scripts(scenes)

        witness = set(i.path.parts[-3:] for i in scripts)
        self.assertEqual(
            witness,
            set((
                ("scenes", "00", "0.scene.toml"),
                ("scenes", "00", "a.scene.toml"),
                ("scenes", "01", "a.scene.toml"),
            ))
        )
