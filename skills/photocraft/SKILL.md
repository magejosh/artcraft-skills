---
name: photocraft
description: "Use PhotoCraft for layered raster editing, PSD/PSB, masks, adjustments, painting, selections, smart objects, filters, and recorded action batches. Trigger on PhotoCraft image-editing tasks; preserve an editable master and verify output fidelity."
---

# PhotoCraft

Edit layered images and automate approved batches in PhotoCraft.

## Target version and setup

Written for PhotoCraft 0.3.0. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/photocraft.

- Discover the CLI from `photocraft-cli` on PATH, or set `PHOTOCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; on other systems, use the available matching platform build. Resolve the GUI independently when it is needed.
- Confirm the application's actual version using its supported version/help output or release/package metadata. Do not assume every CLI supports `--version` or subcommand `--help`.
- Verify executable provenance and task permission before launch. Start with read-only command/schema discovery, then a tiny copied-file trial. Keep unrelated documents, processes, devices, and ports undisturbed.
- Do not configure persistent MCP access, download models or plugins, enable recording, overwrite originals, or transmit files merely because the skill describes those features.

Example discovery after those checks, in a shell appropriate to the host:

```sh
CLI="${PHOTOCRAFT_CLI:-$(command -v photocraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set PHOTOCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" commands --json
```

```powershell
$cli = $env:PHOTOCRAFT_CLI
if (-not $cli) { $cli = (Get-Command photocraft-cli -ErrorAction Stop).Source }
& $cli commands --json
```

The command examples in the reference use synthetic relative filenames. Substitute real authorized inputs and distinct output destinations; never assume the example files exist.

## Workflow

1. Confirm source image, layer/selection scope, dimensions, color mode/depth/profile, edits, and deliverable formats.
2. Inspect document/layer structure and command parameters before applying filters or adjustments. Work on an editable copy; retain masks and smart objects unless flattening is requested.
3. Test action batches on one representative copied file before processing a folder; define collision/overwrite behavior and preserve originals.
4. Use GUI for selections, brush work, masks, typography, and visual comparisons where command automation is unsuitable.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another app's flags.

## Verify and deliver

Reopen layered output and check layer count/order, masks, editable text, profiles, bit depth, transparency, and dimensions. Inspect the exported composite at 100%; compare before/after and report unsupported PSD data or flattened elements.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

PSD/PSB, .pcraft, PNG/JPEG/TIFF/WebP/GIF/BMP/TGA/ICO/QOI/PNM/OpenEXR/Radiance HDR/AVIF; RGB/Gray/CMYK/Lab and 8/16/32-bit modes. LUT .cube/.3dl/.look and .pat patterns documented.

PSD round trips are not byte-identical. Early-alpha typography, plug-in, and generative gaps remain. portable.txt routes settings/presets/autosave/startup state to adjacent PhotoCraftData, with %APPDATA%\Photocraft fallback if unwritable. Do not remove the marker or mutate configuration casually. Source optional craft-fonts is included in desktop releases.

Distinguish source-build dependencies from packaged-runtime requirements. Check the matching platform release and linked packaging documentation before installing extra dependencies.

## Example request

“Apply sharpening and a curves adjustment to a copied PSD, retain an editable master, and inspect a PNG export.”

Target app version: PhotoCraft 0.3.0. If the installed or globally available PhotoCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/photocraft before relying on these commands.
