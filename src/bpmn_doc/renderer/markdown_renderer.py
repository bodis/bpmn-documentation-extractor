"""Jinja2-based Markdown renderer for BpmnDocument."""

import re

from jinja2 import Environment, PackageLoader, select_autoescape

from bpmn_doc.exceptions import BpmnRenderError
from bpmn_doc.models.document import BpmnDocument


def _clean_blank_lines(text: str) -> str:
    """Collapse more than two consecutive blank lines into two."""
    return re.sub(r"\n{3,}", "\n\n", text)


def render_markdown(doc: BpmnDocument) -> str:
    """
    Render a BpmnDocument to a Markdown string.

    Args:
        doc: The parsed BPMN document.

    Returns:
        A Markdown string.

    Raises:
        BpmnRenderError: If rendering fails.
    """
    try:
        env = Environment(
            loader=PackageLoader("bpmn_doc", "renderer/templates"),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
        # Make 'unique' filter available
        env.filters["unique"] = lambda it: list(dict.fromkeys(it))

        tmpl = env.get_template("document.md.j2")
        result = tmpl.render(doc=doc)
        return _clean_blank_lines(result)
    except Exception as e:
        raise BpmnRenderError(f"Markdown rendering failed: {e}") from e
