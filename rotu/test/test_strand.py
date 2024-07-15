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

from rotu.strand import Rule
from rotu.strand import Strand
from rotu.strand import Task


class StrandTests(unittest.TestCase):

    def test_defaults(self):
        self.assertRaises(TypeError, Strand)
        self.assertRaises(TypeError, Task)
        self.assertRaises(TypeError, Rule)
        s = Strand(label="test")
        self.assertFalse(s.tasks)

    def test_simple(self):
        s = Strand(label="test", tasks=[Task(label="test")])
        self.assertEqual(s.tasks[0].items, [])
        self.assertIsNone(s.tasks[0].drama)

    @unittest.skip("TODO")
    def test_base_map(self):
        self.fail()
