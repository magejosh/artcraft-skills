---
name: vectorcraft
description: "Use VectorCraft for vector illustrations, paths, booleans, gradients, artboards, type, SVG, PDF, and image export. Trigger on VectorCraft vector-artwork tasks; preserve editable paths and review fonts and clipping."
---

# VectorCraft

Create and convert local vector artwork with VectorCraft while preserving editable structure.

## Target version and setup

Written for VectorCraft 0.4.0. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/vectorcraft.

- Discover the CLI from `vectorcraft-cli` on PATH, or set `VECTORCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; on other systems, use the available matching platform build. Resolve the GUI independently when it is needed.
- Confirm the application's actual version using its supported version/help output or release/package metadata. Do not assume every CLI supports `--version` or subcommand `--help`.
- Verify executable provenance and task permission before launch. Start with read-only command/schema discovery, then a tiny copied-file trial. Keep unrelated documents, processes, devices, and ports undisturbed.
- Do not configure persistent MCP access, download models or plugins, enable recording, overwrite originals, or transmit files merely because the skill describes those features.

Example discovery after those checks, in a shell appropriate to the host:

```sh
CLI="${VECTORCRAFT_CLI:-$(command -v vectorcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set VECTORCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" commands
```

```powershell
$cli = $env:VECTORCRAFT_CLI
if (-not $cli) { $cli = (Get-Command vectorcraft-cli -ErrorAction Stop).Source }
& $cli commands
```

The command examples in the reference use synthetic relative filenames. Substitute real authorized inputs and distinct output destinations; never assume the example files exist.

## Workflow

1. Confirm artboard dimensions, units, print/screen intent, colors, fonts, assets, and target format.
2. Inspect layers/paths/artboards and exact command schemas before edits. Preserve editable curves and type unless outlining/rasterization is requested.
3. Use CLI for supported deterministic conversion/rendering; use GUI for path editing, shape construction, typography, appearance, and alignment.
4. Export to a new file and compare both visual appearance and editable structure.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another app's flags.

## Verify and deliver

Reopen native/SVG/PDF output, check artboard count/size, layers, clipping masks, path bounds, gradients, text/font substitution, and embedded images. Inspect a raster preview; report effects or text converted to raster/outlines.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

Native .vectorcraft/.drawcraft/.vctemplate; SVG/SVGZ, PDF/PDF-compatible AI, AIT, EPS, DXF, EMF/WMF and common rasters readable. Native/template, SVG/SVGZ, PDF, EPS, DXF, EMF/WMF, PNG/PNG8/JPEG/WebP/GIF/TIFF/BMP/TGA/PSD/text export. PSD/TGA are export-only in this version's table.

Example assets may not be bundled; replace sample paths with authorized files. Do not run bench merely to confirm installation. Check release assets for actual platform availability rather than relying on old README packaging notes. 3D/materials, raster effects, vertical CJK, and scripting/interaction remain limited. Fonts are included in releases with system fallback.

Distinguish source-build dependencies from packaged-runtime requirements. Check the matching platform release and linked packaging documentation before installing extra dependencies.

## Example request

“Convert an existing native drawing to a new PDF and check artboards, text, gradients, and clipping.”

Target app version: VectorCraft 0.4.0. If the installed or globally available VectorCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/vectorcraft before relying on these commands.
