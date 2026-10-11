---
name: cadcraft
description: "Use CADCraft for 2D CAD drawings, DXF/DWG inspection or conversion, command-script drafting, layers, dimensions, layouts, and SVG/PNG/PDF output. Trigger on CADCraft CAD tasks; preserve drawing units and verify geometry and plot scale."
---

# CADCraft

Create, inspect, edit, and convert CAD drawings with CADCraft.

## Target version and setup

Written for CADCraft 0.5.0. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/cadcraft.

- Discover the CLI from `cadcraft-cli` on PATH, or set `CADCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; on other systems, use the available matching platform build. Resolve the GUI independently when it is needed.
- Confirm the application's actual version using its supported version/help output or release/package metadata. Do not assume every CLI supports `--version` or subcommand `--help`.
- Verify executable provenance and task permission before launch. Start with read-only command/schema discovery, then a tiny copied-file trial. Keep unrelated documents, processes, devices, and ports undisturbed.
- Do not configure persistent MCP access, download models or plugins, enable recording, overwrite originals, or transmit files merely because the skill describes those features.

Example discovery after those checks, in a shell appropriate to the host:

```sh
CLI="${CADCRAFT_CLI:-$(command -v cadcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set CADCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" commands
```

```powershell
$cli = $env:CADCRAFT_CLI
if (-not $cli) { $cli = (Get-Command cadcraft-cli -ErrorAction Stop).Source }
& $cli commands
```

The command examples in the reference use synthetic relative filenames. Substitute real authorized inputs and distinct output destinations; never assume the example files exist.

## Workflow

1. Establish units, origin, model versus paper space, required entities/layers/dimensions, and delivery format before drawing.
2. Prefer `info` for a read-only inventory and `convert` for supported format conversion; use `run` with documented command strings for repeatable edits.
3. Discover drawing commands before constructing longer scripts. Preserve blocks, attributes, layers, layouts, and dimensions; inspect unsupported entities rather than flattening silently.
4. Use the GUI for spatial review, snapping, layout/viewports, or unsupported script controls. Fit extents and inspect at useful zoom.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another app's flags.

## Verify and deliver

Reopen the saved drawing; inspect entity counts, extents, layers, units, dimensions, and expected layout. Render the output and check clipping, lineweights, text, and plot scale. Report any DWG/DXF fidelity loss.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

DXF ASCII/binary R12–2018; DWG R13–2018 through acadrust; PDF plotting; SVG and PNG export. Command scripts resemble .scr files.

No external Windows runtime dependency is documented. Trunk is a web source-build dependency. Validate CAD fidelity and supported entity types on the actual file.

Distinguish source-build dependencies from packaged-runtime requirements. Check the matching platform release and linked packaging documentation before installing extra dependencies.

## Example request

“Inspect a DXF, change only an agreed layer, save a new DXF, and render a PNG preview.”

## Changes in 0.5.0

Image exports now support explicit current-view, extents or drawing-window framing. Check units, clipping and framing before delivery; the default view is not a promise to fit every entity. The release also improves DXF entity, layer and dimension preservation, which still needs a round-trip check on the actual drawing. These are source-reviewed changes; earlier runtime checks apply only to their recorded versions. See the reference for exact grammar and verification.

Target app version: CADCraft 0.5.0. If the installed or globally available CADCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/cadcraft before relying on these commands.
