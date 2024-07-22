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

from balladeer import Dialogue
from balladeer import Page

from rotu.main import factory
from rotu.main import Story
from rotu.main import StorySession
from rotu.test.test_popover import PopoverTests


class ActionTests(unittest.TestCase):

    def test_command_form(self):

        story = Story(
            Dialogue("<> Perhaps it's time to go to bed?"),
        )

        page = Page()
        request = PopoverTests.mock_request()
        endpoint = StorySession(dict(type="http"), None, None)
        with story.turn() as turn:
            page = endpoint.compose(request, page, story, turn)
        lines = page.html.splitlines()

        command_form = next(
            (i for i in lines if i.startswith("<form") and 'name="ballad-command-form"' in i),
            None
        )
        self.assertTrue(command_form, lines)

    def test_code_implies_action(self):

        story = Story(
            Dialogue("<> Perhaps it's time to `go to bed`?"),
        )

        page = Page()
        request = PopoverTests.mock_request()
        endpoint = StorySession(dict(type="http"), None, None)
        with story.turn() as turn:
            page = endpoint.compose(request, page, story, turn)
        lines = page.html.splitlines()

        command_form = next(
            (i for i in lines if i.startswith("<form") and 'name="ballad-command-form"' in i),
            None
        )
        self.assertTrue(command_form, lines)

        action_button = next(
            (i for i in lines if "<button" in i and 'form="ballad-action-form-go-to-bed"' in i),
            None
        )
        self.assertTrue(action_button, lines)
        action_form = next(
            (i for i in lines if i.startswith("<form") and 'id="ballad-action-form-go-to-bed"' in i),
            None
        )
        self.assertTrue(action_form, lines)
