"""Namespace URIs and Clark-notation tag helpers."""

BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
CAMUNDA_NS = "http://camunda.org/schema/1.0/bpmn"
EING_NS = "http://eing.tigra.hu/schema/bpmn/eing"
DC_NS = "http://www.omg.org/spec/DD/20100524/DC"
DI_NS = "http://www.omg.org/spec/DD/20100524/DI"
BPMNDI_NS = "http://www.omg.org/spec/BPMN/20100524/DI"

NS = {
    "bpmn": BPMN_NS,
    "camunda": CAMUNDA_NS,
    "eing": EING_NS,
}


def BPMN(name: str) -> str:
    return f"{{{BPMN_NS}}}{name}"


def CAMUNDA(name: str) -> str:
    return f"{{{CAMUNDA_NS}}}{name}"


def EING(name: str) -> str:
    return f"{{{EING_NS}}}{name}"


# Pre-built Clark tags for common BPMN elements
TAG_DEFINITIONS = BPMN("definitions")
TAG_COLLABORATION = BPMN("collaboration")
TAG_PARTICIPANT = BPMN("participant")
TAG_PROCESS = BPMN("process")
TAG_LANE_SET = BPMN("laneSet")
TAG_LANE = BPMN("lane")
TAG_FLOW_NODE_REF = BPMN("flowNodeRef")
TAG_DOCUMENTATION = BPMN("documentation")
TAG_EXTENSION_ELEMENTS = BPMN("extensionElements")
TAG_SEQUENCE_FLOW = BPMN("sequenceFlow")
TAG_CONDITION_EXPRESSION = BPMN("conditionExpression")

# Task tags
TAG_TASK = BPMN("task")
TAG_SERVICE_TASK = BPMN("serviceTask")
TAG_USER_TASK = BPMN("userTask")
TAG_SEND_TASK = BPMN("sendTask")
TAG_RECEIVE_TASK = BPMN("receiveTask")
TAG_SCRIPT_TASK = BPMN("scriptTask")
TAG_BUSINESS_RULE_TASK = BPMN("businessRuleTask")
TAG_MANUAL_TASK = BPMN("manualTask")
TAG_CALL_ACTIVITY = BPMN("callActivity")

TASK_TAGS = {
    TAG_TASK,
    TAG_SERVICE_TASK,
    TAG_USER_TASK,
    TAG_SEND_TASK,
    TAG_RECEIVE_TASK,
    TAG_SCRIPT_TASK,
    TAG_BUSINESS_RULE_TASK,
    TAG_MANUAL_TASK,
    TAG_CALL_ACTIVITY,
}

# Event tags
TAG_START_EVENT = BPMN("startEvent")
TAG_END_EVENT = BPMN("endEvent")
TAG_INTERMEDIATE_CATCH_EVENT = BPMN("intermediateCatchEvent")
TAG_INTERMEDIATE_THROW_EVENT = BPMN("intermediateThrowEvent")
TAG_BOUNDARY_EVENT = BPMN("boundaryEvent")

EVENT_TAGS = {
    TAG_START_EVENT,
    TAG_END_EVENT,
    TAG_INTERMEDIATE_CATCH_EVENT,
    TAG_INTERMEDIATE_THROW_EVENT,
    TAG_BOUNDARY_EVENT,
}

# Event definition tags
TAG_MESSAGE_EVENT_DEF = BPMN("messageEventDefinition")
TAG_TIMER_EVENT_DEF = BPMN("timerEventDefinition")
TAG_SIGNAL_EVENT_DEF = BPMN("signalEventDefinition")
TAG_ERROR_EVENT_DEF = BPMN("errorEventDefinition")
TAG_ESCALATION_EVENT_DEF = BPMN("escalationEventDefinition")
TAG_COMPENSATE_EVENT_DEF = BPMN("compensateEventDefinition")
TAG_CANCEL_EVENT_DEF = BPMN("cancelEventDefinition")
TAG_CONDITIONAL_EVENT_DEF = BPMN("conditionalEventDefinition")
TAG_LINK_EVENT_DEF = BPMN("linkEventDefinition")
TAG_TERMINATE_EVENT_DEF = BPMN("terminateEventDefinition")

