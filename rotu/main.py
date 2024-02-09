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

from collections.abc import Generator
import sys
import textwrap

import balladeer
from balladeer import discover_assets
from balladeer import quick_start
from balladeer import Drama
from balladeer import Detail
from balladeer import Entity
from balladeer import Page
from balladeer import SpeechTables
from balladeer import StoryBuilder
from balladeer import WorldBuilder
from balladeer.lite.types import Fruition
from balladeer.utils.themes import static_page

import rotu

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


class Interaction(SpeechTables, Drama):
    def on_declaring(self, entity: Entity, *args: tuple[Entity], **kwargs):
        entity.set_state(Fruition.completion)

    def do_info(self, this, text, director, *args, **kwargs):
        """
        info | i

        """
        self.set_state(Detail.info)


class World(WorldBuilder):
    def build(self) -> Generator[Entity]:
        for entity in self.build_to_spec(self.specs):
            if entity.names and "Goal" in entity.types:
                yield entity.set_state(Fruition.inception)


class Story(StoryBuilder):
    pass


def run():
    assets = discover_assets(rotu, "")
    world = World(assets=assets)
    story = Story(assets=assets, world=world)
    print(static_page().html)

    about = textwrap.dedent(f"""
    ©2024 D E Haynes
    Balladeer version {balladeer.__version__}
    Rotu version {rotu.__version__}
    """)
    quick_start(rotu, story_builder=story, about=about)


if __name__ == "__main__":
    run()
