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

from collections import defaultdict
import operator
import re
import sys
import textwrap

import balladeer
from balladeer import discover_assets
from balladeer import quick_start
from balladeer import Page
from balladeer import Presenter
from balladeer import StoryBuilder
from balladeer.utils.themes import static_page

import rotu
from rotu.drama import Interaction
from rotu.frames.session import StorySession
from rotu.world import Map
from rotu.world import strands
from rotu.world import World


__doc__ = """
Usage:

    python -m rotu.main > themes.html

"""


Page.themes["grey"] = {
    "ink": {
        "gravity": "hsl(282.86, 0%, 6.12%)",
        "shadows": "hsl(293.33, 0%, 22.75%)",
        "lolight": "hsl(203.39, 0%, 31.96%)",
        "midtone": "hsl(203.39, 0%, 41.96%)",
        "hilight": "hsl(203.06, 0%, 56.47%)",
        "washout": "hsl(66.77, 0%, 82.75%)",
        "glamour": "hsl(50.00, 0%, 100%)",
    },
}

Page.themes["blue"] = {
    "ink": {
        "gravity": "hsl(203.33, 100%, 6.12%)",
        "shadows": "hsl(203.33, 96.92%, 12.75%)",
        "lolight": "hsl(203.33, 96.72%, 21.96%)",
        "midtone": "hsl(203.33, 96.72%, 31.96%)",
        "hilight": "hsl(203.33, 97.72%, 46.47%)",
        "washout": "hsl(203.33, 76.92%, 72.75%)",
        "glamour": "hsl(46.77, 76.92%, 72.75%)",
    },
}


class Representer(Presenter):

    href_matcher = re.compile('(<a\\s+)(href\\s*=\\s*")([^"]*?)("[^>]*?)>([^<]*?)(</a>)')

    @staticmethod
    def convert_link_into_button(match: re.Match):
        target = match[3].removeprefix("#")
        return f'<button popovertarget="{target}">{match[5]}</button>'

    def sanitize(self, html5: str) -> str:
        html5 = self.href_matcher.sub(self.convert_link_into_button, html5)
        return html5.replace("<blockquote id=", "<blockquote popover id=")


class Story(StoryBuilder):

    def make(self):
        # TODO: drama stored by location
        self.drama = list(self.build())
        return self

    @property
    def context(self):
        return next((reversed(sorted(self.drama, key=operator.attrgetter("state")))), None)

    def build(self, *args):
        # TODO: Store drama objects by strand/task/spot
        yield Interaction(
            *self.speech,
            world=self.world, config=self.config
        )


def factory(*args, assets={}):
    spots = defaultdict(list)
    for strand in strands:
        for task in strand.tasks:
            if task.drama is None: continue
            for rule in task.drama.rules:
                for term in rule.terms:
                    try:
                        if term not in spots[rule.name]:
                            spots[rule.name].append(term)
                    except KeyError:
                        # TODO: warn
                        pass

    base = [] # TODO: Generate via Strand
    world = World(map=Map(spots, base=base), assets=assets)
    return Story(*args, assets=assets, world=world)


def run():
    assets = discover_assets(rotu, "")
    story = factory(assets=assets)
    print(static_page().html)

    about = textwrap.dedent(f"""
    ©2024 D E Haynes
    Balladeer version {balladeer.__version__}
    Rotu version {rotu.__version__}
    """)
    quick_start(rotu, story_builder=story, about=about)


if __name__ == "__main__":
    run()
