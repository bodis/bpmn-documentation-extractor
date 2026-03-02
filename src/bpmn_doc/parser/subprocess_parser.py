"""Parser for BPMN subprocess elements (recursive)."""

from __future__ import annotations

from lxml import etree

from bpmn_doc.models.elements import Subprocess
from bpmn_doc.parser.common_parser import get_attr, get_bool_attr, local_tag, parse_documentation
from bpmn_doc.parser.extension_parser import parse_extensions


def parse_subprocess(element: etree._Element, id_map: dict[str, str]) -> Subprocess:
    """Parse a BPMN subProcess, transaction, or adHocSubProcess element (recursive)."""
    # Import here to avoid circular imports
    from bpmn_doc.parser.flow_element_parser import parse_flow_elements

    subprocess_type = local_tag(element)
    tasks, events, gateways, subprocesses, sequence_flows, lane_sets = parse_flow_elements(element, id_map)

    return Subprocess(
        id=get_attr(element, "id"),
        name=get_attr(element, "name"),
        subprocess_type=subprocess_type,
        documentation=parse_documentation(element),
        triggered_by_event=get_bool_attr(element, "triggeredByEvent"),
        camunda_async_before=get_bool_attr(element, "{http://camunda.org/schema/1.0/bpmn}asyncBefore"),
        camunda_async_after=get_bool_attr(element, "{http://camunda.org/schema/1.0/bpmn}asyncAfter"),
        tasks=tasks,
        events=events,
        gateways=gateways,
        subprocesses=subprocesses,
        sequence_flows=sequence_flows,
        lane_sets=lane_sets,
        extensions=parse_extensions(element),
    )
