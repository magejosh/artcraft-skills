# LightCraft 0.4.0: CLI and format reference

## Evidence and use

Checked against official tag v0.4.0, commit `2472021091a28eb93a05947cfc9b941d3911543a`, including CLI parsing, export implementation, camera-look and AI-mask documentation. These are source/documentation findings, not a claim that these examples or Windows UI paths were execution-tested. Recheck after upgrading and prefer matching-version documentation over main.

Bare `lightcraft-cli` and `lightcraft` names below are grammar shorthand. Resolve each executable as described in SKILL.md, substitute authorized inputs for synthetic relative filenames and preserve originals. No runtime helper scripts, models or executables are bundled with this skill.

For JSON arguments, verify native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer the documented JSONL script form for command chains, validate its JSON, and inspect every response. Do not copy Unix paths/quoting blindly.

## Supported command examples

```text
lightcraft-cli --version
lightcraft-cli --help
lightcraft-cli controls --json
lightcraft-cli commands --json
lightcraft-cli run presets.list
lightcraft-cli render photo.jpg -o edited.jpg --set light.exposure=0.5 --size 1024 --opt metadata=none
lightcraft-cli render input.dng -o edited.tif --opt colorSpace=displayP3 --opt bitDepth=16 --opt percent=50
lightcraft-cli run --import photo.jpg develop.set control=light.exposure value=0.7 app.export path=edited.png longEdge=1024
lightcraft-cli run --library library-copy --script steps.jsonl
lightcraft-cli snapshot --demo -o interface.png --size 800x600 --scale 1
lightcraft-cli calibrate --max 20 --out profile-copies raw-copies
lightcraft --memory
```

`library-copy`, `steps.jsonl`, `raw-copies` and `profile-copies` are synthetic paths. Persistent library runs and calibration write state; execute them only as part of the authorized workflow. For separately approved live control, use `lightcraft --control 7980` and `lightcraft-cli run --connect 127.0.0.1:7980 ui.inspect` or `lightcraft-cli mcp --connect 127.0.0.1:7980`.

## Exact grammar and export behavior

- `render INPUT -o OUTPUT` accepts repeated `--set CONTROL=NUMBER`, `--settings FILE`, `--preset ID`, `--size N`, `--quality Q`, `--opt KEY=VALUE`. It applies preset, then settings JSON, then individual control values regardless of option order. Default size is full cropped resolution; set a bounded size for a trial.
- Preset lists have expanded; discover IDs with `run presets.list`, then use `--preset` or the `preset.apply` command. A dot is not a preset and the old four-ID list is not exhaustive.
- `--opt` values parse as JSON or strings and are merged after `--size`/`--quality`, so explicit export options can override them. Format normally follows the output extension; an explicit `format` option wins. Match the extension, encoded format, bit depth and color profile deliberately.
- Export metadata defaults to all. For rendered exports, `--opt metadata=none` omits descriptive metadata while retaining ICC where supported; AVIF always uses sRGB without an embedded profile. Original/DNG take a separate path that bypasses this metadata filter: `format=original` copies source bytes unchanged plus an XMP settings sidecar, and DNG embeds its settings packet. Neither is a sanitized export or a baked edit. Verify both output and sidecars. Render checks originals/sidecars against overwrite, including differently named symlinks; this guard is not permission to overwrite other files.
- `run` supports `--demo`, `--library`, repeated `--import`, `--connect`, `--script FILE|-`, and `--keep-going`. Tokens without `=` start commands; values parse as JSON or strings. JSONL records accept `{command,params}` or `{method,params}`. Inspect each `ok/result/error` record and stop on failure unless a deliberate keep-going workflow was requested.
- `--version` and top-level `--help` are supported. Use a full `HOST:PORT` with separated `--connect`; the optional address recognizer requires a colon. Bare `--connect` uses the default port. The connection-failure hint now reports the actual attempted port.

## Snapshot and merge routing

`snapshot [--demo|--library DIR] [--script FILE] [-o OUT.png] [--size WxH] [--scale S] [FILES...]` runs the full UI headlessly on CPU, with no desktop window or GPU. Defaults are 1600×1000 points at scale 1. JSONL scripts can send `ui.settle {timeoutMs?}` and `ui.screenshot`; inspect settled state before judging a preview. Screenshots are UI images, not photo exports. A persistent library or supplied files still have normal library/import semantics.

The CLI also has `merge hdr|panorama|hdr-panorama` and `synth-merge`. Actual merges normally write a new DNG beside the first input; `--preview OUT.png` renders a bounded preview instead. Inspect top-level help and use copied inputs before an authorized merge. Do not confuse HDR merge with unsupported HDR display/export behavior or run these as installation checks.

## RAW, profiles and library changes

