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
from balladeer import Grouping
from balladeer import Loader
from balladeer import StoryBuilder
from balladeer import WorldBuilder

from speechmark import SpeechMark


class Conversation(Drama):
    # TODO: Make prompt a property which summarises option numbers

    def on_elaborating(self, entity: Entity, *args: tuple[Entity], **kwargs):
        print("Dong!!!")

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

    class World(WorldBuilder):
        def build(self):
            yield from [
                Entity(name="Alan", type="Narrator"),
                Entity(name="Beth", type="Gossiper"),
            ]

    scene_toml_text = textwrap.dedent("""
    [ALAN]
    type = "Narrator"

    [BETH]
    type = "Gossiper"

    [CONVERSATION]
    type = "Conversation"

    [[_]]
    if.CONVERSATION.state = 0
    s='''
    <ALAN> Let's practise our conversation skills.
    '''

    [[_]]
    if.CONVERSATION.state = 0
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
    if.CONVERSATION.state = 1
    s='''
    <ALAN> OK. Conversation over.
    '''
    """)


    def setUp(self):
        scene_toml = Loader.read_toml(self.scene_toml_text)
        assets = Grouping.typewise([Loader.Scene(self.scene_toml_text, scene_toml, None, None, None)])
        world = self.World()
        self.story = StoryBuilder(assets=assets, world=world)
        self.story.drama = [Conversation(world=world)]
        self.assertIsInstance(self.story.context, Conversation)

    def test_terminal(self):
        n = 0
        while n < 4:
            n += 1
            with self.story.turn() as turn:
                print(turn.blocks)
                print(turn.roles)
                print(turn.notes)
                print()

            self.story.context.state = n
