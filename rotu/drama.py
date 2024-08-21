from balladeer import Detail
from balladeer import Drama
from balladeer import Entity
from balladeer import Epilogue
from balladeer.lite.types import Fruition
from balladeer import Prologue
from balladeer import SpeechTables


class Resident:

    def __init__(self, *args, selector={}, **kwargs):
        self.selector = selector
        super().__init__(*args, **kwargs)

    # TODO: accept selector in __init__
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

