# FilmCraft 0.6.0: CLI and format reference

## Evidence and use

Commands and capability notes were reviewed against upstream tag v0.6.0, commit `2ff3f5e266838700c292a35aaf762e3d4dcef980`, including the parser, command schemas and release changelog. These are source/documentation findings, not a guarantee of runtime or visual behavior on a particular machine. Recheck after upgrading; earlier-version smoke tests do not certify this release.

Bare `filmcraft-cli` and `filmcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files. The Windows portable package includes GUI/CLI executables with a statically linked C runtime; no Visual C++ redistributable is required. No FFmpeg runtime dependency is needed.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer the documented JSONL script form or simple `key=value` parameters where suitable. Validate JSON and inspect received/resulting values; never copy Unix quoting blindly.

## Supported command examples

```text
filmcraft-cli --version
filmcraft-cli help
filmcraft-cli commands
filmcraft-cli describe file.exportMedia
filmcraft-cli describe timeline.move
filmcraft-cli --project edit.fcproj inspect sequence
filmcraft-cli --project edit.fcproj export preview.mp4 --start 0 --end 1
filmcraft-cli --project edit.fcproj export preview.mov --format apv --start 0 --end 1
filmcraft-cli export --list-presets apv
filmcraft-cli --project edit.fcproj render --seconds 0 --out frame.png --scale 0.5
filmcraft-cli --project edit.fcproj --save-as edited.fcproj run script.jsonl
filmcraft-cli --project edit.fcproj exec perf.stats
filmcraft --control 9876
filmcraft-cli mcp
filmcraft-cli mcp --bridge 127.0.0.1:9876
```

These preview commands require an existing authorized project with a sufficient sequence range; they do not construct or copy a live GUI project. A demo operation creates synthetic content.

## Exact grammar and traps

- Use CLI `help`, not assumed subcommand `--help`. The GUI's newly improved help/unknown-option handling does not change this CLI's parser: generic `--x` tokens can be consumed as flags. Verify the returned effect, not only the exit code. `--version`/`-V` also work after parsed global options; use the matching parser rather than guessing flag consumption.
- Global `--project` chooses the project. Without a project/demo the headless engine starts empty. `--save` writes back; `--save-as` writes a new project. `--bridge` and `--project`/`--demo` are mutually exclusive.
- Parameters are one JSON object or `key=value` pairs; values parse as JSON when possible and dotted keys nest. `run script.jsonl` expects one `{"id":"COMMAND","params":{...}}` per line; `-` reads stdin. Inspect per-line `ok`/`error` when `--keep-going` is used. Exit 0/1/2 means success/command failure/usage error.
- Timeline values are integer ticks at 254016000000 ticks/second. Use a documented `seconds`, `frame` or `timecode` alternative where available; `sourceIn`/`duration` tick parameters are not seconds.
- `export` waits for the job. It accepts a preset/format, `--range entire|inOut|workArea`, paired `--start`/`--end` seconds, `--settings JSON`, `--scale`, `--quality`, `--no-audio`, and `--queue`. The default is current In/Out if set, otherwise the whole sequence. For a full-sequence deliverable, set `--range entire` explicitly. Supply both custom range endpoints; a lone endpoint is not a reliable bounded export. `--settings` is camelCase ExportSettings JSON merged over the preset.
- Extension inference remains `.mp4`/`.m4v` → H.264, `.mov` → ProRes, `.mxf` → MXF OP1a. APV or HEVC require an explicit format or matching preset; `.mov` alone does not request APV. `render` produces one headless PNG frame and rejects bridge mode; it is not a movie export.

`export --gpu-rendering off|auto` accepts a separated value. GPU export rendering is optional and distinct from hardware encoding; check backend/fallback diagnostics. ProRes `proresProfile` supports `proxy`, `lt`, `standard`, `hq`, `4444`, `4444xq`; alpha needs a compatible profile and settings. `--format aac` writes AAC-LC in `.m4a`, or ADTS for `.aac`. Use explicit formats for image sequences and inspect the numbered output set.

## Editing and interchange changes

`sequence.inspect` includes `end`, `endFrame`, `sourceOut`, `reverse`, `gainDb`, and marker `comment`, alongside existing start/source-in/duration and track state. Use these to verify edits and restored projects.

- Selection-based commands can operate on schema-documented explicit `clips`/`clip` or `items`/`item` targets without selecting them; other prerequisites still apply. Unknown named tracks now error instead of choosing another track.
- `timeline.place` uses `track` for picture and `audioTrack` for sound; supplying an audio track as `track` places sound alone there.
- `timeline.move {moves:[{clip,track,time}],insert?,linked?}` follows linked partners while Linked Selection is on unless `linked:false`. Partners can overwrite destination material; locked partners stay in place. Inspect every returned moved/overwritten clip and audiovisual sync, not just the requested video clip. Ripple/speed changes also need before/after checks across later split edits.
- Nested sequence safety/rendering/interchange and reopening after interchange import improved. Reopen the saved `.fcproj` and verify nested sizing, speed, effects, captions and audio. `file.exportInterchange` accepts `edl|xml|fcpxml|otio|aaf|omf`; unknown formats now fail, and unsupported titles are named in warnings. AAF may carry nested compositions, OMF renders nested sound, and EDL uses reel AX for nests; these are not interchangeable fidelity guarantees.

## Codecs, hardware and prerequisites

The CLI/source support H.264, HEVC, ProRes, DNxHR, APV, MJPEG, MXF OP1a/OP-Atom, PNG/TIFF/BMP/JPEG/Targa/DPX/OpenEXR sequences, GIF, WAV/AIFF and AAC audio. Some README paragraphs still say no HEVC export; use the pinned export/platform source to resolve that stale wording.

- **APV:** new QuickTime export via `--format apv` or an APV preset. The command schema documents `apvProfile: 422-10|422-12|444-10|444-12`; default is 422-10. Inspect actual codec/profile/bit depth in the output and verify playback in its intended reader. A profile label does not prove all source/render stages retain that precision.
- **Windows decode:** Media Foundation with D3D11/DXVA for supported H.264, HEVC, VP9 and AV1. Support depends on GPU profile/size and the installed decoder MFT; HEVC/VP9/AV1 may need Microsoft's codec extensions. Unsupported profiles (including 4:2:2/4:4:4), missing extensions/drivers or unavailable hardware fall back to the app's software decoder where supported. Windows N can run without the Media Feature Pack using software. Do not install extensions or drivers as an incidental workaround.
- **H.264 hardware export:** off by default; `file.exportMedia` accepts `hardwareEncoding:"auto"` (or use `--settings` with that key). macOS uses VideoToolbox; Windows uses an NVIDIA GPU/driver's NVENC. It is 8-bit SDR 4:2:0 and declines unsupported configurations such as two-pass VBR, HDR or MXF to software. A mid-export hardware failure is an error, not a resumable software handoff. Output is machine-dependent.
- **HEVC/AV1 export:** there is no built-in software encoder. Formats are offered only when a hardware encoder registers them. HEVC support includes Windows NVENC and macOS VideoToolbox; Main 10 PQ/HLG requires a backend that reports HDR availability, otherwise HDR is tone-mapped to SDR. Query available formats and test a short output on the actual host.
- **Diagnostics:** `perf.stats` exposes `decode.hardware`/backend and `export.hardware` counters. Read them in the same session that did the work; a fresh CLI process does not retain previous counters. A registered backend is not proof any frames used it. Linux H.264/HEVC hardware decoding is backend-dependent (VA-API or supported NVIDIA paths); export compositing/Lumetri/keys can still be CPU-bound on other platforms.
- Camera RAW and VST3/Audio Units/OpenFX hosting remain unsupported; E-AC-3 decoding and hardware-dependent AV1 export are documented in this release. Caption interchange is SRT/WebVTT/SCC; verify timing and whether captions are burned in or sidecar files.

## Speech-to-text and job lifecycle

Recognition and model downloading are optional build features, off by default. In builds without them, `transcript.generate`/download commands are disabled with an explicit reason; installing model files cannot add a missing build feature. Supplied transcripts still work through `transcript.set` and editing commands. Recognition is synchronous and models are separate authorized downloads. Do not start voice-over recording as a workaround.

`file.exportMedia {wait:true}` now runs as a responsive job in bridge mode as well as headless. Without `wait`, inspect `jobs.list` and the final job result; export queue items must reach `done`. `etaSeconds` can be null and is an estimate. MCP export cancellation removes partial outputs/sidecars; inspect status before retrying. `render_frame`/`render_preview` leave the prior playhead/selection unchanged in this version.

## Live control and verification

Live mode uses `--bridge`, not `--connect`, against the task's verified session. The control port is unauthenticated loopback JSON-lines, not HTTP; enable it only while needed. Invalid/non-request input or lines over 4 MiB close the connection, with at most 16 concurrent connections. Inspect errors and state before reconnecting/replaying a mutation.

Reopen the saved native project and play the complete output. Check first/last frames and edit boundaries, duration, frame rate/size, codec/profile, caption timing, nested sequences, offline media and audio sync/levels. Inspect interchange warnings and job results. File existence, successful export initiation or nominal hardware availability alone is insufficient.

## Changes and verification for 0.6.0

The export source adds hardware-dependent AV1, ProRes 4444/4444 XQ alpha, JPEG/Targa/DPX/OpenEXR sequences and audio-only AAC. Check the actual encoder availability, export settings and complete output. Source capability does not establish GPU support or codec fidelity on the host. This review does not include launching the application or executing these new workflows.

## Source links

- [Target-version release and changelog](https://github.com/storytold/filmcraft/releases/tag/v0.6.0)
- [CLI entrypoint](https://github.com/storytold/filmcraft/blob/v0.6.0/apps/filmcraft-cli/src/main.rs) and [argument parser](https://github.com/storytold/filmcraft/blob/v0.6.0/apps/filmcraft-cli/src/args.rs)
- [Engine command schemas and inspection](https://github.com/storytold/filmcraft/blob/v0.6.0/crates/engine/src/commands.rs)
- [Export formats/settings](https://github.com/storytold/filmcraft/blob/v0.6.0/crates/export/src/lib.rs) and [parameter merge/queue](https://github.com/storytold/filmcraft/blob/v0.6.0/crates/engine/src/export_tools.rs)
- [Platform capabilities and limits](https://github.com/storytold/filmcraft/blob/v0.6.0/crates/platform/README.md) and [registration](https://github.com/storytold/filmcraft/blob/v0.6.0/crates/platform/src/lib.rs)
- [Agent workflow, jobs and MCP](https://github.com/storytold/filmcraft/blob/v0.6.0/docs/agents.md)
- [Control protocol](https://github.com/storytold/filmcraft/blob/v0.6.0/docs/control-protocol.md)
- [Transcript build/model limits](https://github.com/storytold/filmcraft/blob/v0.6.0/docs/transcripts.md)
- [README](https://github.com/storytold/filmcraft/blob/v0.6.0/README.md)
- [Windows packaging](https://github.com/storytold/filmcraft/blob/v0.6.0/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
