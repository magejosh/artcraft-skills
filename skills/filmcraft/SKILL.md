---
name: filmcraft
description: "Use FilmCraft for video timeline editing, trims, captions, color grading, audio mixing, and supported sequence interchange/export. Trigger on FilmCraft editing tasks; use the matching command schemas and validate a short render before a full export."
---

# FilmCraft

Edit and deliver local video timelines with FilmCraft without disturbing other projects.

## Target version and setup

Written for FilmCraft 0.2.1. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/filmcraft.

- Discover the CLI from `filmcraft-cli` on PATH, or set `FILMCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; on other systems, use the available matching platform build. Resolve the GUI independently when it is needed.
- Confirm the application's actual version using its supported version/help output or release/package metadata. Do not assume every CLI supports `--version` or subcommand `--help`.
- Verify executable provenance and task permission before launch. Start with read-only command/schema discovery, then a tiny copied-file trial. Keep unrelated documents, processes, devices, and ports undisturbed.
- Do not configure persistent MCP access, download models or plugins, enable recording, overwrite originals, or transmit files merely because the skill describes those features.

Example discovery after those checks, in a shell appropriate to the host:

```sh
CLI="${FILMCRAFT_CLI:-$(command -v filmcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set FILMCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" help
```

```powershell
$cli = $env:FILMCRAFT_CLI
if (-not $cli) { $cli = (Get-Command filmcraft-cli -ErrorAction Stop).Source }
& $cli help
```

The command examples in the reference use synthetic relative filenames. Substitute real authorized inputs and distinct output destinations; never assume the example files exist.

## Workflow

1. Confirm source media, edit brief, frame rate, sequence dimensions, duration, audio layout, and final codec/container.
2. Inspect clips, tracks, timebase, and command schemas before edits. Resolve missing media without silently substituting files.
3. Use copies and a short selected-range render first. Prefer GUI for timeline review and grading/scopes when exact automation is absent.
4. Use integer timeline ticks accurately: the README documents 254016000000 ticks per second. Do not confuse seconds with sourceIn/duration tick parameters.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another app's flags.

## Verify and deliver

Reopen .fcproj and play the exported file. Inspect beginning/end and each edit boundary; verify duration, resolution, frame rate, captions, audio sync/levels, and codec. Report unsupported interchange elements and offline media.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

.fcproj projects. Export H.264 MP4/AAC, supported ProRes/MJPEG QuickTime and MXF variants, PNG sequences, GIF and WAV. Caption SRT/WebVTT/SCC; timeline FCP7 XML, FCPXML 1.9–1.11, OTIO, EDL, AAF, OMF2.

HEVC/AV1 export, camera RAW, E-AC3, VST3/AU/OpenFX hosting are not supported in the v0.2.1 README. No FFmpeg runtime dependency. Version 0.2.1 hardware decode is macOS-only, so Windows render/export can be CPU-heavy. Optional speech-to-text is off by default. Prefer `help`; generic --help is consumed by this parser.

Distinguish source-build dependencies from packaged-runtime requirements. Check the matching platform release and linked packaging documentation before installing extra dependencies.

## Example request

“Inspect a timeline and prepare a verified short H.264 export before authorizing a full-length render.”

Target app version: FilmCraft 0.2.1. If the installed or globally available FilmCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/filmcraft before relying on these commands.
