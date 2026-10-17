---
name: figcraft
description: "Use FigCraft to create or edit interface designs, screen layouts, reusable components and variants, design tokens, and interactive prototypes. Preserve editable .figcraft files and verify structure plus rendered PNG previews; use matching CLI/MCP schemas for automation."
---

# FigCraft

Build interface designs and prototypes in FigCraft, keeping the native design editable.

## Target version and setup

Written for FigCraft 0.6.0. Read [the command and format reference](references/cli-and-formats.md) before constructing scripts or using MCP. Official repository: https://github.com/storytold/figcraft.

Discover `figcraft-cli` on PATH or set `FIGCRAFT_CLI` to the verified executable. Resolve the GUI independently if the task needs it. Check actual version and provenance; the skill neither installs an app nor configures ongoing access.

```sh
CLI="${FIGCRAFT_CLI:-$(command -v figcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set FIGCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" --version
"$CLI" --help
```

```powershell
$cli = $env:FIGCRAFT_CLI
if (-not $cli) { $cli = (Get-Command figcraft-cli -ErrorAction Stop).Source }
& $cli --version
& $cli --help
```

Use synthetic relative filenames in examples as patterns, then substitute authorized inputs and distinct outputs. One-shot CLI work starts separate headless state; it does not edit an already open GUI document. Before attaching to live control, verify the process, window and document belong to the task. Do not disturb another design session.

## Design workflow

1. Establish screens, target viewport sizes, content, visual style and interactions. Inspect an existing document with `info --json`; read import notes before promising fidelity. For a new design, discover `template.list` or build explicit frames.
2. Name screens and layers meaningfully. Use frames for screen boundaries and containers, auto layout for repeated content, and fixed/hug/fill sizing intentionally. Coordinates are page units with y down, relative to the parent frame; groups do not create coordinate spaces. Auto layout positions flowing children, so edit padding/gap/sizing instead of repeatedly forcing x/y.
3. Build repeated controls as components; use instances and variants for states. Discover `component.*`, `instance.*`, `style.*` and `variable.*` schemas. Keep text editable, preserve instance links and inspect overrides before detaching or converting anything. Check font availability before tuning spacing.
4. Add prototype flows and interactions with `proto.flow.add` and `proto.interaction.add`, using IDs from the current document. Define the start frame, destination, trigger and transition. Review navigation, back actions, overlays and state variants in an authorized presenter session; a PNG cannot demonstrate interactive behavior.
5. Run a reviewed JSON/JSONL script with `run SCRIPT --in INPUT --out OUTPUT.figcraft`, or create from an empty session without `--in`. Inspect every result. Save the native `.figcraft` file before producing PNG/SVG/PDF handoff outputs. Imported `.fig` and REST API JSON are best effort; exported `.fig` is experimental.

## Verify and deliver

Reopen the saved native file with `info --json`; use document/node inspection for page hierarchy, sizes, component links, layout settings, variables and interactions. Render the relevant named page and export individual frames as PNG. Inspect clipping, text wrapping, fonts, contrast, alignment, spacing, image placeholders and states at the intended sizes. Use bounded previews on large canvases; whole-page rendering can scale down, hiding fine detail.

Match the font mode between editing and review. Default headless text uses built-in plus system fonts; `--no-system-fonts` uses only built-in fonts and can change text metrics. Use it for deliberately reproducible output, not as an invisible substitution for the user's typography.

Deliver the editable `.figcraft` file plus requested previews/exports, a brief account of changes, and remaining import/export or interaction limitations. Distinguish version/help/schema checks, structural inspection, rendered visual review and actual prototype playback. Do not call generated code a tested implementation or a static preview a working prototype.

## Automation boundaries

MCP is stdio and headless by default; `mcp --attach PORT` controls an authorized running desktop app. Describe those interfaces when useful; do not install a server/client configuration or start a listener just because a design task mentions agents. Attached calls are not automatically replayed after lost replies: inspect state before retrying an edit.

Batch document edits roll back together on failure, but external writes and non-document effects are not a general transaction. Scripts that explicitly save/export can create side effects before a later step fails. Keep output paths distinct and review commands before execution. Plugin publishing and collaboration can transmit files and create persistent state; they require their own task authorization.

## Evidence scope

Matching-tag CLI/parser and MCP/control documentation were reviewed. The installed version, help and command catalog were queried read-only. No design, export, GUI, live-control or prototype workflow was executed during this skill refresh.

Target app version: FigCraft 0.6.0. If the installed or globally available FigCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/figcraft before relying on these commands.
