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
from rotu.puzzle import Puzzle
from rotu.puzzle import Strand


strands = [
    Strand(
        label="Get Gigging",
        drama=[
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
                # TODO: yield from setup method
                rules=(
                    Puzzle.Rule(type="Transit", states=("exit.cafe_f_ext", "into.car_park", Traffic.flowing)),
                    Puzzle.Rule(type="Transit", states=("exit.car_park", "into.shed_f_ext", Traffic.flowing)),
                    Puzzle.Rule(type="Transit", states=("exit.shed_f_ext", "into.shed_f_int", Traffic.flowing)),
                    Puzzle.Rule(type="Transit", states=("exit.shed_f_int", "into.shed_b_int", Traffic.flowing)),
                    Puzzle.Rule(type="Transit", states=("exit.car_park", "into.van_f_ext", Traffic.flowing)),
                    Puzzle.Rule(type="Transit", states=("exit.van_f_int", "into.van_b_int", Traffic.blocked)),
                    Puzzle.Rule(
                        names=("Door", "Van door"), type="Door", aspect="unlocked", sketch="The {0.name} is {aspect}",
                        states=("exit.van_f_ext", "into.van_f_int", Traffic.flowing)
                    ),
                    Puzzle.Rule(type="Void", states=("exit.car_park", "into.van_b_ext", Traffic.flowing)),
                    Puzzle.Rule(type="Void", states=("exit.van_b_ext", "into.van_b_int", Traffic.flowing)),
                    Puzzle.Rule(type="Void", states=("exit.van_b_ext", "into.roadside", Traffic.flowing)),
                ),
            ),
            Puzzle(
                name="collect tracker samples",
                links={"tracker manual page 1"},
                rules=[
                ],
            ),
        ],
    ),
]


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
