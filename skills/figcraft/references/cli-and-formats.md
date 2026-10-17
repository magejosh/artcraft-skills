# FigCraft 0.6.0: CLI and format reference

## Evidence and discovery

Reviewed against official tag v0.6.0, commit `833f0d2c27f0acbae5394848930ae531fc89c724`: packaged README, tagged CLI parser/file implementation, CLI guide and MCP/control documentation. The installed CLI returned 0.6.0, help and the JSON command catalog. Editing, rendering, GUI and prototype behavior remain source-documented, not runtime-tested by this refresh.

Bare `figcraft-cli` below is grammar shorthand: discover it using `FIGCRAFT_CLI` or PATH as described in SKILL.md. Filenames are synthetic; preserve originals and use separate destinations. JSON files avoid shell-specific literal-quote loss. Save scripts as UTF-8 and inspect their contents and every command result.

## Exact CLI examples

```text
figcraft-cli --version
figcraft-cli --help
figcraft-cli commands --json --filter autoLayout
figcraft-cli commands --json --filter component.
figcraft-cli commands --json --filter proto.
figcraft-cli info app.figcraft --json
figcraft-cli run screens.json --out app.figcraft
figcraft-cli run edits.jsonl --in app.figcraft --out edited.figcraft
figcraft-cli render edited.figcraft -o page-review.png --page Screens --scale 1
figcraft-cli export edited.figcraft -o frames/ --page Screens --format png --scale 2
figcraft-cli export edited.figcraft -o home.png --node Home --scale 2
figcraft-cli export edited.figcraft -o screens.pdf --page Screens
figcraft-cli convert imported.svg editable.figcraft
```

- `commands` takes `--filter TEXT`, not a positional filter, and has no separate `describe` command. JSON entries include `id`, `label`, `params`, menu/shortcut and undoable status. `autoLayout` is a documented search example; use `layout.` to find command IDs directly.
- `run SCRIPT.json|SCRIPT.jsonl [--in FILE] [--out FILE]` takes a positional script, not `--script` or repeated `--cmd`. Accepted files are an array of `{command,params}`, an object with `commands`, or JSON lines (blank lines and `//` comments skipped). It prints `{step,command,ok,result}` per successful step. Failure prints `ok:false` and exits 1 before the final `--out` save; explicitly executed save/export commands can already have written files.
- `--out` chooses format by suffix. Preserve `.figcraft` as the editable deliverable; `--out preview.png` alone does not preserve a native design. Bad arguments exit 2, operation failures 1, success 0. Check notes as well as exit status.
- `render` takes `-o/--out`, scale and page name; no `--node`. It renders a whole page with its background, capped to 16384 pixels. For an individual layer use `export --node ID|NAME` (IDs can be `12` or `0:12`). The first page is the default; use exact page names discovered from `info`.
- `export` to a directory emits one file per top-level frame (or top-level layer if no frames). To a supported image filename it composites the page or selected node. Format is explicit `--format`, otherwise the output extension, otherwise PNG. Raster scale defaults to 1 and has a maximum of 64. Inspect output dimensions and file count instead of assuming one output.
- `--no-system-fonts` is accepted globally by every subcommand; `FIGCRAFT_NO_SYSTEM_FONTS=1` is the environment equivalent. Default text layout uses system fonts on demand plus built-ins. Font mode must match the intended review environment.

## Small native design script

For a fresh empty session only, `screens.json` can contain:

```json
[
  {"command":"frame.create","params":{"x":0,"y":0,"width":390,"height":844,"name":"Home","props":{"fill":"#F5F7FA"}}},
  {"command":"node.create","params":{"type":"text","parent":2,"x":24,"y":48,"text":"Welcome","name":"Heading","props":{"fontSize":32,"fill":"#18212B"}}},
  {"command":"frame.create","params":{"x":450,"y":0,"width":390,"height":844,"name":"Details","props":{"fill":"#FFFFFF"}}},
  {"command":"proto.interaction.add","params":{"id":3,"dest":4}},
  {"command":"proto.flow.add","params":{"start":2,"name":"Main flow"}}
]
```

The tagged CLI guide documents page ID 1 and first new layer ID 2, with sequential IDs in a new document. This fixture therefore uses 2/3/4 deliberately; never transplant those IDs into an imported file, template or existing session. Inspect creation results/current document IDs when editing. The first page's name is not set by this script; omit `--page` or discover its name before rendering. Its click-to-navigate interaction is a minimal wiring example, not a claim of tested playback.

## Layout, components and prototypes

Read the relevant installed `commands --json --filter TEXT` entries before applying these schema forms:

```text
layout.add {"ids":[FRAME_ID],"direction":"vertical"}
node.set {"ids":[FRAME_ID],"props":{"layout":"vertical","gap":16,"padding":24,"sizingH":"fixed","sizingV":"hug"}}
component.create {"ids":[FRAME_ID]}
component.combineVariants {"ids":[COMPONENT_ID,OTHER_COMPONENT_ID]}
instance.create {"component":COMPONENT_ID,"parent":FRAME_ID,"x":0,"y":0}
proto.interaction.add {"id":SOURCE_ID,"dest":DESTINATION_FRAME_ID}
proto.flow.add {"start":TOP_LEVEL_FRAME_ID,"name":"Main flow"}
```

Uppercase IDs are placeholders requiring actual numeric IDs. These are engine command/params pairs, not standalone CLI invocations; put them into `{command,params}` script records or call MCP `run_command`.

