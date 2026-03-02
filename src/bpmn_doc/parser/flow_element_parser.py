"""Dispatch loop over process/subprocess children."""

from __future__ import annotations

from lxml import etree

from bpmn_doc.constants import (
    EVENT_TAGS,
    GATEWAY_TAGS,
    SUBPROCESS_TAGS,
    TAG_ASSOCIATION,
    TAG_CONDITION_EXPRESSION,
    TAG_FLOW_NODE_REF,
    TAG_LANE,
    TAG_LANE_SET,
    TAG_SEQUENCE_FLOW,
    TAG_TEXT,
    TAG_TEXT_ANNOTATION,
    TASK_TAGS,
)
from bpmn_doc.models.elements import (
    Event,
    Gateway,
    Lane,
    LaneSet,
    SequenceFlow,
    Subprocess,
    Task,
)
from bpmn_doc.parser.common_parser import get_attr
from bpmn_doc.parser.event_parser import parse_event
from bpmn_doc.parser.gateway_parser import parse_gateway
from bpmn_doc.parser.subprocess_parser import parse_subprocess
from bpmn_doc.parser.task_parser import parse_task


def _parse_lane_set(lane_set_elem: etree._Element) -> LaneSet:
    """Parse a bpmn:laneSet element."""
    lanes: list[Lane] = []
    for child in lane_set_elem:
        if child.tag == TAG_LANE:
            lane_id = get_attr(child, "id")
            lane_name = get_attr(child, "name")
            refs: list[str] = []
            for ref_elem in child:
                if ref_elem.tag == TAG_FLOW_NODE_REF:
                    refs.append((ref_elem.text or "").strip())
            lanes.append(Lane(id=lane_id, name=lane_name, flow_node_refs=refs))
    return LaneSet(id=get_attr(lane_set_elem, "id"), lanes=lanes)


def parse_flow_elements(
    container: etree._Element,
    id_map: dict[str, str],
) -> tuple[
    list[Task],
    list[Event],
    list[Gateway],
    list[Subprocess],
    list[SequenceFlow],
    list[LaneSet],
]:
    """
    Walk direct children of a process or subprocess container.
    Returns (tasks, events, gateways, subprocesses, sequence_flows, lane_sets).
    """
    tasks: list[Task] = []
    events: list[Event] = []
    gateways: list[Gateway] = []
    subprocesses: list[Subprocess] = []
    sequence_flows: list[SequenceFlow] = []
    lane_sets: list[LaneSet] = []
    annotation_texts: dict[str, str] = {}       # annotation_id -> text
    associations: list[tuple[str, str]] = []    # (source_element_id, annotation_id)

    for child in container:
        tag = child.tag
        if tag in TASK_TAGS:
            tasks.append(parse_task(child))
        elif tag in EVENT_TAGS:
            events.append(parse_event(child, id_map))
        elif tag in GATEWAY_TAGS:
            gateways.append(parse_gateway(child))
        elif tag in SUBPROCESS_TAGS:
            subprocesses.append(parse_subprocess(child, id_map))
        elif tag == TAG_SEQUENCE_FLOW:
            sf = _parse_sequence_flow(child)
            sequence_flows.append(sf)
        elif tag == TAG_LANE_SET:
            lane_sets.append(_parse_lane_set(child))
        elif tag == TAG_TEXT_ANNOTATION:
            text_elem = child.find(TAG_TEXT)
            if text_elem is not None and text_elem.text:
                annotation_texts[child.get("id", "")] = text_elem.text.strip()
        elif tag == TAG_ASSOCIATION:
            src = child.get("sourceRef", "")
            tgt = child.get("targetRef", "")
            if src and tgt:
                associations.append((src, tgt))

    # Build element_id -> [annotation texts]
    annotation_map: dict[str, list[str]] = {}
    for src, tgt in associations:
        text = annotation_texts.get(tgt)
        if text:
            annotation_map.setdefault(src, []).append(text)

    # Attach annotations to all parsed elements in-place
    for elem in [*tasks, *events, *gateways, *subprocesses, *sequence_flows]:
        texts = annotation_map.get(elem.id, [])
        if texts:
            elem.annotations.extend(texts)

    return tasks, events, gateways, subprocesses, sequence_flows, lane_sets


def _parse_sequence_flow(elem: etree._Element) -> SequenceFlow:
    """Parse a bpmn:sequenceFlow element."""
    condition = ""
    for child in elem:
        if child.tag == TAG_CONDITION_EXPRESSION:
            condition = (child.text or "").strip()
    return SequenceFlow(
        id=get_attr(elem, "id"),
        source_ref=get_attr(elem, "sourceRef"),
        target_ref=get_attr(elem, "targetRef"),
        name=get_attr(elem, "name"),
        condition_expression=condition,
    )
