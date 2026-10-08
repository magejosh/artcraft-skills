---
name: lightcraft
description: "Use LightCraft for nondestructive RAW/photo development, culling, ratings, albums, masks, presets, XMP sidecars, and batch image exports. Trigger on LightCraft photo-library work; distinguish full RAW development from embedded-preview support."
---

# LightCraft

Develop and organize photographs while preserving originals and library state.

## Target version and setup

Written for LightCraft 0.2.1. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/lightcraft.

- Discover the CLI from `lightcraft-cli` on PATH, or set `LIGHTCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; on other systems, use the available matching platform build. Resolve the GUI independently when it is needed.
- Confirm the application's actual version using its supported version/help output or release/package metadata. Do not assume every CLI supports `--version` or subcommand `--help`.
- Verify executable provenance and task permission before launch. Start with read-only command/schema discovery, then a tiny copied-file trial. Keep unrelated documents, processes, devices, and ports undisturbed.
- Do not configure persistent MCP access, download models or plugins, enable recording, overwrite originals, or transmit files merely because the skill describes those features.

Example discovery after those checks, in a shell appropriate to the host:

```sh
CLI="${LIGHTCRAFT_CLI:-$(command -v lightcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set LIGHTCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" controls --json
```

```powershell
$cli = $env:LIGHTCRAFT_CLI
if (-not $cli) { $cli = (Get-Command lightcraft-cli -ErrorAction Stop).Source }
& $cli controls --json
```

The command examples in the reference use synthetic relative filenames. Substitute real authorized inputs and distinct output destinations; never assume the example files exist.

## Workflow

1. Confirm source folder/files, intended library, rating/edit criteria, output color/size/format, metadata policy, and whether originals or XMP may change.
2. Prefer single-image render for isolated adjustments. Opening a folder imports/scans into a library; do not use that as a read-only preview.
3. Inspect develop controls for valid ranges/defaults, then apply a small sample. Keep development nondestructive and compare before/after.
4. Use GUI for crop, masks, culling, and visual color review; validate a representative export before a batch.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another app's flags.

## Verify and deliver

Inspect exports at full resolution for exposure, highlight/shadow clipping, color, crop, halos, and sharpness. Confirm dimensions, format, metadata policy, filenames, and count; verify originals remain intact and disclose preview-only RAW processing.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

RAW: DNG, CR2, ARW, NEF, uncompressed RAF/ORF, RW2, PEF; common raster formats and PSD composites/JPEG XL. Export JPEG/PNG/TIFF/WebP/AVIF/DNG/original; XMP sidecars.

CR3 and compressed RAF/ORF use embedded previews only; non-DNG RAW uses neutral matrices. Subject/sky masks are heuristics; AI denoise/super-resolution is missing. Bare launch opens ~/Pictures/LightCraft Library; folder launch scans/imports. Use a discovered preset ID; a dot is not a preset.

Distinguish source-build dependencies from packaged-runtime requirements. Check the matching platform release and linked packaging documentation before installing extra dependencies.

## Example request

“Apply +0.5 exposure to one JPEG and export a separate file, then review before processing the rest of the folder.”

Target app version: LightCraft 0.2.1. If the installed or globally available LightCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/lightcraft before relying on these commands.
