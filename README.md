# bpmn-documentation-extractor

CLI tool that reads BPMN 2.0 XML files (Camunda-flavoured) and produces structured Markdown or
YAML documentation — ready to commit alongside your process definitions, include in wikis, or diff
in pull requests.

## What gets extracted

### Process structure
- **Collaboration & participants** — pool names and their linked processes
- **Lanes** — swimlane membership of every flow node
- **Processes** — id, name, executable flag, inline documentation

### Flow elements
| Element | Extracted attributes |
|---------|----------------------|
| **Tasks** (service, user, send, receive, business rule, script, manual, call activity) | name, type, documentation, annotations, Camunda implementation (`class`, `expression`, `delegateExpression`, `topic`), result variable, async flags, called-element binding |
| **Events** (start, end, intermediate catch/throw, boundary) | name, type, documentation, annotations, event definitions (message, timer, signal, error, escalation, conditional, compensation), timer expressions, boundary attachment, cancel-activity flag, async flags |
| **Gateways** (exclusive, inclusive, parallel, complex, event-based) | name, type, documentation, annotations, default flow, gateway direction |
| **Subprocesses** (sub-process, transaction, ad-hoc, call activity) | name, type, documentation, triggered-by-event flag, async flags, full recursive content |
| **Sequence flows** | source → target names, condition expressions, text annotations |

### Global definitions
- **Messages**, **Signals** — id and name
- **Errors** — id, name, error code
- **Escalations** — id, name, escalation code

### Camunda extensions (per element)
- Input / output parameters (literal values and expressions)
- Execution listeners (event, implementation, fields)
- Call-activity variable mappings (in/out, all-variables, business key)

## Installation (pipx — recommended)

Prerequisites: Python ≥ 3.12, [pipx](https://pipx.pypa.io/) installed.

```bash
pipx install git+https://github.com/bodis/bpmn-documentation-extractor.git
```

After this, `bpmn-doc` is available system-wide. If the command is not found, run:

```bash
pipx ensurepath   # then open a new terminal
```

## Updating

```bash
pipx upgrade bpmn-documentation-extractor
```

## Usage

```bash
bpmn-doc <file.bpmn>                   # Markdown to stdout
bpmn-doc <file.bpmn> --format yaml     # YAML to stdout
bpmn-doc <file.bpmn> -o output.md      # write to file
bpmn-doc <file.bpmn> --suppress-empty  # omit empty sections
bpmn-doc <file.bpmn> --verbose         # show parsing progress
```

Exit codes: 0 success, 1 file error, 2 parse error, 3 render error.

## Developer Setup

Requirements: Python 3.12+, [uv](https://docs.astral.sh/uv/)

```bash
git clone https://github.com/bodis/bpmn-documentation-extractor.git
cd bpmn-documentation-extractor
uv sync          # creates .venv and installs all deps
uv run bpmn-doc <file.bpmn>
```

## Installing locally with pipx (from source)

```bash
cd bpmn-documentation-extractor
pipx install .
```
