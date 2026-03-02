"""Parser for BPMN task elements."""

from lxml import etree

from bpmn_doc.models.elements import Task
from bpmn_doc.parser.common_parser import get_attr, get_bool_attr, local_tag, parse_documentation
from bpmn_doc.parser.extension_parser import parse_extensions


def parse_task(element: etree._Element) -> Task:
    """Parse a BPMN task element of any type."""
    task_type = local_tag(element)
    return Task(
        id=get_attr(element, "id"),
        name=get_attr(element, "name"),
        task_type=task_type,
        documentation=parse_documentation(element),
        camunda_class=get_attr(element, "{http://camunda.org/schema/1.0/bpmn}class"),
        camunda_expression=get_attr(element, "{http://camunda.org/schema/1.0/bpmn}expression"),
        camunda_delegate_expression=get_attr(element, "{http://camunda.org/schema/1.0/bpmn}delegateExpression"),
        camunda_type=get_attr(element, "{http://camunda.org/schema/1.0/bpmn}type"),
        camunda_topic=get_attr(element, "{http://camunda.org/schema/1.0/bpmn}topic"),
        camunda_result_variable=get_attr(element, "{http://camunda.org/schema/1.0/bpmn}resultVariable"),
        camunda_async_before=get_bool_attr(element, "{http://camunda.org/schema/1.0/bpmn}asyncBefore"),
        camunda_async_after=get_bool_attr(element, "{http://camunda.org/schema/1.0/bpmn}asyncAfter"),
        called_element=get_attr(element, "calledElement"),
        called_element_binding=get_attr(element, "{http://camunda.org/schema/1.0/bpmn}calledElementBinding"),
        called_element_version=get_attr(element, "{http://camunda.org/schema/1.0/bpmn}calledElementVersion"),
        extensions=parse_extensions(element),
    )
