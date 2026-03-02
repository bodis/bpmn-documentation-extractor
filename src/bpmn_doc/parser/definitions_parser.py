"""Parser for top-level definitions children (process, collaboration, globals)."""

from lxml import etree

from bpmn_doc.constants import (
    TAG_COLLABORATION,
    TAG_ERROR,
    TAG_ESCALATION,
    TAG_MESSAGE,
    TAG_PARTICIPANT,
    TAG_PROCESS,
    TAG_SIGNAL,
)
from bpmn_doc.models.elements import (
    Collaboration,
    GlobalError,
    GlobalEscalation,
    GlobalMessage,
    GlobalSignal,
    Participant,
    Process,
)
from bpmn_doc.parser.common_parser import get_attr, get_bool_attr, parse_documentation
from bpmn_doc.parser.extension_parser import parse_extensions
from bpmn_doc.parser.flow_element_parser import parse_flow_elements


def parse_process(elem: etree._Element, id_map: dict[str, str]) -> Process:
    """Parse a bpmn:process element."""
    tasks, events, gateways, subprocesses, sequence_flows, lane_sets = parse_flow_elements(elem, id_map)
    return Process(
        id=get_attr(elem, "id"),
        name=get_attr(elem, "name"),
        is_executable=get_bool_attr(elem, "isExecutable"),
        documentation=parse_documentation(elem),
        lane_sets=lane_sets,
        tasks=tasks,
        events=events,
        gateways=gateways,
        subprocesses=subprocesses,
        sequence_flows=sequence_flows,
        extensions=parse_extensions(elem),
    )


def parse_collaboration(elem: etree._Element) -> Collaboration:
    """Parse a bpmn:collaboration element."""
    participants: list[Participant] = []
    for child in elem:
        if child.tag == TAG_PARTICIPANT:
            participants.append(Participant(
                id=get_attr(child, "id"),
                name=get_attr(child, "name"),
                process_ref=get_attr(child, "processRef"),
            ))
    return Collaboration(
        id=get_attr(elem, "id"),
        name=get_attr(elem, "name"),
        participants=participants,
    )


def parse_global_message(elem: etree._Element) -> GlobalMessage:
    return GlobalMessage(id=get_attr(elem, "id"), name=get_attr(elem, "name"))


def parse_global_signal(elem: etree._Element) -> GlobalSignal:
    return GlobalSignal(id=get_attr(elem, "id"), name=get_attr(elem, "name"))


def parse_global_error(elem: etree._Element) -> GlobalError:
    return GlobalError(
        id=get_attr(elem, "id"),
        name=get_attr(elem, "name"),
        error_code=get_attr(elem, "errorCode"),
    )


def parse_global_escalation(elem: etree._Element) -> GlobalEscalation:
    return GlobalEscalation(
        id=get_attr(elem, "id"),
        name=get_attr(elem, "name"),
        escalation_code=get_attr(elem, "escalationCode"),
    )
