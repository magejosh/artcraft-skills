# PhotoCraft 0.6.0: CLI and format reference

## Evidence and use

Checked against official tag v0.6.0, commit `0c72d95425dece90ef9a1cceb49e3315c96e22d5`, including the parser, command documentation, format capabilities and packaging source. These are source/documentation findings, not a claim that these examples or Windows GUI paths were execution-tested. Recheck after upgrading and prefer matching-version documentation over main.

Bare `photocraft-cli` and `photocraft` names below are grammar shorthand. Resolve each executable as described in SKILL.md; replace synthetic relative filenames with authorized inputs and distinct outputs. No runtime helper scripts, models, or executables are bundled with this skill.

For JSON arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Validate JSON before invocation and inspect received values/results; do not copy Unix quoting blindly. `run` does not have a script-file flag. A batch actions file is a different operation, affecting every recognized image in its input directory.

## Supported command examples

```text
photocraft-cli --version
photocraft-cli --help
photocraft-cli commands --json --filter actions.
photocraft-cli info input.psd --compact
photocraft-cli run input.psd --cmd image.adjustments.invert --out inverted.png
photocraft-cli convert input.psd flattened.tif
photocraft-cli convert input.psd layered.tif --tiff-layers
photocraft-cli convert input.psd preview.webp --quality 90
photocraft-cli batch --actions grade.json --in input-copies --out graded --format psd
photocraft input.psd
```

These server forms are for separately authorized control workflows, not routine installation checks:

```text
photocraft-cli mcp --automation-read-root READ_DIR --automation-write-root WRITE_DIR
photocraft --control 7878 --control-token-file PRIVATE_TOKEN_FILE --automation-read-root READ_DIR --automation-write-root WRITE_DIR
photocraft-cli mcp --bridge 127.0.0.1:7878 --control-token-file PRIVATE_TOKEN_FILE
photocraft-cli serve --automation-read-root READ_DIR --automation-write-root WRITE_DIR
```

READ_DIR, WRITE_DIR and PRIVATE_TOKEN_FILE are placeholders, not ready-to-run values. Confirm process ownership, token-file protection, roots and permission before launching a listener or persistent session.

## Exact grammar and changes

- `run` requires exactly one input file or `--new JSON`; each `--params JSON` belongs to the preceding `--cmd ID`. Repeated commands execute in order. Without `--out`, ordinary edits are not saved. An output-only run is accepted.
- `convert IN OUT`, `run`, and `batch` accept `--format EXT`, `--quality 1..100`, and the new bare `--tiff-layers`. TIFF is flat unless layers are requested. `--quality` controls JPEG/WebP: WebP is lossless without it and lossy with it.
- `batch --actions FILE --in DIR --out DIR` accepts action steps as `[id, params]`, `{command, params}` (also `id`), or bare command IDs, optionally wrapped in `actions`, `steps`, or a droplet. Input extensions are retained unless `--format` is specified. Stage only the intended files. Same input/output directory requires `--in-place`; a separate directory is safer.
- `droplet FILE.pcdroplet FILE-OR-DIR... [--out DIR]` executes saved automation. Review its paths and steps before use.
- `commands [--json] [--filter TEXT]` lists IDs and parameter documentation. Top-level `--version` and subcommand `--help` are supported. Unknown flags are usage errors (exit 2); operation failures return 1. Inspect warnings and each JSON result, not only process status.
- CLI paths are ordinary OS paths. MCP roots do not confine one-shot CLI `run`, `convert`, `batch` or droplet actions.

## Actions, type and live control

Use discovered schemas for new `actions.list/get/record/stop/play/delete` commands. `actions.get {action: name-or-index}` returns `{name, steps:[[id,params],...]}`. `actions.play` accepts optional zero-based `from`; a result can be successful at the outer level but contain `failed:{step,id,error}` after a partial run. Check `ran` and `failed`, preserve partial-output context, and do not blindly replay it. Recorded actions omit query and action-control entries. GUI action state persists; recording is not a read-only probe.

`type.hitTest`, `type.caret`, and `type.navigate` provide document-coordinate/character-index editing aids; inspect the actual text layer and schema before using them. `layer.removeBackground` is a mask-based cutout, not proof of a generative fill capability. Camera Raw smart-filter settings, smart-object placement, and multi-instance effects need a save/reopen check.

