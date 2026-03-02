"""Typer CLI for the BPMN documentation extractor."""

import sys
from enum import Enum
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

app = typer.Typer(
    name="bpmn-doc",
    help="Extract structured documentation from BPMN 2.0 files.",
    add_completion=False,
)

stderr = Console(stderr=True)


class OutputFormat(str, Enum):
    markdown = "markdown"
    yaml = "yaml"


@app.command()
def main(
    bpmn_file: Annotated[Path, typer.Argument(help="Path to the .bpmn file")],
    format: Annotated[
        OutputFormat,
        typer.Option("--format", "-f", help="Output format"),
    ] = OutputFormat.markdown,
    output_file: Annotated[
        Optional[Path],
        typer.Option("--output-file", "-o", help="Output file path (default: stdout)"),
    ] = None,
    suppress_empty: Annotated[
        bool,
        typer.Option("--suppress-empty", help="Omit empty sections"),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Show parsing progress to stderr"),
    ] = False,
) -> None:
    """Extract structured documentation from a BPMN 2.0 file."""

    # Validate input file
    if not bpmn_file.exists():
        stderr.print(f"[red]Error:[/red] File not found: {bpmn_file}")
        raise typer.Exit(code=1)
    if not bpmn_file.is_file():
        stderr.print(f"[red]Error:[/red] Not a file: {bpmn_file}")
        raise typer.Exit(code=1)
    if not bpmn_file.suffix.lower() == ".bpmn" and verbose:
        stderr.print(f"[yellow]Warning:[/yellow] File does not have .bpmn extension: {bpmn_file}")

    # Parse
    try:
        from bpmn_doc.parser.bpmn_parser import parse
        doc = parse(bpmn_file, verbose=verbose)
        doc.suppress_empty = suppress_empty
    except Exception as e:
        stderr.print(f"[red]Parse error:[/red] {e}")
        raise typer.Exit(code=2)

    # Render
    try:
        if format == OutputFormat.markdown:
            from bpmn_doc.renderer.markdown_renderer import render_markdown
            output = render_markdown(doc)
        else:
            from bpmn_doc.renderer.yaml_renderer import render_yaml
            output = render_yaml(doc)
    except Exception as e:
        stderr.print(f"[red]Render error:[/red] {e}")
        raise typer.Exit(code=3)

    # Write output
    if output_file is not None:
        try:
            output_file.write_text(output, encoding="utf-8")
            if verbose:
                stderr.print(f"[green]Written to:[/green] {output_file}")
        except OSError as e:
            stderr.print(f"[red]Write error:[/red] {e}")
            raise typer.Exit(code=1)
    else:
        sys.stdout.write(output)
        if not output.endswith("\n"):
            sys.stdout.write("\n")