- DNG uses embedded camera matrices and profile HueSatMap/LookTable/ToneCurve. ARW/NEF/RW2 can fit a starting look to their embedded camera JPEG when calibration is absent; output pixels still come from the RAW mosaic. Failed fits retain fallback behavior. Older Sony metadata and downsized lossless ARW, Nikon 12-bit black levels, and Panasonic RW2/RAW/Leica RWL support improve in this release.
- CR3 reads fuller container previews/metadata but remains embedded-preview-only. Compressed RAF/ORF remain preview-only. Treat temporary camera JPEGs during culling as stand-ins, not successful RAW development; wait for `source:render` and settled jobs before evaluating a decoded image.
- `calibrate [--max N] [--out DIR] INPUTS...` scans ARW/NEF/NRW, with 300 files default and zero meaning all; at least five usable photos per camera model are needed. RW2 is not collected by this command. Explicit `--out` avoids writing into the live profile directory; otherwise `LIGHTCRAFT_CAMERA_PROFILES` or the application config's `camera-profiles` is used. New profiles there affect later rendering and are read once per process.
- A built-in ILCE-7M4 profile ships in source. Profiles are camera-look estimates, not measured spectral calibration or a guarantee of matching another application. Uncalibrated Sony/Nikon/Panasonic white balance is relative around the as-shot look; do not present its neutral 6500/0 reference as measured capture temperature.
- XMP face regions can appear in loupe/People views; this is imported metadata, not evidence of face recognition. Recently Deleted restoration, stable-seed random sorting/reshuffle and File Path smart-album rules are available. These library mutations need the intended library and scope, not a generic preview.
- JPEG/PNG/TIFF/WebP and other common raster decoders, PSD composites and JPEG XL are documented; export supports JPEG/PNG/TIFF/lossless WebP/AVIF/DNG/original. Build features can limit AVIF/JPEG XL. Preserve original files and disclose composite-only/preview-only inputs.

## Optional AI masks and prerequisites

Object and Describe masks use optional SAM 3, distinct from heuristic Subject/Sky masks. At this tag the desktop enables the feature; a standalone default CLI build and the web build omit it. Windows packaging builds the desktop and CLI together, so shared engine features may differ from a standalone CLI build. Metal accelerates it on macOS; Windows/Linux use CPU. Discover `segment.model.status` through the intended session to check `available`, `installed`, `busy` and download state. Merely finding a command in a schema does not establish a usable model.

The weights are approximately 3.4 GB, not bundled, and governed by a separate license. Built-in download mirrors are empty at this tag; user-configured mirrors or a separately authorized model installation are needed. Do not download weights, set credentials, configure persistent access, or send `segment.model.download {acknowledged:true}` without the necessary user approval and license disclosure. Never copy tokens from documentation into commands or notes.

Mask coordinates are normalized to the uncropped, oriented photo. Object clicks are capped at 64, and a selection retains at most four bounded detail patches. Desktop mask commands can return `pending:true`; wait for completion before checking mask/export results. Headless model-capable builds wait. Stored segmentation renders/exports without the model; changing the photo's look does not automatically recompute it.

Windows portable packages statically link the C runtime and include release fonts; no model is needed for ordinary development/export. Do not install Rust, Windows SDK, WiX or Python model-reference dependencies just to run the portable app.

## Live control and persistence

Control is unauthenticated loopback; use it only for a verified task-owned process. Never open a persistent library in another headless process while the GUI owns it; connect to the owning app instead. `--memory` is throwaway; `--library` saves edits. Bare GUI launch opens its default Pictures library, and a folder launch scans/imports. A portable package is not necessarily a separate library/configuration sandbox.

## Source links

- [Target release and changes since 0.2.1](https://github.com/storytold/lightcraft/releases/tag/v0.4.0)
- [Exact CLI parser](https://github.com/storytold/lightcraft/blob/v0.4.0/apps/lightcraft-cli/src/main.rs)
- [Preset catalogue](https://github.com/storytold/lightcraft/blob/v0.4.0/crates/engine/src/presets.rs)
- [Export behavior and metadata](https://github.com/storytold/lightcraft/blob/v0.4.0/crates/engine/src/export.rs)
- [Camera-look estimates and profiles](https://github.com/storytold/lightcraft/blob/v0.4.0/docs/camera-preview-colour.md)
- [AI-mask requirements and commands](https://github.com/storytold/lightcraft/blob/v0.4.0/docs/ai-masks.md)
- [MCP guide](https://github.com/storytold/lightcraft/blob/v0.4.0/docs/mcp.md)
- [Control and headless snapshots](https://github.com/storytold/lightcraft/blob/v0.4.0/docs/control-protocol.md)
- [Codec capabilities](https://github.com/storytold/lightcraft/blob/v0.4.0/crates/codecs/src/lib.rs)
- [Windows packaging](https://github.com/storytold/lightcraft/blob/v0.4.0/packaging/windows/package.ps1)
