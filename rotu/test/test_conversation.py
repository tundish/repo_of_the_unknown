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

import textwrap
import tomllib
import unittest

from balladeer import Dialogue
from balladeer import Drama
from balladeer import Entity

from speechmark import SpeechMark


class Conversation(Drama):
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


class ConversationTests(unittest.TestCase):

    scene_toml = textwrap.dedent("""
    [ALAN]
    type = "Narrator"

    [BETH]
    type = "Gossiper"

    [[_]]
    s='''
    <ALAN> Let's practise our conversation skills.
    '''

    [[_]]
    s='''
    <ALAN.elaborating> Maybe now's a good time to ask {BETH.name} a question.
        1. Ask about the weather
        2. Ask about pets
        3. Ask about football
    '''

    [[_.1]]
    s='''
    <BETH> Well, you never know what's it's going to do next, do you?
    '''

    [[_.2]]
    s='''
    <BETH.elaborating> I've got two lovely cats.
        1. Ask about Charlie
        2. Ask about Doodles
    '''

    [[_.2.1]]
    s='''
    <BETH> Charlie is the elder cat. He's a Marmalade. Very laid back.
    '''

    [[_.3]]
    s='''
    <BETH> I don't know anything about football at all.
    '''

    [[_.2.2]]
    s='''
    <BETH> Oh my goodness, Doodles. Always up to mischief!
    '''

    [[_]]
    s='''
    <ALAN> OK. Conversation over.
    '''
    """)


    def setUp(self):
        self.ensemble = [
            Entity(name="Alan", type="Narrator"),
            Entity(name="Beth", type="Gossiper"),
        ]

    def test_asj(self):
        data = tomllib.loads(self.scene_toml)
        print(data)

        convo = Conversation()
        self.fail(convo)
