---
name: recraft-gridcraft
description: "Use GridCraft to create or inspect spreadsheets, XLSX/CSV/TSV data, formulas, tables, charts, PivotTables, formatting, and print output. Trigger on GridCraft or reCraft workbook tasks; preserve formulas and validate recalculated values."
---

# GridCraft

Work with local spreadsheets through GridCraft's command engine and GUI.

## Target version and setup

Written for GridCraft 0.3.0. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/gridcraft.

- Discover the CLI from `gridcraft-cli` on PATH, or set `GRIDCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; on other systems, use the available matching platform build. Resolve the GUI independently when it is needed.
- Confirm the application's actual version using its supported version/help output or release/package metadata. Do not assume every CLI supports `--version` or subcommand `--help`.
- Verify executable provenance and task permission before launch. Start with read-only command/schema discovery, then a tiny copied-file trial. Keep unrelated documents, processes, devices, and ports undisturbed.
- Do not configure persistent MCP access, download models or plugins, enable recording, overwrite originals, or transmit files merely because the skill describes those features.

Example discovery after those checks, in a shell appropriate to the host:

```sh
CLI="${GRIDCRAFT_CLI:-$(command -v gridcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set GRIDCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" commands
```

```powershell
$cli = $env:GRIDCRAFT_CLI
if (-not $cli) { $cli = (Get-Command gridcraft-cli -ErrorAction Stop).Source }
& $cli commands
```

The command examples in the reference use synthetic relative filenames. Substitute real authorized inputs and distinct output destinations; never assume the example files exist.

## Workflow

1. Identify workbook, sheet, exact target range, units, formulas versus values, and requested output. Preserve untouched sheets and workbook structure.
2. Inspect ranges before writing. Use the command catalog and schemas to create formulas, formatting, charts, and tables; avoid guessed field names.
3. Calculate and check representative formulas, totals, dates, currencies, dynamic-array spill ranges, and missing/error values.
4. Use GUI for chart/layout/print review, then save an editable XLSX copy and any requested exports.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another reCraft app's flags.

## Verify and deliver

Reopen the saved workbook and compare sheet names, cell/range values, formulas, styles, tables, charts, and print areas. Independently check important totals; distinguish preserved formulas from cached values and CSV's flattened output.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

XLSX, CSV/TSV and native/debug JSON; HTML export. CSV/TSV/HTML use the active sheet. PDF requires a separate engine command, not CLI convert. XLSM/XLTX/XLTM recognition does not prove macro preservation.

Pre-alpha. Slicers, Solver, chart trendlines, and true Page Layout view are roadmap items. No extra Windows runtime requirement documented; web source builds need Trunk and wasm. Formula compatibility is not guaranteed solely by a function count.

Distinguish source-build dependencies from packaged-runtime requirements. Check the matching platform release and linked packaging documentation before installing extra dependencies.

## Example request

“Inspect B4:F15 in a budget workbook, bold the agreed header range in a copy, and verify totals after saving.”

Target app version: GridCraft 0.3.0. If the installed or globally available GridCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/gridcraft before relying on these commands.
