"""Parser for Camunda and eing extension elements."""

from lxml import etree

from bpmn_doc.constants import (
    TAG_CAMUNDA_ENTRY,
    TAG_CAMUNDA_EXECUTION_LISTENER,
    TAG_CAMUNDA_EXPRESSION_TAG,
    TAG_CAMUNDA_FIELD,
    TAG_CAMUNDA_IN,
    TAG_CAMUNDA_INPUT_OUTPUT,
    TAG_CAMUNDA_INPUT_PARAMETER,
    TAG_CAMUNDA_LIST,
    TAG_CAMUNDA_MAP,
    TAG_CAMUNDA_OUT,
    TAG_CAMUNDA_OUTPUT_PARAMETER,
    TAG_CAMUNDA_STRING,
    TAG_CAMUNDA_VALUE,
    TAG_EING_JSON_SOURCE,
    TAG_EING_JSON_SOURCES,
    TAG_EING_TEMPLATE,
    TAG_EING_TEMPLATE_REGISTRY,
    TAG_EXTENSION_ELEMENTS,
)
from bpmn_doc.models.extensions import (
    CallActivityMapping,
    EingJsonSource,
    EingTemplate,
    EingTemplateRegistry,
    ExecutionListener,
    ExecutionListenerField,
    Extensions,
    InputParameter,
    OutputParameter,
)
from bpmn_doc.parser.common_parser import get_attr


def _parse_parameter_value(param_elem: etree._Element) -> tuple[str, bool]:
    """
    Parse a camunda:inputParameter or camunda:outputParameter element.
    Returns (value_string, is_expression).
    """
    # Check for child elements first
    children = list(param_elem)
    if not children:
        # Simple text value
        return (param_elem.text or "").strip(), False

    # Check for expression child
    for child in children:
        if child.tag == TAG_CAMUNDA_EXPRESSION_TAG:
            return (child.text or "").strip(), True
        if child.tag == TAG_CAMUNDA_STRING:
            return (child.text or "").strip(), False
        if child.tag == TAG_CAMUNDA_LIST:
            values = []
            for val_elem in child:
                if val_elem.tag == TAG_CAMUNDA_VALUE:
                    values.append((val_elem.text or "").strip())
            return "[" + ", ".join(values) + "]", False
        if child.tag == TAG_CAMUNDA_MAP:
            entries = []
            for entry in child:
                if entry.tag == TAG_CAMUNDA_ENTRY:
                    key = entry.get("key", "")
                    val = (entry.text or "").strip()
                    entries.append(f"{key}: {val}")
            return "{" + ", ".join(entries) + "}", False

    # Fallback: serialize child XML as string
    parts = []
    for child in children:
        tag_local = child.tag.split("}", 1)[-1] if "}" in child.tag else child.tag
        parts.append(f"<{tag_local}>")
    return " ".join(parts), False


def _parse_input_output(io_elem: etree._Element) -> tuple[list[InputParameter], list[OutputParameter]]:
    """Parse camunda:inputOutput element."""
    inputs: list[InputParameter] = []
    outputs: list[OutputParameter] = []
    for child in io_elem:
        if child.tag == TAG_CAMUNDA_INPUT_PARAMETER:
            name = get_attr(child, "name")
            value, is_expr = _parse_parameter_value(child)
            inputs.append(InputParameter(name=name, value=value, is_expression=is_expr))
        elif child.tag == TAG_CAMUNDA_OUTPUT_PARAMETER:
            name = get_attr(child, "name")
            value, is_expr = _parse_parameter_value(child)
            outputs.append(OutputParameter(name=name, value=value, is_expression=is_expr))
    return inputs, outputs


