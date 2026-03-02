"""Custom exceptions for the BPMN documentation extractor."""


class BpmnParseError(Exception):
    """Raised when a BPMN file cannot be parsed."""


class BpmnRenderError(Exception):
    """Raised when documentation cannot be rendered."""
