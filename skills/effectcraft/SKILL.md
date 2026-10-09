---
name: effectcraft
description: "Use EffectCraft for motion graphics, layered compositions, keyframes, compositing, masks, effects, and Lottie or video export. Trigger on EffectCraft animation tasks; verify the available CLI and render settings before exporting."
---

# EffectCraft

Create and inspect layered motion graphics, preserving an editable EffectCraft project.

## Target version and setup

Written for EffectCraft 0.6.0. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/effectcraft.

- Discover the CLI from `effectcraft-cli` on PATH, or set `EFFECTCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; on other systems, use the available matching platform build. Resolve the GUI independently when it is needed.
- Confirm the application's actual version using its supported version/help output or release/package metadata. Do not assume every CLI supports `--version` or subcommand `--help`.
- Verify executable provenance and task permission before launch. Start with read-only command/schema discovery, then a tiny copied-file trial. Keep unrelated documents, processes, devices, and ports undisturbed.
- Do not configure persistent MCP access, download models or plugins, enable recording, overwrite originals, or transmit files merely because the skill describes those features.

Example discovery after those checks, in a shell appropriate to the host:

```sh
CLI="${EFFECTCRAFT_CLI:-$(command -v effectcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set EFFECTCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" commands --schemas --json
```

```powershell
$cli = $env:EFFECTCRAFT_CLI
if (-not $cli) { $cli = (Get-Command effectcraft-cli -ErrorAction Stop).Source }
& $cli commands --schemas --json
```

The command examples in the reference use synthetic relative filenames. Substitute real authorized inputs and distinct output destinations; never assume the example files exist.

## Workflow

1. Confirm duration, frame rate, canvas size, composition, assets, alpha/audio needs, and target codec or Lottie feature constraints.
2. Inspect the project and command/property schema before setting indexed layer paths; identify layers by the current project rather than assumed indexes. Query `render.backend` to distinguish the requested GPU setting from the active compositor and its CPU fallback reason. `comp.renderer` separately selects Classic or Advanced 3D.
3. Save an editable .ecproj copy before a short preview render. Validate representative first/middle/last and key transition frames before a full export.
4. Use GUI for timeline/graph editor work, masks, or visual compositing when command coverage is uncertain. Ease presets apply to neighbouring selected keyframe pairs; select the intended keys and inspect the curve after applying. Adding a 3D model/primitive switches a Classic 3D composition to Advanced 3D, so review the composition after the change.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another app's flags.

## Verify and deliver

Reopen the project, inspect the intended composition/layers/keyframes, and play the output. Verify eased motion between keys, masks/shape contents, dimensions, frame rate, duration, codec, alpha, and audio as applicable. Record the actual render backend when performance or GPU fidelity matters. For Lottie, read unsupported-feature reports and inspect playback.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

.ecproj versioned JSON; Lottie .json/.lottie. Documented outputs include H.264 MP4, ProRes MOV, HEVC/AV1 MP4, WebM, image sequences including EXR, GIF, and WAV/AIFF; check the exact matching preset/schema.

Cannot open AEP/AEPX or run After Effects plug-ins; the upstream compatibility assessment still reports unmeasured differences. The GUI now starts empty, but project-less CLI render still uses the demo; explicitly supply --project. Headless CLI/MCP rendering defaults to CPU; --gpu needs a usable adapter and the project must enable GPU acceleration. Full CLI render rejects --bridge. Optional ML models are separate downloads; no FFmpeg runtime dependency.

Rust 1.95+ is for source builds. Official Windows portable packages include GUI and CLI executables with a statically linked C runtime, so the packaging script requires no Visual C++ redistributable. Diagnose GPU fallback before changing system settings. Ease-preset save/rename/delete can write the app configuration and is separate from saving the project.

## Example request

“Animate a known layer's position in a copied project, render a short preview, and inspect its first and last keyframes.”

Target app version: EffectCraft 0.6.0. If the installed or globally available EffectCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/effectcraft before relying on these commands.
