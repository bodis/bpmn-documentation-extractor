"""Common helper functions for BPMN parsing."""

from lxml import etree

from bpmn_doc.constants import BPMN_NS, TAG_DOCUMENTATION


def local_tag(element: etree._Element) -> str:
    """Return the local name of an element (without namespace)."""
    tag = element.tag
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


def get_attr(element: etree._Element, attr: str, default: str = "") -> str:
    """Get an attribute value with a default."""
    return element.get(attr, default) or default


def get_bool_attr(element: etree._Element, attr: str, default: bool = False) -> bool:
    """Get a boolean attribute value."""
    val = element.get(attr, "").lower()
    if val in ("true", "1", "yes"):
        return True
    if val in ("false", "0", "no"):
        return False
    return default


def parse_documentation(element: etree._Element) -> str:
    """Extract the text content of the first bpmn:documentation child element."""
    for child in element:
        if child.tag == TAG_DOCUMENTATION:
            text = child.text or ""
            return text.strip()
    return ""


def build_id_map(root: etree._Element) -> dict[str, str]:
    """
    Walk the entire XML tree and collect id -> name mappings.
    Used to resolve refs like messageRef, signalRef, errorRef.
    """
    id_map: dict[str, str] = {}
    for elem in root.iter():
        elem_id = elem.get("id")
        if elem_id:
            name = elem.get("name", "")
            id_map[elem_id] = name
    return id_map


def clark(ns: str, local: str) -> str:
    """Build a Clark-notation tag string."""
    return f"{{{ns}}}{local}"