Coordinates use page units (one unit = one pixel at 100%), x right/y down, relative to the parent frame. Groups/boolean groups do not supply a coordinate space. Flowing children of auto layout are laid out by the engine. `sizingH`/`sizingV` are `fixed|hug|fill`; a child filling a hugged axis changes its parent to fixed, while making the parent hug changes filling children to fixed. `absolute:true` removes a child from flow. Verify the result after resizing. Grid auto layout uses zero-based cell anchors and track sizes such as `[120,"1fr","auto"]`.

`component.create` converts a single frame/group or wraps multiple layers; `component.combineVariants` expects components. Instances can link to a component or a set's default variant. Discover property/override commands before editing an instance, and inspect links after save/reopen. Styles and variables can be linked to text ranges and paints; direct edits may unlink a style. Do not assume changing the main component preserves every deliberate override without inspection.

For prototypes, the short `{id,dest}` form means click-navigation. Full `proto.interaction.add` supports a `trigger`, `action`/`actions`, `transition`, `durationMs`, easing and delay. Query the schema for overlays, back, scrollTo, changeTo and variable/conditional actions. `proto.present`/`proto.preview` are UI requests; one-shot scripts drop dialogs/UI requests, so PNG inspection cannot exercise playback. Use an authorized GUI session to verify flows, hover/press states, overlays, back navigation, scrolling and resizing.

## Native and interchange formats

- `.figcraft` is the native editable archive. JSON can be FigCraft JSON or public REST API file JSON. REST image fills use sibling `images/<imageRef>.<ext>` when present; missing assets become placeholders. Check `info --json` notes and image appearance.
- `.fig` import is best effort. `.fig` export is experimental and is not certified by reopening in another application. Current release notes add variables, styles and instance-size support, while the CLI guide still lists some of those among possible omissions: rely on the actual export notes and inspect interoperability rather than promising complete round-trip fidelity.
- SVG imports editable structures where supported; raster images become image layers. Converting a screenshot to native format does not reconstruct editable UI controls. Native load reports missing images; retain those warnings.
- PNG/JPG/WebP are flattened. SVG/PDF retain supported vector/text content, but shadows/blurs can rasterize and unsupported features can differ. Visible nesting beyond 256 levels makes SVG/PDF export fail; reduce nesting or export an inner node instead of accepting a truncated design.
- PDF without a node exports the page's top-level frames as PDF pages in reading order, with frame sizes interpreted as points. `--bleed LENGTH`, `--crop-marks`, `--bleed-marks`, `--cmyk` are print options. CMYK uses a naive conversion and DeviceCMYK without an output intent; it is not a profiled press-ready guarantee.
- sRGB is the default document profile; Display P3 is supported. SVG/PDF convert P3 to sRGB and out-of-gamut colors clip. The app canvas itself shows sRGB. Verify profile tags and output in an appropriate viewer when wide gamut matters.

## MCP and live control (describe, do not configure implicitly)

`figcraft-cli mcp` starts a stdio MCP server with a headless document and CPU renderer. `figcraft-cli mcp --attach PORT` (also HOST:PORT) attaches to a desktop app started with `figcraft --control PORT`. Do not substitute another app's `--connect`/`--bridge`. One-shot `run` has no collaboration network link; MCP collaboration/plugin-directory calls can transmit data.

Useful MCP tools are `list_commands`, `run_command {command,params}`, `batch {commands,label?}`, `create_node`, `set_properties`, `inspect_document {depth,allPages}`, `get_node {id,depth}`, `select`, `export`, `screenshot`, `open_file` and `save_file`. `screenshot` returns PNG and defaults to a maximum size of 1600; `window:true` requires attached mode for the actual window. `save_file` preserves native `.figcraft`. Get schemas from the matching server before use.

Attached desktop control uses newline-delimited JSON on loopback, not HTTP. A method can specify a window ID; absent one, the last foreground window is targeted. Discover `window.list` and verify its active document before mutation. The channel has 32 MiB request-line limits, eight active connections and 60-second inactivity/response limits. A lost attached reply is ambiguous: the edit may have completed. Inspect state before an explicit retry; the backend does not replay edits automatically.

`batch` is all-or-nothing for open-document state, but not preferences, clipboard, tool state or UI requests; do not assume file/network side effects roll back. Describing MCP or collaboration here does not authorize persistent configuration, publishing plugins, joining remote sessions or opening unrelated documents.

## Pinned sources

- [Target release](https://github.com/storytold/figcraft/releases/tag/v0.6.0)
- [CLI guide](https://github.com/storytold/figcraft/blob/v0.6.0/docs/cli.md)
- [CLI dispatch](https://github.com/storytold/figcraft/blob/v0.6.0/apps/figcraft-cli/src/main.rs)
- [Argument parser](https://github.com/storytold/figcraft/blob/v0.6.0/apps/figcraft-cli/src/args.rs)
- [File/script implementation](https://github.com/storytold/figcraft/blob/v0.6.0/apps/figcraft-cli/src/files.rs)
- [MCP tools, layout, components, prototypes and format notes](https://github.com/storytold/figcraft/blob/v0.6.0/docs/mcp.md)
- [Desktop control and windows](https://github.com/storytold/figcraft/blob/v0.6.0/docs/control-protocol.md)
- [Packaged overview](https://github.com/storytold/figcraft/blob/v0.6.0/README.md)
