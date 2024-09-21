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

from balladeer import Loader


class Resident:

    def __init__(self, *args, selector: dict[str, list] = {}, **kwargs):
        self.selector = selector | {"states": set(selector.get("states", []))}
        super().__init__(*args, **kwargs)

    def is_resident(self, *args: tuple[enum.Enum]):
        return all(str(i).lower() in self.selector["states"] for i in args)

    def scripts(self, assets: list):
        return [
            i for i in assets if isinstance(i, Loader.Scene) and any(i.path.match(p) for p in self.selector["paths"])
        ]