def _parse_execution_listener(listener_elem: etree._Element) -> ExecutionListener:
    """Parse a camunda:executionListener element."""
    event = get_attr(listener_elem, "event")
    class_name = get_attr(listener_elem, "class")
    expression = get_attr(listener_elem, "expression")
    delegate_expression = get_attr(listener_elem, "delegateExpression")
    fields: list[ExecutionListenerField] = []
    for child in listener_elem:
        if child.tag == TAG_CAMUNDA_FIELD:
            field_name = get_attr(child, "name")
            string_val = ""
            expr_val = ""
            for sub in child:
                if sub.tag == TAG_CAMUNDA_STRING:
                    string_val = (sub.text or "").strip()
                elif sub.tag == TAG_CAMUNDA_EXPRESSION_TAG:
                    expr_val = (sub.text or "").strip()
            # Also check attributes
            if not string_val and not expr_val:
                string_val = get_attr(child, "stringValue")
                expr_val = get_attr(child, "expression")
            fields.append(ExecutionListenerField(
                name=field_name,
                string_value=string_val,
                expression_value=expr_val,
            ))
    return ExecutionListener(
        event=event,
        class_name=class_name,
        expression=expression,
        delegate_expression=delegate_expression,
        fields=fields,
    )


def _parse_mapping(mapping_elem: etree._Element, direction: str) -> CallActivityMapping:
    """Parse a camunda:in or camunda:out element."""
    source = get_attr(mapping_elem, "source")
    target = get_attr(mapping_elem, "target")
    source_expression = get_attr(mapping_elem, "sourceExpression")
    all_vars_str = mapping_elem.get("variables", "")
    all_variables = all_vars_str.lower() == "all"
    process_variables = get_attr(mapping_elem, "processVariables")
    local_str = mapping_elem.get("local", "false").lower()
    local = local_str in ("true", "1")
    business_key = get_attr(mapping_elem, "businessKey")
    return CallActivityMapping(
        direction=direction,
        source=source,
        target=target,
        source_expression=source_expression,
        all_variables=all_variables,
        process_variables=process_variables,
        local=local,
        business_key_expression=business_key,
    )


def _parse_eing_template_registry(registry_elem: etree._Element) -> EingTemplateRegistry:
    """Parse eing:templateRegistry element."""
    templates: list[EingTemplate] = []
    for child in registry_elem:
        if child.tag == TAG_EING_TEMPLATE:
            tmpl_id = get_attr(child, "id")
            name = get_attr(child, "name")
            description = get_attr(child, "description")
            extra = {
                k: v for k, v in child.attrib.items()
                if k not in ("id", "name", "description")
            }
            templates.append(EingTemplate(id=tmpl_id, name=name, description=description, extra_attrs=extra))
    return EingTemplateRegistry(templates=templates)


def _parse_eing_json_sources(sources_elem: etree._Element) -> list[EingJsonSource]:
    """Parse eing:jsonSources element."""
    sources: list[EingJsonSource] = []
    for child in sources_elem:
        if child.tag == TAG_EING_JSON_SOURCE:
            src_id = get_attr(child, "id")
            name = get_attr(child, "name")
            source = get_attr(child, "source")
            extra = {
                k: v for k, v in child.attrib.items()
                if k not in ("id", "name", "source")
            }
            sources.append(EingJsonSource(id=src_id, name=name, source=source, extra_attrs=extra))
    return sources


def parse_extensions(element: etree._Element) -> Extensions:
    """
    Parse the bpmn:extensionElements child of an element.
    Returns an Extensions dataclass.
    """
    ext = Extensions()
    ext_elem = element.find(TAG_EXTENSION_ELEMENTS)
    if ext_elem is None:
        return ext

    for child in ext_elem:
        if child.tag == TAG_CAMUNDA_INPUT_OUTPUT:
            inputs, outputs = _parse_input_output(child)
            ext.input_parameters.extend(inputs)
            ext.output_parameters.extend(outputs)
        elif child.tag == TAG_CAMUNDA_EXECUTION_LISTENER:
            ext.execution_listeners.append(_parse_execution_listener(child))
        elif child.tag == TAG_CAMUNDA_IN:
            ext.call_activity_mappings.append(_parse_mapping(child, "in"))
        elif child.tag == TAG_CAMUNDA_OUT:
            ext.call_activity_mappings.append(_parse_mapping(child, "out"))
        elif child.tag == TAG_EING_TEMPLATE_REGISTRY:
            ext.eing_template_registry = _parse_eing_template_registry(child)
        elif child.tag == TAG_EING_JSON_SOURCES:
            ext.eing_json_sources.extend(_parse_eing_json_sources(child))

    return ext
