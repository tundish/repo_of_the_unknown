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
import functools
import re
import sys
import textwrap

import balladeer
from balladeer import discover_assets
from balladeer import quick_start
from balladeer import Drama
from balladeer import Detail
from balladeer import Entity
from balladeer import Epilogue
from balladeer import MapBuilder
from balladeer import Page
from balladeer import Presenter
from balladeer import Prologue
from balladeer import Session
from balladeer import SpeechTables
from balladeer import StoryBuilder
from balladeer import Traffic
from balladeer import Transit
from balladeer import Turn
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


class Map(MapBuilder):
    spots = {
        "van_f_ext": ["in front of the van"],
        "van_f_in": ["into the van"],
        "van_b_ext": ["behind the van"],
        "van_b_in": ["back of the van"],
        "car_park": ["car park"],
        "cafe_f_ext": ["in front of the cafe"],
        "shed_f_int": ["inside the shed"],
        "shed_b_int": ["back of the shed"],
        "roadside": ["by the roadside"],
    }

    def build(self):
        yield from [
            Transit().set_state(self.exit.cafe_f_ext, self.into.car_park, Traffic.flowing),
            Transit().set_state(self.exit.car_park, self.into.shed_f_ext, Traffic.flowing),
            Transit().set_state(self.exit.shed_f_ext, self.into.shed_f_int, Traffic.flowing),
            Transit().set_state(self.exit.shed_f_int, self.into.shed_b_int, Traffic.flowing),
            Transit().set_state(self.exit.car_park, self.into.van_f_ext, Traffic.flowing),
            Transit().set_state(self.exit.van_f_ext, self.into.van_f_int, Traffic.flowing),
            Transit().set_state(self.exit.car_park, self.into.van_b_ext, Traffic.flowing),
            Transit().set_state(self.exit.van_b_ext, self.into.van_b_int, Traffic.flowing),
            Transit().set_state(self.exit.van_b_ext, self.into.roadside, Traffic.flowing),
        ]


class StorySession(Session):

    code_matcher = re.compile(f"(<code.*?>)(.*?)(<\\/code>)", re.DOTALL)

    @staticmethod
    def convert_code_into_action(match: re.Match, request=None, story=None, turn=None, page = None):
        text = f"{match[2]}".replace(" ", "-")
        try:
            url = request.url_for("command", session_id=story.uid)
            form = textwrap.dedent(f"""
            <form role="form" action="{url}" method="post" id="ballad-action-form-{text}" class="ballad action">
            <input type="hidden" name="ballad-command-form-input-text" value="{match[2]}" />
            </form>
            """)
            page.paste(form, zone=page.zone.inputs)
        except AttributeError:
            pass
        return f'<button form="ballad-action-form-{text}" class="ballad action" type="submit">{match[2]}</button>'

    def render_cues(
        self, request, story: StoryBuilder = None, turn: Turn = None, page: Page = None
    ) -> Generator[str]:
        for cue_block in super().render_cues(request, story, turn):
            func = functools.partial(self.convert_code_into_action, request=request, story=story, turn=turn, page=page)
            yield self.code_matcher.sub(func, cue_block)

    def render_title(self, request, story, turn):
        try:
            chapter = int(turn.scene.path.parent.name) + 1
            section = int(turn.scene.path.with_suffix("").with_suffix("").name)
        except ValueError:
            section = turn.scene.path.with_suffix("").with_suffix("").name.upper()
        except Exception:
            chapter = 0
            section = "??"

        return f"<title>RotU section {chapter:02d}-{section}</title>"


class Interaction(SpeechTables, Drama):
    def on_proposing(self, entity: Entity, *args: tuple[Entity], **kwargs):
        for ent in args:
            ent.set_state(Fruition.elaboration)

    def on_suggesting(self, entity: Entity, *args: tuple[Entity], **kwargs):
        for ent in args:
            ent.set_state(Fruition.discussion)

    def on_confirming(self, entity: Entity, *args: tuple[Entity], **kwargs):
        for ent in args:
            ent.set_state(Fruition.construction)

    def on_delivering(self, entity: Entity, *args: tuple[Entity], **kwargs):
        for ent in args:
            ent.set_state(Fruition.transition)

    def on_declaring(self, entity: Entity, *args: tuple[Entity], **kwargs):
        for ent in args:
            ent.set_state(Fruition.completion)

    def do_info(self, this, text, director, *args, **kwargs):
        """
        info | i

        """
        self.tree = None
        self.set_state(Detail.info)
        elaboration = self.world.statewise[str(Fruition.elaboration)]
        discussion = self.world.statewise[str(Fruition.discussion)]
        construction = self.world.statewise[str(Fruition.construction)]
        if elaboration:
            items = "\n".join(
                f"+ {i.description[0].upper() + i.description[1:]}"
                for i in elaboration
                if i.description
            )
            yield Epilogue(f"<> You should maybe:\n{items}")


class World(WorldBuilder):
    def build(self) -> Generator[Entity]:
        for entity in self.build_to_spec(self.specs):
            if entity.names and "Goal" in entity.types:
                if "goal_00a" in entity.names:
                    yield entity.set_state(Fruition.elaboration)
                else:
                    yield entity.set_state(Fruition.inception)


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
