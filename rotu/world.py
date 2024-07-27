from collections.abc import Generator
import operator

from balladeer import Drama
from balladeer import Entity
from balladeer import Fruition
from balladeer import MapBuilder
from balladeer import Traffic
from balladeer import Transit
from balladeer import WorldBuilder


from rotu.drama import Exploration
from rotu.drama import Interaction


class Map(MapBuilder):

    def build(self, base=[], **kwargs):
        yield from base
        yield from [
            Transit(type="Void").set_state(self.exit.cafe_f_ext, self.into.car_park, Traffic.flowing),
            Transit(type="Void").set_state(self.exit.car_park, self.into.shed_f_ext, Traffic.flowing),
            Transit(type="Void").set_state(self.exit.shed_f_ext, self.into.shed_f_int, Traffic.flowing),
            Transit(type="Void").set_state(self.exit.shed_f_int, self.into.shed_b_int, Traffic.flowing),
            Transit(type="Void").set_state(self.exit.car_park, self.into.van_f_ext, Traffic.flowing),
            Transit(type="View").set_state(self.exit.van_f_int, self.into.van_b_int, Traffic.blocked),
            Transit(
                names=["Door", "Van door"], type="Door", aspect="unlocked", sketch="The {0.name} is {aspect}"
            ).set_state(self.exit.van_f_ext, self.into.van_f_int, Traffic.flowing),
            Transit(type="Void").set_state(self.exit.car_park, self.into.van_b_ext, Traffic.flowing),
            Transit(type="Void").set_state(self.exit.van_b_ext, self.into.van_b_int, Traffic.flowing),
            Transit(type="Void").set_state(self.exit.van_b_ext, self.into.roadside, Traffic.flowing),
        ]


class World(WorldBuilder):
    specs = set()

    # Move to Puzzle
    @property
    def focus(self):
        return next((reversed(sorted(self.typewise["Focus"], key=operator.attrgetter("state")))), None)

    def build(self, **kwargs) -> Generator[Entity]:
        yield Entity(type="Focus").set_state(self.map.spot.van_f_int)
        for entity in self.build_to_spec(self.specs):
            if entity.names and "Goal" in entity.types:
                if "goal_00a" in entity.names:
                    yield entity.set_state(Fruition.elaboration)
                else:
                    yield entity.set_state(Fruition.inception)
