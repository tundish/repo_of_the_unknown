from collections.abc import Generator
import functools
import re
import textwrap

from balladeer import Page
from balladeer import Session
from balladeer import StoryBuilder
from balladeer import Turn


class StorySession(Session):

    code_matcher = re.compile(f"(<code.*?>)(.*?)(<\\/code>)", re.DOTALL)

    @staticmethod
    def convert_code_into_action(match: re.Match, request=None, story=None, turn=None, page = None):
        text = f"{match[2]}".replace(" ", "-")
        try:
            url = request.url_for("command", session_id=story.uid)
            form = textwrap.dedent(f"""
            <form role="form" action="{url}" method="post" id="ballad-action-form-{text}" class="ballad action">
            <input type="hidden" name="ballad-command-form-input-text" value="{match[2]}" />
            </form>
            """)
            page.paste(form, zone=page.zone.inputs)
        except AttributeError:
            pass
        return f'<button form="ballad-action-form-{text}" class="ballad action" type="submit">{match[2]}</button>'

    def render_cues(
        self, request, story: StoryBuilder = None, turn: Turn = None, page: Page = None
    ) -> Generator[str]:
        for cue_block in super().render_cues(request, story, turn):
            func = functools.partial(self.convert_code_into_action, request=request, story=story, turn=turn, page=page)
            yield self.code_matcher.sub(func, cue_block)

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


