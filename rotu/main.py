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
from collections import deque
import itertools
import operator
import random
import re
import sys
import textwrap

import balladeer
from balladeer import discover_assets
from balladeer import quick_start
from balladeer import Page
from balladeer import Presenter
from balladeer import Traffic
from balladeer import Transit
from balladeer.utils.themes import static_page

import rotu
from rotu.puzzle import Puzzle
from rotu.puzzle import Strand
from rotu.story import Story
from rotu.world import Map
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


strands = [
    Strand(
        label="Get Gigging",
        puzzles=[
            Puzzle(
                name="tracker manual page 1",
                spots={
                    "van_f_ext": ["in front of the van"],
                    "van_f_int": ["in the van"],
                    "van_b_ext": ["behind the van"],
                    "van_b_int": ["in the back of the van"],
                    "car_park": ["car park"],
                    "cafe_f_ext": ["in front of the cafe"],
                    "shed_f_ext": ["in front of the shed"],
                    "shed_f_int": ["inside the shed"],
                    "shed_b_int": ["back of the shed"],
                    "roadside": ["by the roadside"],
                },
                items=(
                    Puzzle.Item(type="Focus", init=("spot.van_f_int")),
                    Puzzle.Item(type="Transit", init=("exit.cafe_f_ext", "into.car_park", Traffic.flowing)),
                    Puzzle.Item(type="Transit", init=("exit.car_park", "into.shed_f_ext", Traffic.flowing)),
                    Puzzle.Item(type="Transit", init=("exit.shed_f_ext", "into.shed_f_int", Traffic.flowing)),
                    Puzzle.Item(type="Transit", init=("exit.shed_f_int", "into.shed_b_int", Traffic.flowing)),
                    Puzzle.Item(type="Transit", init=("exit.car_park", "into.van_f_ext", Traffic.flowing)),
                    Puzzle.Item(type="Transit", init=("exit.van_f_int", "into.van_b_int", Traffic.blocked)),
                    Puzzle.Item(
                        names=("Door", "Van door"), type="Door", aspect="unlocked", sketch="The {0.name} is {aspect}",
                        init=("exit.van_f_ext", "into.van_f_int", Traffic.flowing)
                    ),
                    Puzzle.Item(type="Void", init=("exit.car_park", "into.van_b_ext", Traffic.flowing)),
                    Puzzle.Item(type="Void", init=("exit.van_b_ext", "into.van_b_int", Traffic.flowing)),
                    Puzzle.Item(type="Void", init=("exit.van_b_ext", "into.roadside", Traffic.flowing)),
                ),
            ),
            Puzzle(
                name="collect tracker samples",
                links={"tracker manual page 1"},
                items=[
                ],
            ),
        ],
    ),
]


class Representer(Presenter):

    href_matcher = re.compile('(<a\\s+)(href\\s*=\\s*")([^"]*?)("[^>]*?)>([^<]*?)(</a>)')

    @staticmethod
    def convert_link_into_button(match: re.Match):
        target = match[3].removeprefix("#")
        return f'<button popovertarget="{target}">{match[5]}</button>'

    def sanitize(self, html5: str) -> str:
        html5 = self.href_matcher.sub(self.convert_link_into_button, html5)
        return html5.replace("<blockquote id=", "<blockquote popover id=")


def factory(*args, assets={}, strands: list[Strand] = []):
    spots = Story.spots(strands)
    world = World(map=Map(spots=spots), assets=assets)
    return Story(*args, assets=assets, world=world, strands=strands)


def run():
    assets = discover_assets(rotu, "")
    story = factory(assets=assets, strands=strands)
    print(static_page().html)

    about = textwrap.dedent(f"""
    ©2024 D E Haynes
    Balladeer version {balladeer.__version__}
    Rotu version {rotu.__version__}
    """)
    quick_start(rotu, story_builder=story, about=about)


if __name__ == "__main__":
    run()
