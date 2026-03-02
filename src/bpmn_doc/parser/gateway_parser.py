"""Parser for BPMN gateway elements."""

from lxml import etree

from bpmn_doc.models.elements import Gateway
from bpmn_doc.parser.common_parser import get_attr, local_tag, parse_documentation


def parse_gateway(element: etree._Element) -> Gateway:
    """Parse a BPMN gateway element of any type."""
    return Gateway(
        id=get_attr(element, "id"),
        name=get_attr(element, "name"),
        gateway_type=local_tag(element),
        documentation=parse_documentation(element),
        default_flow=get_attr(element, "default"),
        gateway_direction=get_attr(element, "gatewayDirection"),
    )
