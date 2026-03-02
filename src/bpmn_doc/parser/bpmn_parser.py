"""Entry point for BPMN parsing: parse(path) -> BpmnDocument."""

import os
from datetime import datetime
from pathlib import Path

from lxml import etree

from bpmn_doc.constants import (
    TAG_COLLABORATION,
    TAG_ERROR,
    TAG_ESCALATION,
    TAG_MESSAGE,
    TAG_PROCESS,
    TAG_SIGNAL,
)
from bpmn_doc.exceptions import BpmnParseError
from bpmn_doc.models.document import BpmnDocument
from bpmn_doc.parser.common_parser import build_id_map, get_attr
from bpmn_doc.parser.definitions_parser import (
    parse_collaboration,
    parse_global_error,
    parse_global_escalation,
    parse_global_message,
    parse_global_signal,
    parse_process,
)


def parse(file_path: str | Path, verbose: bool = False) -> BpmnDocument:
    """
    Parse a BPMN 2.0 file and return a BpmnDocument.

    Args:
        file_path: Path to the .bpmn file.
        verbose: If True, print progress information to stderr.

    Returns:
        A populated BpmnDocument.

    Raises:
        BpmnParseError: If the file cannot be parsed.
    """
    from rich.console import Console
    stderr = Console(stderr=True)

    path = Path(file_path)
    if not path.exists():
        raise BpmnParseError(f"File not found: {file_path}")
    if not path.is_file():
        raise BpmnParseError(f"Not a file: {file_path}")

    try:
        if verbose:
            stderr.print(f"[dim]Parsing {path.name}...[/dim]")
        tree = etree.parse(str(path))
        root = tree.getroot()
    except etree.XMLSyntaxError as e:
        raise BpmnParseError(f"XML syntax error in {file_path}: {e}") from e

    if verbose:
        stderr.print("[dim]Building ID map...[/dim]")
    id_map = build_id_map(root)

    doc = BpmnDocument(
        file_path=str(path.resolve()),
        file_name=path.name,
        generated_at=datetime.now(),
        definitions_id=get_attr(root, "id"),
        exporter=get_attr(root, "exporter"),
        exporter_version=get_attr(root, "exporterVersion"),
        target_namespace=get_attr(root, "targetNamespace"),
    )

    for child in root:
        tag = child.tag
        if tag == TAG_COLLABORATION:
            if verbose:
                stderr.print("[dim]Parsing collaboration...[/dim]")
            doc.collaboration = parse_collaboration(child)
        elif tag == TAG_PROCESS:
            if verbose:
                stderr.print(f"[dim]Parsing process {get_attr(child, 'id')}...[/dim]")
            doc.processes.append(parse_process(child, id_map))
        elif tag == TAG_MESSAGE:
            doc.messages.append(parse_global_message(child))
        elif tag == TAG_SIGNAL:
            doc.signals.append(parse_global_signal(child))
        elif tag == TAG_ERROR:
            doc.errors.append(parse_global_error(child))
        elif tag == TAG_ESCALATION:
            doc.escalations.append(parse_global_escalation(child))

    _link_participants_to_processes(doc)

    if verbose:
        stderr.print(
            f"[green]Parsed:[/green] {len(doc.processes)} process(es), "
            f"{sum(len(p.tasks) for p in doc.processes)} task(s), "
            f"{sum(len(p.events) for p in doc.processes)} event(s)"
        )

    return doc


def _link_participants_to_processes(doc: BpmnDocument) -> None:
    """
    If a collaboration exists, enrich participant.name on Process objects
    by matching participant.process_ref -> process.id.
    """
    if doc.collaboration is None:
        return
    process_map = {p.id: p for p in doc.processes}
    for participant in doc.collaboration.participants:
        proc = process_map.get(participant.process_ref)
        if proc and not proc.name and participant.name:
            proc.name = participant.name
