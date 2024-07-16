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

import dataclasses

from balladeer import Drama


@dataclasses.dataclass
class Rule:
    name: str
    terms: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Task:
    label: str
    prior: list[str] = dataclasses.field(default_factory=list)
    drama: Drama = None
    items: list[dict] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Strand:
    label: str
    tasks: list[Task] = dataclasses.field(default_factory=list)


class Puzzle(Drama):
    def __init__(self, *args, **kwargs):
        self.spots = tuple(kwargs.pop("spots", {}).items())
        super().__init__(*args, **kwargs)


