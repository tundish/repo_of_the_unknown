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
from rotu.strand import Rule
from rotu.strand import Strand
from rotu.strand import Task


class Puzzle(Drama):
    def __init__(self, *args, **kwargs):
        self.rules = kwargs.pop("rules", [])
        super().__init__(*args, **kwargs)


strands = [
    Strand(
        label="Get Gigging",
        tasks=[
            Task(
                label="tracker manual page 1",
                prior=[],
                drama=Puzzle(
                    rules=[
                        Rule(name="van_f_ext", terms=["in front of the van"]),
                        Rule(name="van_f_int", terms=["in the van"]),
                        Rule(name="van_b_ext", terms=["behind the van"]),
                        Rule(name="van_b_int", terms=["in the back of the van"]),
                        Rule(name="car_park", terms=["car park"]),
                        Rule(name="cafe_f_ext", terms=["in front of the cafe"]),
                        Rule(name="shed_f_ext", terms=["in front of the shed"]),
                        Rule(name="shed_f_int", terms=["inside the shed"]),
                        Rule(name="shed_b_int", terms=["back of the shed"]),
                        Rule(name="roadside", terms=["by the roadside"]),
                    ],
                ),
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
                items = [
                ],
            ),
        ],
    )
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
