"""Dataclasses for Camunda and eing extension elements."""

from dataclasses import dataclass, field


@dataclass
class InputParameter:
    name: str
    value: str = ""
    is_expression: bool = False


@dataclass
class OutputParameter:
    name: str
    value: str = ""
    is_expression: bool = False


@dataclass
class ExecutionListenerField:
    name: str
    string_value: str = ""
    expression_value: str = ""


@dataclass
class ExecutionListener:
    event: str
    class_name: str = ""
    expression: str = ""
    delegate_expression: str = ""
    fields: list[ExecutionListenerField] = field(default_factory=list)


@dataclass
class CallActivityMapping:
    direction: str  # "in" or "out"
    source: str = ""
    target: str = ""
    source_expression: str = ""
    all_variables: bool = False
    process_variables: str = ""
    local: bool = False
    business_key_expression: str = ""


@dataclass
class EingTemplate:
    id: str
    name: str = ""
    description: str = ""
    extra_attrs: dict[str, str] = field(default_factory=dict)


@dataclass
class EingTemplateRegistry:
    templates: list[EingTemplate] = field(default_factory=list)


@dataclass
class EingJsonSource:
    id: str = ""
    name: str = ""
    source: str = ""
    extra_attrs: dict[str, str] = field(default_factory=dict)


@dataclass
class Extensions:
    input_parameters: list[InputParameter] = field(default_factory=list)
    output_parameters: list[OutputParameter] = field(default_factory=list)
    execution_listeners: list[ExecutionListener] = field(default_factory=list)
    call_activity_mappings: list[CallActivityMapping] = field(default_factory=list)
    eing_template_registry: EingTemplateRegistry | None = None
    eing_json_sources: list[EingJsonSource] = field(default_factory=list)

    def is_empty(self) -> bool:
        return (
            not self.input_parameters
            and not self.output_parameters
            and not self.execution_listeners
            and not self.call_activity_mappings
            and self.eing_template_registry is None
            and not self.eing_json_sources
        )