Headless MCP/serve use explicit read/write roots; absent roots grant no corresponding filesystem access. Desktop bridge paths are relative to its launch-time roots and reject absolute paths and escapes. TCP control authenticates before dispatch. Prefer token files; never expose token values in chat, logs, args or skills. A missing token file may be created, an existing one reused. Changes to ongoing access or file protection need the task's appropriate authorization.

Over desktop control, use root-scoped `app.open`/`app.save`, not `file.open/save/saveAs/saveACopy`. Ambient-path commands, path-bearing preset/plugin operations, file-backed preference updates and desktop `image.mode.*` are restricted. Action playback does not bypass these restrictions. Use an authorized one-shot workflow or the GUI when necessary; never route around an access denial.

## Formats, metadata and fidelity

- Native `.pcraft`, PSD/PSB and layered TIFF preserve editable structures only to the extent the importer/exporter supports them. PSDT opens as an untitled template in the GUI. TIFF layers require `--tiff-layers` for CLI convert/run/batch or `tiffLayers:true` on documented save/export surfaces. Lab TIFF stays flat; extra alpha channels are not written. Reopen the TIFF and compare layers, masks and composite, rather than trusting its extension.
- PNG/JPEG/TIFF/WebP/GIF/BMP/TGA/ICO/PNM/PFM/QOI/OpenEXR/Radiance HDR have codec paths. Official releases include optional read-only HEIC/HEIF; a build without the feature recognizes the format but reports it unsupported. AVIF encoding is optional and AVIF decoding is not implemented. Animated/multipage inputs currently import one frame/page with a warning.
- Default flat-codec decode limits are 262,144 pixels per dimension, 268,435,456 pixels total and 2 GiB decoded allocation. These are codec limits, not a universal PSB size guarantee. Keep limits enabled; do not relax them for untrusted inputs. Large PSB improvements do not replace memory and layer-depth validation.
- JPEG and Radiance HDR flatten transparency over white. Formats without ICC support convert RGB to sRGB, or linear sRGB for EXR/HDR; verify profiles and pixel values.
- Metadata behavior is surface-specific. Exact source sets CLI conversion/save defaults to full document XMP; Export As starts at `metadata=none`. Layered PSD/PSB/.pcraft preserve full XMP. Do not treat CLI conversion as sanitization or invent a `--metadata` flag. A choice about XMP is not evidence that all EXIF/location data is removed. Inspect actual metadata before sharing.
- Windows portable packaging includes the CLI/GUI and `portable.txt`; the marker redirects state to adjacent PhotoCraftData, with an application-data fallback if unwritable. Preserve that state. The C runtime is statically linked; Rust/SDK/WiX requirements in the packaging script concern building, not portable use.

## Changes and verification for 0.6.0

SVG opens as editable shape layers and places as a vector smart object. CLI info, convert and run report missing-font fallbacks. Layered TIFF and metadata handling improve; inspect layer structure, warnings and metadata rather than assuming lossless preservation or sanitization. A bridge edit with a lost reply must not be blindly replayed. This review does not include launching the application or executing these new workflows.

## Source links

- [Target release and changes since 0.3.0](https://github.com/storytold/photocraft/releases/tag/v0.6.0)
- [Exact CLI parser](https://github.com/storytold/photocraft/blob/v0.6.0/apps/photocraft-cli/src/lib.rs)
- [CLI guide](https://github.com/storytold/photocraft/blob/v0.6.0/book/src/automation/cli.md)
- [MCP guide](https://github.com/storytold/photocraft/blob/v0.6.0/book/src/automation/mcp.md)
- [Control, actions and type methods](https://github.com/storytold/photocraft/blob/v0.6.0/docs/control-protocol.md)
- [Automation restrictions](https://github.com/storytold/photocraft/blob/v0.6.0/crates/automation/src/workspace.rs)
- [Raster formats and layered TIFF](https://github.com/storytold/photocraft/blob/v0.6.0/book/src/formats/raster-formats.md)
- [Export defaults](https://github.com/storytold/photocraft/blob/v0.6.0/crates/io/src/lib.rs)
- [Export As metadata default](https://github.com/storytold/photocraft/blob/v0.6.0/crates/ui-egui/src/export_dialog.rs)
- [Windows packaging](https://github.com/storytold/photocraft/blob/v0.6.0/packaging/windows/package.ps1)
