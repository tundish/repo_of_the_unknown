#!/usr/bin/env python
# encoding: utf8

# Copyright 2023 D E Haynes

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

from balladeer import Dialogue
from balladeer import Drama

from speechmark import SpeechMark


class Prompter(Drama):
    # TODO: Make prompt a property which summarises option numbers

    def do_ask(self, this, text, director):
        """
        Ask {p.entity} about {p.topic}

        """
        yield Dialogue("Yes, this.")

    def do_say(self, this, text, director):
        """
        Say {p.phrase}
        Tell {p.entity} that {p.phrase}

        """
        yield from [Dialogue("Yes."), dialogue("That.")]


class TestPrompter(unittest.TestCase):

    def test_asj(self):
        prompter = Prompter()
        self.fail(prompter)
