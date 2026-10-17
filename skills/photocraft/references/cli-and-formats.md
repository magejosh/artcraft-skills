# PhotoCraft 0.9.0: CLI and format reference

## Evidence and use

Checked against official tag v0.9.0, commit `c699e3cda69f4852b43c0b191ab0091aaeff9d6a`, including the parser, command documentation, format capabilities and packaging source. These are source/documentation findings, not a claim that these examples or Windows GUI paths were execution-tested. Recheck after upgrading and prefer matching-version documentation over main.

Bare `photocraft-cli` and `photocraft` names below are grammar shorthand. Resolve each executable as described in SKILL.md; replace synthetic relative filenames with authorized inputs and distinct outputs. No runtime helper scripts, models, or executables are bundled with this skill.

For JSON arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Validate JSON before invocation and inspect received values/results; do not copy Unix quoting blindly. `run` does not have a script-file flag. A batch actions file is a different operation, affecting every recognized image in its input directory.

## Supported command examples

```text
photocraft-cli convert input.pcraft frame.dpx --dpx-bits 10
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
- `convert IN OUT`, `run`, and `batch` accept `--format EXT`, `--quality 1..100`, and bare `--tiff-layers`. TIFF is flat unless layers are requested. `--quality` controls JPEG/WebP: WebP is lossless without it and lossy with it.
- `batch --actions FILE --in DIR --out DIR` accepts action steps as `[id, params]`, `{command, params}` (also `id`), or bare command IDs, optionally wrapped in `actions`, `steps`, or a droplet. Input extensions are retained unless `--format` is specified. Stage only the intended files. Same input/output directory requires `--in-place`; a separate directory is safer.
- `droplet FILE.pcdroplet FILE-OR-DIR... [--out DIR]` executes saved automation. Review its paths and steps before use.
- `commands [--json] [--filter TEXT]` lists IDs and parameter documentation. Top-level `--version` and subcommand `--help` are supported. Unknown flags are usage errors (exit 2); operation failures return 1. Inspect warnings and each JSON result, not only process status.
- CLI paths are ordinary OS paths. MCP roots do not confine one-shot CLI `run`, `convert`, `batch` or droplet actions.

`convert` and `run` accept `--tga-bits 24|32` for TGA output. Batch can select a named action with `--action`; discover the action set before choosing it. A failed recorded action now makes `run` fail; earlier steps may still have taken effect.

## Actions, type and live control

Use discovered schemas for new `actions.list/get/record/stop/play/delete` commands. `actions.get {action: name-or-index}` returns `{name, steps:[[id,params],...]}`. `actions.play` accepts optional zero-based `from`; a result can be successful at the outer level but contain `failed:{step,id,error}` after a partial run. Check `ran` and `failed`, preserve partial-output context, and do not blindly replay it. Recorded actions omit query and action-control entries. They can now record Save/Save As: review the steps and destinations before replay. Batch/droplet execution skips recorded view and save steps; a failure inside a called action fails the file rather than silently succeeding. GUI action state persists; recording is not a read-only probe.

`type.hitTest`, `type.caret`, and `type.navigate` provide document-coordinate/character-index editing aids; inspect the actual text layer and schema before using them. `layer.removeBackground` is a mask-based cutout, not proof of a generative fill capability. Camera Raw smart-filter settings, smart-object placement, and multi-instance effects need a save/reopen check.

Headless MCP/serve use explicit read/write roots; absent roots grant no corresponding filesystem access. Desktop bridge paths may be relative to its launch-time roots or absolute beneath the appropriate root. Absolute paths outside that root, traversal, malformed/device paths and symlink escapes remain refused. The tagged control guide still contains an older blanket absolute-path warning; the updated workspace implementation and its tests define the accepted in-root behavior. TCP control authenticates before dispatch. Prefer token files; never expose token values in chat, logs, args or skills. A missing token file may be created, an existing one reused. Changes to ongoing access or file protection need the task's appropriate authorization.

Over desktop control, use root-scoped `app.open`/`app.save`, not `file.open/save/saveAs/saveACopy`. Ambient-path commands, path-bearing preset/plugin operations, file-backed preference updates and desktop `image.mode.*` are restricted. Action playback does not bypass these restrictions. Use an authorized one-shot workflow or the GUI when necessary; never route around an access denial.

## Formats, metadata and fidelity

- FITS `.fits`/`.fit`/`.fts` supports reading and writing grayscale/RGB U8/U16/F32 data. KRA import reads only the merged composite as one editable raster layer and warns that Krita layers were not imported. Preserve the KRA original; saving the imported raster does not round-trip its layer structure.
- OpenRaster `.ora` reads/writes raster layers and groups, names, supported blend modes, opacity and visibility. Other layer kinds export as rendered pixels; masks are applied to pixels, and unsupported structures produce warnings. Keep a PSD/.pcraft master and reopen the ORA to inspect structure and composite. Its importer has separate archive/layer limits, so the flat-codec limits below are not an ORA size guarantee.
- SVG opens as editable shape layers and places as a vector smart object; inspect unsupported features and font fallbacks.
- Native `.pcraft`, PSD/PSB and layered TIFF preserve editable structures only to the extent the importer/exporter supports them. PSDT opens as an untitled template in the GUI. TIFF layers require `--tiff-layers` for CLI convert/run/batch or `tiffLayers:true` on documented save/export surfaces. Lab TIFF stays flat; extra alpha channels are not written. Reopen the TIFF and compare layers, masks and composite, rather than trusting its extension.
- PNG/JPEG/TIFF/WebP/GIF/BMP/TGA/ICO/PNM/PFM/QOI/OpenEXR/Radiance HDR have codec paths. Official releases include optional read-only HEIC/HEIF; a build without the feature recognizes the format but reports it unsupported. AVIF encoding is optional and AVIF decoding is not implemented. Animated/multipage inputs currently import one frame/page with a warning.
- Default flat-codec decode limits are 262,144 pixels per dimension, 1,073,741,824 pixels total and 8 GiB decoded allocation on 64-bit targets (2 GiB on 32-bit targets). These are codec limits, not a universal PSB size guarantee. Keep limits enabled; do not relax them for untrusted inputs. Large PSB improvements do not replace memory and layer-depth validation.
- JPEG and Radiance HDR flatten transparency over white. Formats without ICC support convert RGB to sRGB, or linear sRGB for EXR/HDR; verify profiles and pixel values.
- Metadata behavior is surface-specific. Exact source sets CLI conversion/save defaults to full document XMP; Export As starts at `metadata=none`. Layered PSD/PSB/.pcraft preserve full XMP. Do not treat CLI conversion as sanitization or invent a `--metadata` flag. A choice about XMP is not evidence that all EXIF/location data is removed. Inspect actual metadata before sharing.
- Windows portable packaging includes the CLI/GUI and `portable.txt`; the marker redirects state to adjacent PhotoCraftData, with an application-data fallback if unwritable. Preserve that state. The C runtime is statically linked; Rust/SDK/WiX requirements in the packaging script concern building, not portable use.

## Changes and verification for 0.9.0

convert, run and batch accept --dpx-bits 8|10|12|16; the default is 8 for an 8-bit document and 16 otherwise. batch --actions accepts Photoshop .atn sets; use --action NAME for a multi-action set, inspect unsupported-step warnings and stop on failures. Krita .kra/.krz are now batch inputs but remain composite-only imports. Windows pen handling fixes do not establish actual tablet/pressure behavior on the host.

These are matching-tag source/documentation findings. The installed CLI version was checked; these editing/export workflows were not executed for this refresh.

## Previously documented behavior and verification

Automation accepts absolute paths beneath its authorized read/write roots while retaining traversal and escape checks. OpenRaster opens and saves layers/groups, with unsupported content rendered or warned about. Duplicated Smart Objects can share contents; inspect all affected instances. Recorded actions can include Save/Save As, so review output paths and nested failures before replay or batch processing. These changes do not establish lossless format preservation. This review does not include launching the application or executing these new workflows.

## Source links

- [KRA composite-only import](https://github.com/storytold/photocraft/blob/v0.9.0/crates/io/src/kra.rs)
- [OpenRaster import/export and limitations](https://github.com/storytold/photocraft/blob/v0.9.0/crates/io/src/ora.rs)
- [Codec capability declarations](https://github.com/storytold/photocraft/blob/v0.9.0/crates/codecs/src/format.rs)
- [Target release and changelog](https://github.com/storytold/photocraft/releases/tag/v0.9.0)
- [Exact CLI parser](https://github.com/storytold/photocraft/blob/v0.9.0/apps/photocraft-cli/src/lib.rs)
- [CLI guide](https://github.com/storytold/photocraft/blob/v0.9.0/book/src/automation/cli.md)
- [MCP guide](https://github.com/storytold/photocraft/blob/v0.9.0/book/src/automation/mcp.md)
- [Control, actions and type methods](https://github.com/storytold/photocraft/blob/v0.9.0/docs/control-protocol.md)
- [Automation restrictions](https://github.com/storytold/photocraft/blob/v0.9.0/crates/automation/src/workspace.rs)
- [Raster formats and layered TIFF](https://github.com/storytold/photocraft/blob/v0.9.0/book/src/formats/raster-formats.md)
- [Export defaults](https://github.com/storytold/photocraft/blob/v0.9.0/crates/io/src/lib.rs)
- [Export As metadata default](https://github.com/storytold/photocraft/blob/v0.9.0/crates/ui-egui/src/export_dialog.rs)
- [Windows packaging](https://github.com/storytold/photocraft/blob/v0.9.0/packaging/windows/package.ps1)