EVENT_DEF_TAGS = {
    TAG_MESSAGE_EVENT_DEF,
    TAG_TIMER_EVENT_DEF,
    TAG_SIGNAL_EVENT_DEF,
    TAG_ERROR_EVENT_DEF,
    TAG_ESCALATION_EVENT_DEF,
    TAG_COMPENSATE_EVENT_DEF,
    TAG_CANCEL_EVENT_DEF,
    TAG_CONDITIONAL_EVENT_DEF,
    TAG_LINK_EVENT_DEF,
    TAG_TERMINATE_EVENT_DEF,
}

# Gateway tags
TAG_EXCLUSIVE_GATEWAY = BPMN("exclusiveGateway")
TAG_INCLUSIVE_GATEWAY = BPMN("inclusiveGateway")
TAG_PARALLEL_GATEWAY = BPMN("parallelGateway")
TAG_EVENT_BASED_GATEWAY = BPMN("eventBasedGateway")
TAG_COMPLEX_GATEWAY = BPMN("complexGateway")

GATEWAY_TAGS = {
    TAG_EXCLUSIVE_GATEWAY,
    TAG_INCLUSIVE_GATEWAY,
    TAG_PARALLEL_GATEWAY,
    TAG_EVENT_BASED_GATEWAY,
    TAG_COMPLEX_GATEWAY,
}

# Subprocess tags
TAG_SUBPROCESS = BPMN("subProcess")
TAG_TRANSACTION = BPMN("transaction")
TAG_AD_HOC_SUBPROCESS = BPMN("adHocSubProcess")

SUBPROCESS_TAGS = {
    TAG_SUBPROCESS,
    TAG_TRANSACTION,
    TAG_AD_HOC_SUBPROCESS,
}

# Global definition tags
TAG_MESSAGE = BPMN("message")
TAG_SIGNAL = BPMN("signal")
TAG_ERROR = BPMN("error")
TAG_ESCALATION = BPMN("escalation")

# Timer sub-expressions
TAG_TIME_DATE = BPMN("timeDate")
TAG_TIME_DURATION = BPMN("timeDuration")
TAG_TIME_CYCLE = BPMN("timeCycle")
TAG_CONDITION = BPMN("condition")

# Camunda extension tags
TAG_CAMUNDA_INPUT_OUTPUT = CAMUNDA("inputOutput")
TAG_CAMUNDA_INPUT_PARAMETER = CAMUNDA("inputParameter")
TAG_CAMUNDA_OUTPUT_PARAMETER = CAMUNDA("outputParameter")
TAG_CAMUNDA_EXECUTION_LISTENER = CAMUNDA("executionListener")
TAG_CAMUNDA_FIELD = CAMUNDA("field")
TAG_CAMUNDA_STRING = CAMUNDA("string")
TAG_CAMUNDA_EXPRESSION_TAG = CAMUNDA("expression")
TAG_CAMUNDA_IN = CAMUNDA("in")
TAG_CAMUNDA_OUT = CAMUNDA("out")
TAG_CAMUNDA_LIST = CAMUNDA("list")
TAG_CAMUNDA_VALUE = CAMUNDA("value")
TAG_CAMUNDA_MAP = CAMUNDA("map")
TAG_CAMUNDA_ENTRY = CAMUNDA("entry")

# Eing extension tags
TAG_EING_TEMPLATE_REGISTRY = EING("templateRegistry")
TAG_EING_TEMPLATE = EING("template")
TAG_EING_JSON_SOURCES = EING("jsonSources")
TAG_EING_JSON_SOURCE = EING("jsonSource")

# Annotation tags
TAG_TEXT_ANNOTATION = BPMN("textAnnotation")
TAG_TEXT = BPMN("text")
TAG_ASSOCIATION = BPMN("association")
