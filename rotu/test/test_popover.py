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

import pathlib
import unittest
from unittest.mock import Mock

from balladeer import Dialogue
from balladeer import StoryBuilder
from balladeer import Page
from starlette.applications import Starlette
from starlette.datastructures import State
from starlette.requests import Request

from rotu.frames.session import StorySession
from rotu.main import Representer
from rotu.story import Story


class PopoverTests(unittest.TestCase):

    @staticmethod
    def mock_request():
        request = Mock(spec=Request)
        request.app = Mock(spec=Starlette)
        request.app.state = Mock(spec=State)
        request.app.state.static = pathlib.Path(".")
        request.app.state.presenter = Representer()
        return request

    def test_label_implies_popover(self):

        story = StoryBuilder(
            Dialogue("<?label=test-01> Knock, knock."),
        )

        page = Page()
        request = self.mock_request()
        endpoint = StorySession(dict(type="http"), None, None)
        with story.turn() as turn:
            page = endpoint.compose(request, page, story, turn)
        lines = page.html.splitlines()
        self.assertIn(
            '<blockquote popover id="test-01" cite="&lt;?label=test-01&gt;">', lines
        )

    def test_href_to_id_becomes_popovertarget(self):

        story = StoryBuilder(
            Dialogue("<> Want to [know more](#more-info)?"),
        )

        page = Page()
        request = self.mock_request()
        endpoint = StorySession(dict(type="http"), None, None)
        with story.turn() as turn:
            page = endpoint.compose(request, page, story, turn)

        self.assertNotIn(
            '<a href="#more-info">know more</a>?',
            page.html
        )
        self.assertNotIn(
            '<a href="#more-info" target="_blank" rel="noopener noreferrer">know more</a>?',
            page.html
        )

        self.assertIn(
            '<button popovertarget="more-info">know more</button>',
            page.html
        )
