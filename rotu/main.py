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

import sys

import balladeer
from balladeer import discover_assets
from balladeer import quick_start
from balladeer import Dialogue
from balladeer import Entity
from balladeer import Grouping
from balladeer import Loader
from balladeer import Page
from balladeer import Session
from balladeer import StoryBuilder
from balladeer import Turn
from balladeer import WorldBuilder
from balladeer.lite.app import About
from balladeer.utils.themes import static_page

from starlette.responses import PlainTextResponse

import rotu

__doc__ = """
Usage:

    python -m rotu.main > themes.html

"""

ex = (
Dialogue("""
<NARRATOR.elaborating@ACTOR> Maybe now's a good time to ask {ACTOR.name} a question.
    1. Ask about LAAR
    2. Ask about Thackaray
    3. Ask about Lewis
"""),
[
]
)


class AboutThisProject(About):
    async def get(self, request):
        return PlainTextResponse(
            "\n".join(
                (
                    "©2023 D E Haynes",
                    f"Balladeer version {balladeer.__version__}",
                    f"Rotu version {rotu.__version__}",
                )
            )
        )


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


class World(WorldBuilder):
    pass


class Narrative(Session):
    # TODO for options=list(story.context.options(ensemble).keys())) eg:
    """
    <label for="ice-cream-choice">Choose a flavor:</label>
    <input list="ice-cream-flavors" id="ice-cream-choice" name="ice-cream-choice" />

    <datalist id="ice-cream-flavors">
      <option value="Chocolate"></option>
      <option value="Coconut"></option>
      <option value="Mint"></option>
      <option value="Strawberry"></option>
      <option value="Vanilla"></option>
    </datalist>
    """

    def compose(
        self, request, page: Page, story: StoryBuilder = None, turn: Turn = None
    ) -> Page:
        page = super().compose(request, page, story, turn)

        page.paste(
            '<div class="dressing">',
            *(f'<span class="rockery"></span>' for n in range(8)),
            '<span class="factory"></span>',
            "</div>",
            zone=page.zone.basket
        )
        return page


def run():
    assets = discover_assets(rotu, "")
    world = World(assets=assets)
    story_builder = StoryBuilder(assets=assets, world=world)
    print(world.specs, file=sys.stderr)
    #print(static_page().html)

    quick_start(rotu, story_builder=story_builder)


if __name__ == "__main__":
    run()
