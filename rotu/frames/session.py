from collections.abc import Generator
import functools
import re
import textwrap

from balladeer import Page
from balladeer import Session
from balladeer import StoryBuilder
from balladeer import Turn


class StorySession(Session):

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


