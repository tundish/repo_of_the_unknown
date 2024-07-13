from collections.abc import Generator
import operator

from balladeer import Entity
from balladeer.lite.types import Fruition
from balladeer import MapBuilder
from balladeer import Traffic
from balladeer import Transit
from balladeer import WorldBuilder


from rotu.drama import Exploration
from rotu.drama import Interaction
from rotu.strand import Rule
from rotu.strand import Strand
from rotu.strand import Task


strands = [
    Strand(
        label="Get Gigging",
        tasks=[
            Task(
                label="tracker manual page 1",
                prior=[],
                rules = [
                    Rule(name="van_f_ext", terms=["in front of the van"], stack=[dict(type=Exploration, states=[0])]),
                    Rule(name="van_f_int", terms=["in the van"], stack=[dict(type=Exploration, states=[0])]),
                    Rule(name="van_b_ext", terms=["behind the van"], stack=[dict(type=Exploration, states=[0])]),
                    Rule(name="van_b_int", terms=["in the back of the van"], stack=[dict(type=Exploration, states=[0])]),
                    Rule(name="car_park", terms=["car park"], stack=[dict(type=Exploration, states=[0])]),
                    Rule(name="cafe_f_ext", terms=["in front of the cafe"], stack=[dict(type=Exploration, states=[0])]),
                    Rule(name="shed_f_ext", terms=["in front of the shed"], stack=[dict(type=Exploration, states=[0])]),
                    Rule(name="shed_f_int", terms=["inside the shed"], stack=[dict(type=Exploration, states=[0])]),
                    Rule(name="shed_b_int", terms=["back of the shed"], stack=[dict(type=Exploration, states=[0])]),
                    Rule(name="roadside", terms=["by the roadside"], stack=[dict(type=Exploration, states=[0])]),
                ],
                items = [
                    dict(type="Void", states=["exit.cafe_f_ext", "into.car_park", Traffic.flowing]),
                    dict(type="Void", states=["exit.car_park", "into.shed_f_ext", Traffic.flowing]),
                    dict(type="Void", states=["exit.shed_f_ext", "into.shed_f_int", Traffic.flowing]),
                    dict(type="Void", states=["exit.shed_f_int", "into.shed_b_int", Traffic.flowing]),
                    dict(type="Void", states=["exit.car_park", "into.van_f_ext", Traffic.flowing]),
                    dict(type="View", states=["exit.van_f_int", "into.van_b_int", Traffic.blocked]),
                    dict(
                        names=["Door", "Van door"], type="Door", aspect="unlocked", sketch="The {0.name} is {aspect}",
                        states=["exit.van_f_ext", "into.van_f_int", Traffic.flowing]
                    ),
                    dict(type="Void", states=["exit.car_park", "into.van_b_ext", Traffic.flowing]),
                    dict(type="Void", states=["exit.van_b_ext", "into.van_b_int", Traffic.flowing]),
                    dict(type="Void", states=["exit.van_b_ext", "into.roadside", Traffic.flowing]),
                ],
            ),
            Task(
                label="collect tracker samples",
                prior=["tracker manual page 1"],
                rules = [],
                items = [
                ],
            ),
        ],
    )
]


class Map(MapBuilder):

    def build(self, base=[]):
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

    def build(self) -> Generator[Entity]:
        yield Entity(type="Focus").set_state(self.map.spot.van_f_int)
        for entity in self.build_to_spec(self.specs):
            if entity.names and "Goal" in entity.types:
                if "goal_00a" in entity.names:
                    yield entity.set_state(Fruition.elaboration)
                else:
                    yield entity.set_state(Fruition.inception)
