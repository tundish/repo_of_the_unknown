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

from collections import Counter
from collections import deque
from collections import namedtuple
import pprint
import re
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

    Tree = namedtuple("ConversationTree", ["block", "roles", "table", "path", "menu"])

    def __init__(self, *args, world=None, config=None, **kwargs):
        super().__init__(*args, config=config, world=world, **kwargs)
        self.state = 0
        self.tree = None
        self.witness = Counter()
        self.ol_matcher = re.compile("<ol>.*?<\\/ol>", re.DOTALL | re.MULTILINE)
        self.li_matcher = re.compile("<li id=\"(\\d+)\">", re.DOTALL | re.MULTILINE)
        self.pp_matcher = re.compile("<p[^>]*?>(.*?)<\\/p>", re.DOTALL)

    @staticmethod
    def follow_path(table, path: list):
        node = table
        for key in path:
            node = node.get(key, {})
            yield node

    @property
    def menu_options(self):
        return list(self.tree.menu.keys()) if self.tree else []

    def option_map(self, block: str):
        list_block = self.ol_matcher.search(block)
        list_items = list(self.li_matcher.findall(list_block.group()))
        para_items = list(self.pp_matcher.findall(list_block.group()))
        return dict(
            {k: v for k, v in zip(para_items, list_items)},
            **{v: v for k, v in zip(para_items, list_items)}
        )

    def build_tree(self, turn: StoryBuilder.Turn, identifier=0):
        try:
            n, block = turn.blocks[identifier]
            table = turn.scene.tables["_"][n]
        except (IndexError, KeyError, ValueError) as e:
            print(e)
            return None

        menu = self.option_map(block)
        return self.Tree(block=block, menu=menu, table=table, roles=turn.roles, path=deque([]))

    def on_branching(self, entity: Entity, *args: tuple[Entity], **kwargs):
        self.witness["branching"] += 1
        try:
            # Descend into tree
            node = list(self.follow_path(self.tree.table, self.tree.path))[-1]
            print(f"node: {node}")
            block = node.get("s", "")
            self.tree = self.tree._replace(menu=self.option_map(block))
        except AttributeError:
            # Build root tree
            identifier = kwargs.pop("identifier")
            print(f"identifier: {identifier}")
            self.tree = self.build_tree(StoryBuilder.Turn(**kwargs), identifier)
            # print(f"tree: {self.tree}")

    def on_returning(self, entity: Entity, *args: tuple[Entity], **kwargs):
        print("returning")
        self.witness["returning"] += 1

    def do_menu_option(self, this, text, director, *args, option: "menu_options", **kwargs):
        """
        {option}

        """
        try:
            key = self.tree.menu[option]
            #print(f"key {key}")
            branch = self.tree.table[key]
            #print(f"branch {branch}")
            self.tree.path.append(key)
        except KeyError:
            return

        for shot in branch.get(director.shot_key, []):
            #print(f"shot: {shot}")
            conditions = dict(director.specify_conditions(shot))
            if director.allows(conditions, self.tree.roles):
                text = shot.get(director.dialogue_key, "")
                yield Dialogue(text)


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
    if.CONVERSATION.tree = false
    s='''
    <ALAN> Let's practise our conversation skills.
    <ALAN.branching> Maybe now's a good time to ask {BETH.name} a question.
        1. Ask about the weather
        2. Ask about pets
        3. Ask about football

    '''

    [[_.1._]]
    s='''
    <BETH> Well, you never know what's it's going to do next, do you?
    '''

    [[_.1._]]
    s='''
    <BETH.returning> I've never seen anything like it!
    '''

    [[_.2._]]
    s='''
    <BETH.branching> I've got two lovely cats.
        1. Ask about Charlie
        2. Ask about Doodles
    '''

    [[_.2._.1._]]
    s='''
    <BETH> Charlie is the elder cat. He's a Marmalade. Very laid back.
    '''

    [[_.3._]]
    s='''
    <BETH> I don't know anything about football at all.
    '''

    [[_.2._.2._]]
    s='''
    <BETH> Oh my goodness, Doodles. Always up to mischief!
    '''

    [[_]]
    if.CONVERSATION.state = 1
    if.CONVERSATION.tree = false
    s='''
    <ALAN> OK. Conversation over.
    '''
    """)


    def setUp(self):
        scene_toml = Loader.read_toml(self.scene_toml_text)
        pprint.pprint(scene_toml)
        assets = Grouping.typewise([Loader.Scene(self.scene_toml_text, scene_toml, None, None, None)])
        world = self.World()
        self.story = StoryBuilder(assets=assets, world=world)
        self.story.drama = [Conversation(world=world)]
        self.assertIsInstance(self.story.context, Conversation)

    def test_no_command(self):
        n_turns = 4
        for n in range(n_turns):
            with self.story.turn() as turn:
                options = self.story.context.options(self.story.context.ensemble)
                action = self.story.action("2")
                with self.subTest(n=n):
                    if n == 0:
                        self.assertEqual(0, self.story.context.state)
                        self.assertEqual(1, self.story.context.witness["branching"])
                        self.assertIsNone(self.story.context.tree)
                        self.assertIsNone(action)
                        print(turn.blocks)
                    if n == 1:
                        self.assertEqual(0, self.story.context.state)
                        self.assertEqual(2, self.story.context.witness["branching"])
                        self.assertIsNone(self.story.context.tree)
                        self.assertIsNone(action)
                    elif n == 2:
                        self.assertEqual(0, self.story.context.state)
                        self.assertEqual(3, self.story.context.witness["branching"])
                        self.assertTrue(self.story.context.tree)
                        fn, args, kwargs = action
                        self.assertEqual({"option": "2"}, kwargs)
                    elif n == 3:
                        self.assertEqual(0, self.story.context.state)
                        self.assertEqual(4, self.story.context.witness["branching"])
                        self.assertTrue(self.story.context.tree)
                        fn, args, kwargs = action
                        self.assertEqual({"option": "2"}, kwargs)


    def test_double_branch(self):
        n_turns = 4
        for n in range(n_turns):
            with self.story.turn() as turn:
                options = self.story.context.options(self.story.context.ensemble)
                action = self.story.action("2")
                with self.subTest(n=n):
                    if n == 0:
                        self.assertEqual(0, self.story.context.state)
                        self.assertIsNone(self.story.context.tree)
                        self.assertIsNone(action)
                    if n == 1:
                        self.assertEqual(0, self.story.context.state)
                        self.assertIsNone(self.story.context.tree)
                        self.assertIsNone(action)
                    elif n == 2:
                        self.assertEqual(0, self.story.context.state)
                        self.assertTrue(self.story.context.tree)
                        fn, args, kwargs = action
                        self.assertEqual({"option": "2"}, kwargs)

        self.assertEqual(2, self.story.context.witness["branching"])
