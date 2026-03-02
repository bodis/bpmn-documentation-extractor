"""YAML renderer for BpmnDocument using dataclasses.asdict()."""

import dataclasses
from datetime import datetime

import yaml

from bpmn_doc.exceptions import BpmnRenderError
from bpmn_doc.models.document import BpmnDocument


def _make_serializable(obj: object) -> object:
    """Recursively convert dataclass instances and datetimes to plain dicts/strings."""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {k: _make_serializable(v) for k, v in dataclasses.asdict(obj).items()}
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, list):
        return [_make_serializable(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _make_serializable(v) for k, v in obj.items()}
    return obj


def render_yaml(doc: BpmnDocument) -> str:
    """
    Render a BpmnDocument to a YAML string.

    Args:
        doc: The parsed BPMN document.

    Returns:
        A YAML string.

    Raises:
        BpmnRenderError: If rendering fails.
    """
    try:
        data = _make_serializable(doc)
        return yaml.dump(
            data,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=120,
        )
    except Exception as e:
        raise BpmnRenderError(f"YAML rendering failed: {e}") from e
