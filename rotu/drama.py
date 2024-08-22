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

import enum

from balladeer import Detail
from balladeer import Drama
from balladeer import Entity
from balladeer import Epilogue
from balladeer import Fruition
from balladeer import Loader
from balladeer import Prologue
from balladeer import SpeechTables


class Resident:

    def __init__(self, *args, selector: dict[str, list] = {}, **kwargs):
        self.selector = selector | {"states": set(selector.get("states", []))}
        super().__init__(*args, **kwargs)

    def is_resident(self, *args: tuple[enum.Enum]):
        return all(str(i).lower() in self.selector["states"] for i in args)

    def scripts(self, assets: list):
        # TODO: Differentiate between Structure assets for Stage.
        return [i for i in assets if isinstance(i, Loader.Scene)]

    # Memo
    @property
    def active(self):
        for key in list(self._active.keys()):
            try:
                if self.drama[key].get_state(Fruition) in {
                    Fruition.withdrawn, Fruition.defaulted, Fruition.cancelled, Fruition.completion
                }:
                    del self._active[key]
                    self.sorter.done(key)
            except (AttributeError, KeyError, ValueError):
                continue

        self._active.update({i: self.drama.get(i) for i in self.sorter.get_ready()})
        return list(self._active.values())


class Exploration(Resident, Drama):

    def interlude(self, *args, **kwargs) -> Entity:
        self.speech.append(
            Epilogue("<> Guidance")
        )
        return super().interlude(*args, **kwargs)


class Interaction(Resident, SpeechTables, Drama):
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

