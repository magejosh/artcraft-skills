# VectorCraft 0.7.0: CLI and format reference

## Evidence and use

Checked against official tag v0.7.0, commit `af7a5239be4636035abf7ecf79e6b0b8d274c7c3`, with intervening 0.5/0.6 release notes and the exact CLI, format schemas and control documentation. These are source/documentation findings, not a claim of execution-tested Windows behavior. Recheck after upgrading and prefer matching-version documentation over main.

Bare `vectorcraft-cli` and `vectorcraft` names below are grammar shorthand. Resolve each executable as described in SKILL.md, substitute authorized paths for synthetic relative examples, and preserve source files. No runtime helper scripts or executables are bundled with this skill.

For JSON arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Validate JSON and inspect received/resulting values. This CLI has no `run --script` fallback; use verified argument transport rather than transferring another app's flags.

## Supported command examples

```text
vectorcraft-cli --version
vectorcraft-cli --help
vectorcraft-cli commands
vectorcraft-cli info artwork.vectorcraft
vectorcraft-cli info input.eps
vectorcraft-cli run --in artwork.vectorcraft --export artwork.svg --export artwork.pdf
vectorcraft-cli run --in artwork.vectorcraft --cmd document.inspect --params '{"depth":0}'
vectorcraft-cli run --in artwork.vectorcraft --cmd document.find --params '{"kind":"Type","limit":20}'
vectorcraft-cli run --cmd file.new --params '{"colorMode":"cmyk"}' --export blank.vectorcraft
vectorcraft-cli convert artwork.vectorcraft artwork.png --scale 2 --artboard 0
vectorcraft-cli convert artwork.vectorcraft selected.pdf --range 1-3,5
vectorcraft artwork.vectorcraft
```

These live-control forms require a verified, authorized session:

```text
vectorcraft --control 7979
vectorcraft-cli mcp --headless
vectorcraft-cli mcp --connect 127.0.0.1:7979
```

## Exact grammar

- `run` supports `--in/-i`, repeated `--cmd/-c ID` followed by `--params/-p JSON-OBJECT`, repeated `--export/-o FILE`, and `--scale/-s`. Export steps occur in sequence among commands, so place them after the intended edits. No `run --save`, `--sample`, `--script`, `--connect`, `--artboard`, or `--range`.
- `convert IN OUT` accepts `--scale/-s`, zero-based `--artboard/-a`, one-based `--range/-r` (for example `1-3,5`) and `--outline-text`. Use one artboard selector. PDF defaults to all artboards; most other formats default to the first; EPS uses visible art bounds. `--outline-text` is for SVG paths, not a promise to outline every output format.
- `commands` emits the JSON catalogue without a filter or separate describe/app subcommand. `--version` and top-level `--help` are supported. Do not assume ignored trailing arguments are valid filters or that subcommands implement their own help.
- `info FILE` now includes import warnings, title/color information, artboards, object counts by kind and fonts. `run` emits JSON per step; review every result and warning. No output file is created for query-only runs.
- Rich per-format settings are engine-command parameters, not arbitrary CLI flags. Discover `document.formats` before using `document.export`, `document.exportPdf`, `document.exportEps` or screen-export commands. Account for every returned `files` and `linked` sidecar, not just the requested path.

## Bounded document inspection

Prefer `document.inspect {depth:0}` for a skeleton, then `document.find {name?,kind?,text?,limit?}` and `document.node {id,summary:true,depth?,childLimit?}`. Find requires a filter; all supplied filters must match. Matching is case-insensitive; name/text are substrings, kind is the exact panel label. Limit defaults to 100; zero counts only. Results contain `total` plus matches and their ancestor paths.

Node `depth` and `childLimit` must be nonnegative integers and require `summary:true`; depth zero returns only the node. A truncated level reports `childCount`. Full `document.node` JSON and `document.json` remain unsliced fidelity reads. Obtain IDs from the current document; never reuse IDs from another run.

## Formats and upgrade routing

