"""Parser for BPMN event elements."""

from lxml import etree

from bpmn_doc.constants import (
    TAG_CANCEL_EVENT_DEF,
    TAG_COMPENSATE_EVENT_DEF,
    TAG_CONDITION,
    TAG_CONDITIONAL_EVENT_DEF,
    TAG_ERROR_EVENT_DEF,
    TAG_ESCALATION_EVENT_DEF,
    TAG_LINK_EVENT_DEF,
    TAG_MESSAGE_EVENT_DEF,
    TAG_SIGNAL_EVENT_DEF,
    TAG_TERMINATE_EVENT_DEF,
    TAG_TIME_CYCLE,
    TAG_TIME_DATE,
    TAG_TIME_DURATION,
    TAG_TIMER_EVENT_DEF,
)
from bpmn_doc.models.elements import Event, EventDefinition
from bpmn_doc.parser.common_parser import get_attr, get_bool_attr, local_tag, parse_documentation
from bpmn_doc.parser.extension_parser import parse_extensions

_EVENT_DEF_TYPE_MAP = {
    TAG_MESSAGE_EVENT_DEF: "message",
    TAG_TIMER_EVENT_DEF: "timer",
    TAG_SIGNAL_EVENT_DEF: "signal",
    TAG_ERROR_EVENT_DEF: "error",
    TAG_ESCALATION_EVENT_DEF: "escalation",
    TAG_COMPENSATE_EVENT_DEF: "compensate",
    TAG_CANCEL_EVENT_DEF: "cancel",
    TAG_CONDITIONAL_EVENT_DEF: "conditional",
    TAG_LINK_EVENT_DEF: "link",
    TAG_TERMINATE_EVENT_DEF: "terminate",
}


def _parse_event_definition(elem: etree._Element, id_map: dict[str, str]) -> EventDefinition | None:
    """Parse a single event definition child element."""
    def_type = _EVENT_DEF_TYPE_MAP.get(elem.tag)
    if def_type is None:
        return None

    ref_id = ""
    ref_name = ""
    timer_expression = ""
    timer_expression_type = ""
    condition_expression = ""
    error_code = ""
    escalation_code = ""

    if def_type == "message":
        ref_id = get_attr(elem, "messageRef")
        ref_name = id_map.get(ref_id, "")
    elif def_type == "signal":
        ref_id = get_attr(elem, "signalRef")
        ref_name = id_map.get(ref_id, "")
    elif def_type == "error":
        ref_id = get_attr(elem, "errorRef")
        ref_name = id_map.get(ref_id, "")
        error_code = get_attr(elem, "errorCode")
    elif def_type == "escalation":
        ref_id = get_attr(elem, "escalationRef")
        ref_name = id_map.get(ref_id, "")
        escalation_code = get_attr(elem, "escalationCode")
    elif def_type == "timer":
        for child in elem:
            if child.tag == TAG_TIME_DATE:
                timer_expression = (child.text or "").strip()
                timer_expression_type = "timeDate"
            elif child.tag == TAG_TIME_DURATION:
                timer_expression = (child.text or "").strip()
                timer_expression_type = "timeDuration"
            elif child.tag == TAG_TIME_CYCLE:
                timer_expression = (child.text or "").strip()
                timer_expression_type = "timeCycle"
    elif def_type == "conditional":
        for child in elem:
            if child.tag == TAG_CONDITION:
                condition_expression = (child.text or "").strip()

    return EventDefinition(
        def_type=def_type,
        ref_id=ref_id,
        ref_name=ref_name,
        timer_expression=timer_expression,
        timer_expression_type=timer_expression_type,
        condition_expression=condition_expression,
        error_code=error_code,
        escalation_code=escalation_code,
    )


def parse_event(element: etree._Element, id_map: dict[str, str]) -> Event:
    """Parse a BPMN event element of any type."""
    event_type = local_tag(element)
    event_defs: list[EventDefinition] = []

    from bpmn_doc.constants import EVENT_DEF_TAGS
    for child in element:
        if child.tag in EVENT_DEF_TAGS:
            ed = _parse_event_definition(child, id_map)
            if ed is not None:
                event_defs.append(ed)

    cancel_activity_str = element.get("cancelActivity", "true")
    cancel_activity = cancel_activity_str.lower() not in ("false", "0")

    return Event(
        id=get_attr(element, "id"),
        name=get_attr(element, "name"),
        event_type=event_type,
        documentation=parse_documentation(element),
        event_definitions=event_defs,
        attached_to_ref=get_attr(element, "attachedToRef"),
        cancel_activity=cancel_activity,
        camunda_async_before=get_bool_attr(element, "{http://camunda.org/schema/1.0/bpmn}asyncBefore"),
        camunda_async_after=get_bool_attr(element, "{http://camunda.org/schema/1.0/bpmn}asyncAfter"),
        extensions=parse_extensions(element),
    )
