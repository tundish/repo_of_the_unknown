from collections.abc import Generator

from balladeer import Entity
from balladeer.lite.types import Fruition
from balladeer import MapBuilder
from balladeer import Traffic
from balladeer import Transit
from balladeer import WorldBuilder


class Map(MapBuilder):
    spots = {
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


class World(WorldBuilder):
    def build(self) -> Generator[Entity]:
        yield Entity(type="Focus").set_state(self.map.spot.van_f_int)
        for entity in self.build_to_spec(self.specs):
            if entity.names and "Goal" in entity.types:
                if "goal_00a" in entity.names:
                    yield entity.set_state(Fruition.elaboration)
                else:
                    yield entity.set_state(Fruition.inception)