- Native `.vectorcraft/.drawcraft/.vctemplate`; SVG/SVGZ; PDF/PDF-compatible AI/AIT; EPS/PostScript AI; DXF; EMF/WMF; PNG/JPEG/GIF/WebP/TIFF/BMP are readable according to `document.formats`. PSD and TGA remain export-only; do not infer import support from their presence in output lists.
- The 0.5–0.7 changes improve EPS interpretation as vector paths, colors, clipping, gradients, images and text. Unsupported PostScript can fall back to its TIFF preview with a reason in `warnings`. Check object kinds and preview: a successful `info`/convert may still represent raster fallback.
- PDF/AI import improves live text/strokes, wrapped lines, CMYK/spot colors, nested/hidden layers and layer order. `document.open` supports page selection and `textAs:text|outlines`; fonts are resolved by name with warnings for missing ones. Native data embedded by Preserve Editing can restore a drawing only when valid and applicable; otherwise artwork is imported with a warning. Reopen and inspect editable type and layers before promising fidelity.
- SVG/PDF/EPS/DXF/EMF/WMF and raster exports have different loss behavior. PDF artboard indices, source PDF page selection and returned file lists must be checked independently. Outlining improves font independence but removes text editability.
- WebP export is lossless; asking for lossy emits a warning and still writes lossless. PSD output is at most 30,000 pixels per side; default layers are top-level pixel layers, while `maxEditability:true` writes finer layer/group structure with clipping/masking exceptions. It does not preserve vector editing.
- Later GUI work adds better pen/anchor modifiers, per-corner Live Corners, snapping, artboard copying, floating panels, horizontal CJK composition and bidirectional type. Initial vertical type still has CJK composition gaps; 3D/materials, raster Effect Gallery and scripting remain limited. Inspect exact controls instead of guessing menu behavior from another application.

## Live control and prerequisites

Choose explicit `mcp --headless` or `mcp --connect HOST:PORT`; they are mutually exclusive. Bare MCP tries the live default port and silently falls back headless, risking work in the wrong document. Control is loopback and unauthenticated; enable only for a needed authorized task, verify process/document ownership and do not expose or reuse an unrelated listener. GUI supports `VECTORCRAFT_CONTROL_PORT`; it has no `--sample`. Preferences live in application data, so a portable executable does not imply isolated settings.

Windows packages statically link the C runtime; optional craft-fonts is included in official builds with system fallback. Canvas rasterization is CPU-based, while UI compositing requires a working GPU adapter. Windows prefers DX12 before Vulkan on a given adapter and can retry another adapter on startup failure. Do not equate successful headless conversion with GUI/GPU compatibility, install source-build tooling, or run the large `bench`/`perf` defaults merely to check installation.

## Source links

- [Target release](https://github.com/storytold/vectorcraft/releases/tag/v0.7.0)
- [0.5 capability changes](https://github.com/storytold/vectorcraft/releases/tag/v0.5.0)
- [0.6 changes](https://github.com/storytold/vectorcraft/releases/tag/v0.6.0)
- [Exact CLI parser](https://github.com/storytold/vectorcraft/blob/v0.7.0/apps/vectorcraft-cli/src/main.rs)
- [Format and import/export schemas](https://github.com/storytold/vectorcraft/blob/v0.7.0/crates/engine/src/cmd/fileio/mod.rs)
- [Import implementation](https://github.com/storytold/vectorcraft/blob/v0.7.0/crates/engine/src/cmd/fileio/load.rs)
- [MCP and bounded reads](https://github.com/storytold/vectorcraft/blob/v0.7.0/docs/mcp.md)
- [Control protocol](https://github.com/storytold/vectorcraft/blob/v0.7.0/docs/control-protocol.md)
- [Graphics and fonts](https://github.com/storytold/vectorcraft/blob/v0.7.0/docs/development.md)
- [Windows packaging](https://github.com/storytold/vectorcraft/blob/v0.7.0/packaging/windows/package.ps1)
