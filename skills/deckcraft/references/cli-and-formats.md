# DeckCraft 0.7.0: CLI and format reference

## Evidence and use

Examples and command notes were checked against upstream tag v0.7.0, commit `d78e657e4cb1e490ceb5445785c052d9cf5ad963`. These are source/documentation findings, not a guarantee of behavior on a particular machine. Recheck after upgrading and prefer matching-version documentation over main.

Bare `deckcraft-cli` and `deckcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form where available, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix paths or quoting blindly.

## Supported command examples

```text
deckcraft-cli render-transition deck.pptx --slide 1 --t 0,0.5,1 --width 800 transition.png
deckcraft-cli render --sample --all --scale 1 out/
deckcraft-cli commands format.
deckcraft-cli run --sample --cmd 'slide.new={"layout":"titleOnly","title":"Hello"}' --save hello.deckcraft
deckcraft-cli mcp
deckcraft --control 7990
deckcraft-cli mcp --connect 7990
deckcraft-cli describe slide.new
deckcraft-cli info deck.pptx
deckcraft-cli render deck.pptx --slide 0 --scale 2 first.png
deckcraft-cli convert input.deckcraft output.pptx
deckcraft-cli convert input.pptx first.jpg
deckcraft-cli run --in input.pptx --cmd 'file.export={"path":"first.jpg","format":"jpeg","slide":0,"scale":2}' --print
deckcraft-cli run --in hello.deckcraft --export hello.pdf
```

COMMAND, JSON, READ_DIR, WRITE_DIR, and PRIVATE_TOKEN_FILE are grammar placeholders, not ready-to-run values. Discover schemas and fill them deliberately. Demo/sample operations create synthetic content, not a copy of a GUI project.

## Exact grammar and traps

`run` uses --in, --sample, repeated --cmd ID[=JSON], --save, --export, --print. --print prints results, not to a physical printer. `describe COMMAND` supplies the schema. Render --slide is zero-based; --all makes slide-01.png etc. `render` always writes PNG bytes even when a path ends .jpg; use convert/file.export for JPEG. Use file.export's schema for PDF notes/handouts parameters, not invented CLI flags. `render --edit` includes editor placeholder prompts and dashed outlines; omit it for a presentation-output preview. Coordinates use slide points (1/72 inch). Convert to .jpg/.jpeg exports slide 0 as real JPEG; file.export also accepts format=jpeg, slide (zero-based), and scale. JPEG quality is fixed at 92; scale defaults to 2 pixels/point and is clamped 0.01–16.

## Live control and MCP

MCP is headless by default; --connect accepts PORT or HOST:PORT. For raw control methods use `deckcraft-cli app --port 7990 --method document.inspect`; otherwise app expects COMMAND [JSON]. DECKCRAFT_CONTROL_PORT is supported. GUI preferences may be written to %APPDATA%\DeckCraft.

Use GUI when it materially helps. Launch the exact GUI executable, inspect its current document, use visible controls/automation IDs that exist, and save explicitly. GUI fallback does not authorize interfering with an unrelated session.

## Changes and verification for 0.7.0

The CLI adds render-transition FILE --slide N --t T[,T...] [--width PX] OUT.png. N is zero-based, transitioning from N-1 (black before slide 0); progress values must be in 0..1. Multiple values create separate suffixed PNGs. Use these frames to inspect transition geometry, then review actual playback for timing. Shape effects, gradients, grouped text and chart rendering have changed; compare the exported slides with the intended presentation.

These are matching-tag source/documentation findings. The installed CLI version was checked; these editing/export workflows were not executed for this refresh.

## Previously documented behavior and verification

Morph now includes shape movement, resizing and blending plus Words/Characters text modes. Arabic/BiDi typography and table fitting/PDF text improve. Check slide-show playback, table overflow and exported searchable text with the actual fonts; a static slide render cannot certify a transition. This review does not include launching the application or executing these new workflows.

This release also morphs changed shape outlines, corrects old/new slide transition display, exposes PDF notes/handout options through MCP export, and supports animated GIF playback with pause. Confirm the export tool schema, hyperlink behavior and complete slide-show playback; animation is not established by a static PNG. These additional release findings have not been execution-tested.

## Source links

- [Editor-view rendering](https://github.com/storytold/deckcraft/blob/v0.7.0/crates/render/src/lib.rs)
- [Target-version release](https://github.com/storytold/deckcraft/releases/tag/v0.7.0)
- [apps/deckcraft-cli/src/main.rs](https://github.com/storytold/deckcraft/blob/v0.7.0/apps/deckcraft-cli/src/main.rs)
- [crates/engine/src/cmd/file.rs](https://github.com/storytold/deckcraft/blob/v0.7.0/crates/engine/src/cmd/file.rs)
- [docs/mcp.md](https://github.com/storytold/deckcraft/blob/v0.7.0/docs/mcp.md)
- [docs/control-protocol.md](https://github.com/storytold/deckcraft/blob/v0.7.0/docs/control-protocol.md)
- [packaging/windows/package.ps1](https://github.com/storytold/deckcraft/blob/v0.7.0/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
