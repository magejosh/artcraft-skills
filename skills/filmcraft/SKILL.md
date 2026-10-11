---
name: filmcraft
description: "Use FilmCraft for video timeline editing, trims, captions, color grading, audio mixing, and supported sequence interchange/export. Trigger on FilmCraft editing tasks; use the matching command schemas and validate a short render before a full export."
---

# FilmCraft

Edit and deliver local video timelines with FilmCraft without disturbing other projects.

## Target version and setup

Written for FilmCraft 0.6.0. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/filmcraft.

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
2. Inspect clips, tracks, timebase, and command schemas before edits. `sequence.inspect` now exposes clip ends, source-out, reversal, gain and marker comments. Resolve missing media without silently substituting files; an unknown named track is an error.
3. Use copies and a short selected-range export first. Set `--range entire` for the final full-sequence export; otherwise existing In/Out marks can limit it. Check linked audio/video partners, locked/sync-locked tracks and overwrite reports when moving or trimming clips. Nested-sequence rendering and interchange improved, but verify nested timing/effects/captions and each interchange warning. Prefer GUI for timeline review and grading/scopes when exact automation is absent.
4. Use integer timeline ticks accurately: the README documents 254016000000 ticks per second. Do not confuse seconds with sourceIn/duration tick parameters.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another app's flags.

## Verify and deliver

Reopen .fcproj, including projects saved after an interchange import, and play the exported file. Inspect beginning/end, edit boundaries and nested sequences; verify duration, resolution, frame rate, captions, audio sync/levels, codec and profile. Report unsupported interchange elements and offline media. Hardware availability and a preset name do not prove which encoder or decoder ran.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

.fcproj projects. Export H.264 MP4/AAC, ProRes/DNxHR/APV/MJPEG QuickTime, supported MXF variants, PNG/TIFF/BMP/JPEG/Targa/DPX/OpenEXR sequences, GIF and WAV/AIFF/AAC audio. HEVC and AV1 export depend on an available hardware encoder; inspect supported profiles and HDR capability on the actual host. Caption SRT/WebVTT/SCC; timeline FCP7 XML, FCPXML 1.9–1.11, OTIO, EDL, AAF, OMF2.

Windows now has Media Foundation/D3D11 hardware decoding and opt-in NVIDIA NVENC H.264 encoding; macOS uses VideoToolbox. Profile, driver and codec-extension availability matter, and export compositing can remain CPU-bound. Linux H.264/HEVC hardware decode depends on an available backend. Hardware-dependent AV1 export and E-AC3 decoding are documented; camera RAW and VST3/AU/OpenFX hosting remain unsupported. No FFmpeg runtime dependency. Speech-to-text is optional and unavailable commands report the missing build feature; supplied transcripts can still be edited. Prefer CLI `help`; the GUI’s improved --help does not change the CLI parser.

Official Windows portable packages include GUI and CLI executables with a statically linked C runtime; the packaging script requires no Visual C++ redistributable. Optional Windows decoder extensions and supported GPU drivers are distinct from source-build tools. Do not install extensions, drivers or speech models merely because an export or transcript feature exists.

## Example request

“Inspect a timeline and prepare a verified short H.264 export before authorizing a full-length render.”

## Changes in 0.6.0

The export source adds hardware-dependent AV1, ProRes 4444/4444 XQ alpha, JPEG/Targa/DPX/OpenEXR sequences and audio-only AAC. Check the actual encoder availability, export settings and complete output. Source capability does not establish GPU support or codec fidelity on the host. These are source-reviewed changes; earlier runtime checks apply only to their recorded versions. See the reference for exact grammar and verification.

Target app version: FilmCraft 0.6.0. If the installed or globally available FilmCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/filmcraft before relying on these commands.
