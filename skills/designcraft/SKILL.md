---
name: designcraft
description: "Use DesignCraft for publication layout, threaded text, styles, parent pages, data merge, multilingual IDML, and page or PDF export. Trigger on DesignCraft publishing tasks; inspect preflight and export warnings."
---

# DesignCraft

Compose multipage publications and verify text flow and page appearance in DesignCraft.

## Target version and setup

Written for DesignCraft 0.6.0. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/designcraft.

- Discover the CLI from `designcraft-cli` on PATH, or set `DESIGNCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; on other systems, use the available matching platform build. Resolve the GUI independently when it is needed.
- Confirm the application's actual version using its supported version/help output or release/package metadata. Do not assume every CLI supports `--version` or subcommand `--help`.
- Verify executable provenance and task permission before launch. Start with read-only command/schema discovery, then a tiny copied-file trial. Keep unrelated documents, processes, devices, and ports undisturbed.
- Do not configure persistent MCP access, download models or plugins, enable recording, overwrite originals, or transmit files merely because the skill describes those features.

Example discovery after those checks, in a shell appropriate to the host:

```sh
CLI="${DESIGNCRAFT_CLI:-$(command -v designcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set DESIGNCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" commands
```

```powershell
$cli = $env:DESIGNCRAFT_CLI
if (-not $cli) { $cli = (Get-Command designcraft-cli -ErrorAction Stop).Source }
& $cli commands
```

The command examples in the reference use synthetic relative filenames. Substitute real authorized inputs and distinct output destinations; never assume the example files exist.

## Workflow

1. Establish page size, margins, facing pages, columns, page count, assets, and required exchange format.
2. Preserve parent-page relationships, named paragraph/character styles, threaded stories, swatches, and layers when adapting a publication.
3. Discover supported commands, then choose deterministic CLI page renders or GUI layout operations. Use GUI for frame fitting, spread inspection, and fine typography. For data merge, inspect the linked source, preview a record, and save the newly created merged document separately from its template; the old `spread` parameter is rejected.
4. Run `preflight.run` and inspect overset text, missing fonts/glyphs/images, baseline and column alignment, page numbering, and spread order. For CJK/Arabic, verify actual shaping, column/table direction, and line breaks; preserved IDML rules can still be unimplemented. Text selection offsets are UTF-8 bytes.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another app's flags.

## Verify and deliver

Render every page and inspect at reading size. Reopen the saved native/IDML output and verify page count, text flow, fonts, and assets. Inspect data-merge missing-image/overset reports and source freshness. For PDF, examine export warnings and rendered pages, especially placed graphics, transparency and CMYK inks; selecting PDF/X-4 is not proof of a compliant print file.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

.designcraft native JSON and IDML input; native/IDML, PNG/JPEG, PDF, and EPUB output are implemented in tagged v0.4.0 source. Do not promise INDD input.

Some README text still calls PDF roadmap work; the tagged parser/engine implement PDF and EPUB. Print export improves placed PDF 1.7, CMYK TIFFs, [Paper] and transparency, but warnings and format limitations still matter. Data merge supports CSV/TSV/XLSX sources and creates a new document. CJK/Arabic compatibility is partial; see the reference before promising typography parity. Web builds lack desktop control. Run exports execute in option order; use lowercase extensions.

Official Windows portable packages include GUI and CLI executables with a statically linked C runtime; the packaging script says no Visual C++ redistributable is needed. Optional craft-fonts is a source-build input and is included in release builds; still verify the fonts required by each document. Do not install build tools merely to run a portable package.

## Example request

“Render the sample magazine to a new output folder and review all pages for clipping and overset text.”

## Changes in 0.6.0

The parser rejects page, scale or PDF options placed after the last export. PDF/A image retention and IDML stacking/packaged asset handling improve. Built-in PDF/X-4 validation is available, but its scope does not replace an independent validator when a delivery standard requires one. These are source-reviewed changes; earlier runtime checks apply only to their recorded versions. See the reference for exact grammar and verification.

Target app version: DesignCraft 0.6.0. If the installed or globally available DesignCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/designcraft before relying on these commands.
