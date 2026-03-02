"""Root BpmnDocument dataclass."""

from dataclasses import dataclass, field
from datetime import datetime

from bpmn_doc.models.elements import (
    Collaboration,
    GlobalError,
    GlobalEscalation,
    GlobalMessage,
    GlobalSignal,
    Process,
)


@dataclass
class BpmnDocument:
    file_path: str
    file_name: str
    generated_at: datetime
    definitions_id: str = ""
    exporter: str = ""
    exporter_version: str = ""
    target_namespace: str = ""
    collaboration: Collaboration | None = None
    processes: list[Process] = field(default_factory=list)
    messages: list[GlobalMessage] = field(default_factory=list)
    signals: list[GlobalSignal] = field(default_factory=list)
    errors: list[GlobalError] = field(default_factory=list)
    escalations: list[GlobalEscalation] = field(default_factory=list)
    suppress_empty: bool = False
