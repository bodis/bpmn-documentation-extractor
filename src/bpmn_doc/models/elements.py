"""Dataclasses for BPMN flow elements."""

from dataclasses import dataclass, field

from bpmn_doc.models.extensions import Extensions


@dataclass
class EventDefinition:
    def_type: str  # "message", "timer", "signal", "error", "escalation", etc.
    ref_id: str = ""
    ref_name: str = ""
    timer_expression: str = ""
    timer_expression_type: str = ""  # "timeDate", "timeDuration", "timeCycle"
    condition_expression: str = ""
    error_code: str = ""
    escalation_code: str = ""


@dataclass
class SequenceFlow:
    id: str
    source_ref: str
    target_ref: str
    name: str = ""
    condition_expression: str = ""
    annotations: list[str] = field(default_factory=list)


@dataclass
class LaneSet:
    id: str
    lanes: list["Lane"] = field(default_factory=list)


@dataclass
class Lane:
    id: str
    name: str = ""
    flow_node_refs: list[str] = field(default_factory=list)


@dataclass
class Task:
    id: str
    name: str
    task_type: str  # "serviceTask", "userTask", "sendTask", etc.
    documentation: str = ""
    annotations: list[str] = field(default_factory=list)
    camunda_class: str = ""
    camunda_expression: str = ""
    camunda_delegate_expression: str = ""
    camunda_type: str = ""
    camunda_topic: str = ""
    camunda_result_variable: str = ""
    camunda_async_before: bool = False
    camunda_async_after: bool = False
    called_element: str = ""  # for callActivity
    called_element_binding: str = ""
    called_element_version: str = ""
    extensions: Extensions = field(default_factory=Extensions)


@dataclass
class Event:
    id: str
    name: str
    event_type: str  # "startEvent", "endEvent", etc.
    documentation: str = ""
    annotations: list[str] = field(default_factory=list)
    event_definitions: list[EventDefinition] = field(default_factory=list)
    # boundary event fields
    attached_to_ref: str = ""
    cancel_activity: bool = True
    camunda_async_before: bool = False
    camunda_async_after: bool = False
    extensions: Extensions = field(default_factory=Extensions)


@dataclass
class Gateway:
    id: str
    name: str
    gateway_type: str  # "exclusiveGateway", "inclusiveGateway", etc.
    documentation: str = ""
    annotations: list[str] = field(default_factory=list)
    default_flow: str = ""
    gateway_direction: str = ""


@dataclass
class Subprocess:
    id: str
    name: str
    subprocess_type: str  # "subProcess", "transaction", "callActivity", "adHocSubProcess"
    documentation: str = ""
    annotations: list[str] = field(default_factory=list)
    triggered_by_event: bool = False
    camunda_async_before: bool = False
    camunda_async_after: bool = False
    tasks: list[Task] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)
    gateways: list[Gateway] = field(default_factory=list)
    subprocesses: list["Subprocess"] = field(default_factory=list)
    sequence_flows: list[SequenceFlow] = field(default_factory=list)
    lane_sets: list[LaneSet] = field(default_factory=list)
    extensions: Extensions = field(default_factory=Extensions)


@dataclass
class GlobalMessage:
    id: str
    name: str = ""


@dataclass
class GlobalSignal:
    id: str
    name: str = ""


@dataclass
class GlobalError:
    id: str
    name: str = ""
    error_code: str = ""


@dataclass
class GlobalEscalation:
    id: str
    name: str = ""
    escalation_code: str = ""


@dataclass
class Process:
    id: str
    name: str = ""
    is_executable: bool = False
    documentation: str = ""
    lane_sets: list[LaneSet] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)
    gateways: list[Gateway] = field(default_factory=list)
    subprocesses: list[Subprocess] = field(default_factory=list)
    sequence_flows: list[SequenceFlow] = field(default_factory=list)
    extensions: Extensions = field(default_factory=Extensions)


@dataclass
class Participant:
    id: str
    name: str = ""
    process_ref: str = ""


@dataclass
class Collaboration:
    id: str
    name: str = ""
    participants: list[Participant] = field(default_factory=list)
