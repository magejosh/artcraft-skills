# DesignCraft 0.6.0: CLI and format reference

## Evidence and use

Commands and capability notes were reviewed against upstream tag v0.6.0, commit `a9124a0517594ce9872f73637e7b841a4967bcf9`, including the parser, command schemas and release changelog. These are source/documentation findings, not a guarantee of runtime or visual behavior on a particular machine. Recheck after upgrading; earlier-version smoke tests do not certify this release.

Bare `designcraft-cli` and `designcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files. Windows portable packaging includes both executables and statically links the C runtime; no Visual C++ redistributable is required by that packaging script.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix quoting blindly.

## Supported command examples

```text
designcraft-cli --version
designcraft-cli commands data.
designcraft-cli describe data.merge
designcraft-cli describe preflight.run
designcraft-cli run --sample --all-pages out/
designcraft-cli run --in document.idml --page 0 --scale 2 --export first.png
designcraft-cli run --sample --export sample.designcraft --export sample.pdf
designcraft-cli run --sample --export sample.epub
designcraft-cli script page.dcs --save page.designcraft --export page.pdf
designcraft-cli script merge.dcs --in template.designcraft --save merged.designcraft
designcraft --sample --control 7979
designcraft-cli mcp
designcraft-cli mcp --connect 7979
```

Sample operations create synthetic content, not a copy of a GUI project. Script files may use command-per-line syntax, JSONL, or arrays of `{command,params}`; later params can reference earlier results with `$0.story`, `$last` or interpolation such as `${0.id}`.

## Exact grammar and traps

- `run` accepts `--in`, `--sample`, repeated `--cmd ID[=JSON]`, `--page`, `--scale`, `--pdf-options JSON`, repeated `--export`, and `--all-pages`. There is no `run --save`: use `--export output.designcraft`.
- `run` options execute sequentially: open/create, edit, set render/PDF options, then export. `--page` is zero-based; placed-PDF `pdfPage` and `file.exportPdf` page selections are one-based. Use lowercase suffixes because some output checks remain case-sensitive.
- `script FILE|-` accepts `--in`/`--sample`, `--connect`, `--save`, repeated `--export`, and `--keep-going`. Check `completed`, `results` and any `failedIndex`/`failedCommand`/`error`; continuing after a failure is not successful completion.
- `text.select {story,anchor,focus}` uses UTF-8 byte offsets, not character counts. Use boundaries from the actual story/find results. Carriage returns in created/typed text now start paragraphs.
- Explicit IDs can satisfy a command's selection requirement where its schema documents targets; other enablement conditions still apply. Do not change the GUI selection unnecessarily.

`designcraft-cli validate-pdf output.pdf` reads the PDF and returns `{path,standard,valid,issues}` for built-in PDF/X-4 checks; failed conformance returns a failure exit status. Put `--page`, `--scale` and `--pdf-options` before the export they affect: unused options after the final export are now errors.

## Data merge changes

`data.merge` now creates and activates a new document, leaving the template and its undo history intact. The old `spread` parameter is an error. Save the template before merging if its edits must be retained, then save the merged document to a distinct destination.

1. `data.source.select {path,sheet?}` links CSV/TSV/XLSX data; `data.fields {}` inspects linked fields. Delimited text must be UTF-8 (BOM allowed); comma/tab/semicolon delimiters are supported. `data.source.update {}` re-reads the file.
2. `data.placeholder.add {field,role?,story?,at?,end?,item?}` marks text or a frame; roles are `text`, `image`, `qr`, `hyperlink`. Inspect the schema rather than assuming plain `<<field>>` text is an attached placeholder.
3. `data.preview {record}` previews a one-based record without saving it; `data.preview.stop {}` restores the unfilled template.
4. `data.options` or `data.merge` accepts `records: all|one|range`, `one`, `range`, `perPage: single|multiple`, `arrange: rows|columns`, four `insets`, spacing, fitting, `center`, `linkImages`, and `limit`. Multiple records per page require a one-page template with facing pages off. Ranges use one-based record numbers.
5. Merge may use the linked source or inline `csv`, `rows`, `path` or `bytes`. Inspect returned `records`, `pages`, `missingImages`, `oversetStories` and `warnings`. Changed or missing linked files can use cached rows with a warning; update the source deliberately rather than delivering stale data.

For an existing template whose placeholders are already configured, `merge.dcs` could contain:

```text
data.merge {"path":"records.csv","records":"range","range":"1-2","limit":2}
preflight.run {}
```

Source limits include 100,000 nonempty data rows, 200 columns, and 256 MiB per data/image file read. Parent-page placeholders may remain unfilled and generate warnings. Preview/merge success does not prove every record fits or every image is available.

## Typography, formats and print checks

- Native `.designcraft` and IDML are supported; do not promise INDD input. Outputs include native/IDML, PNG/JPEG, PDF and EPUB. The README still has stale PDF-roadmap wording; the pinned parser and exporter implement it.
- `preflight.run {minPpi?}` reports structured severity/kind/message findings, including overset, missing fonts/glyphs/assets and unsupported typography rules. Placed PDF/SVG vectors are no longer treated as low-resolution raster images.
- CJK import/composition improves composite fonts, kinsoku boundaries, spacing, fallback and vertical metrics. Mojikumi spacing tables and kinsoku push-in/push-out priorities are retained but not executed. Arabic improves bidi, joining, digits, marks and independent story/table direction; vendor-specific kashida/diacritic presets and some RTL tab behavior remain incomplete. Preserve the warnings and inspect line breaks; serialized rules do not establish visual parity.
- Print export improves `[Paper]` no-ink behavior, CMYK transparency groups and supported CMYK TIFF ink preservation. Unsupported TIFF layouts can still convert to RGB with a warning. A placed PDF 1.7 can export in PDF/X-4 with a compatibility warning; PDF 2.0 cannot simply be relabelled. Device RGB under the CMYK output intent is reported. Inspect all warnings and use an appropriate PDF validator for a required standard.
- Soft effects, knockout groups, hidden placed-PDF layers or requested flattening can rasterize portions of the output. Reopen and render the exported file, checking page dimensions/count, bleed, color, transparency, text and links.

## Live control and MCP

MCP defaults to an isolated empty Letter document; `--sample` is optional. `--connect` accepts PORT or HOST:PORT and does not silently fall back. The GUI supports `DESIGNCRAFT_CONTROL_PORT`; `app --port 7979 --method document.inspect` calls raw control. Layout coordinates are spread-space points with y down. MCP `inspect_document`/`get_story` expose overset; `render_page` provides visual evidence.

Control is unauthenticated loopback JSON-lines, not HTTP. Enable it only for the task. Invalid/non-request input, lines over 4 MiB, and excess connections are rejected; a malformed request closes that connection (16 concurrent connections maximum). Inspect errors before reconnecting, and never blindly replay a possibly completed mutation. Web builds lack this desktop listener.

## Changes and verification for 0.6.0

The parser rejects page, scale or PDF options placed after the last export. PDF/A image retention and IDML stacking/packaged asset handling improve. Built-in PDF/X-4 validation is available, but its scope does not replace an independent validator when a delivery standard requires one. This review does not include launching the application or executing these new workflows.

## Source links

- [Target-version release and changelog](https://github.com/storytold/designcraft/releases/tag/v0.6.0)
- [CLI parser](https://github.com/storytold/designcraft/blob/v0.6.0/apps/designcraft-cli/src/main.rs)
- [Agent workflow](https://github.com/storytold/designcraft/blob/v0.6.0/docs/agents.md)
- [Data-merge schemas](https://github.com/storytold/designcraft/blob/v0.6.0/crates/engine/src/cmd/datamerge/mod.rs) and [parser limits](https://github.com/storytold/designcraft/blob/v0.6.0/crates/engine/src/cmd/datamerge/parse.rs)
- [Text selection and direction](https://github.com/storytold/designcraft/blob/v0.6.0/crates/engine/src/cmd/text.rs)
- [Preflight](https://github.com/storytold/designcraft/blob/v0.6.0/crates/engine/src/cmd/preflight.rs)
- [CJK boundaries](https://github.com/storytold/designcraft/blob/v0.6.0/docs/cjk-typography.md) and [Arabic boundaries](https://github.com/storytold/designcraft/blob/v0.6.0/docs/arabic-typography.md)
- [File formats](https://github.com/storytold/designcraft/blob/v0.6.0/crates/engine/src/cmd/file.rs), [PDF command](https://github.com/storytold/designcraft/blob/v0.6.0/crates/engine/src/cmd/export.rs), and [PDF exporter](https://github.com/storytold/designcraft/blob/v0.6.0/crates/pdf/src/export.rs)
- [MCP](https://github.com/storytold/designcraft/blob/v0.6.0/docs/mcp.md) and [control protocol](https://github.com/storytold/designcraft/blob/v0.6.0/docs/control-protocol.md)
- [Windows packaging](https://github.com/storytold/designcraft/blob/v0.6.0/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
