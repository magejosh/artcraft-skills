# DeckCraft 0.3.0: CLI and format reference

## Evidence and use

Examples and command notes were checked against upstream tag v0.3.0, commit `d0e57d7e25f9852179cc66be12dd6188f1c05535`. These are source/documentation findings, not a guarantee of behavior on a particular machine. Recheck after upgrading and prefer matching-version documentation over main.

Bare `deckcraft-cli` and `deckcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form where available, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix paths or quoting blindly.

## Supported command examples

```text
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

`run` uses --in, --sample, repeated --cmd ID[=JSON], --save, --export, --print. --print prints results, not to a physical printer. `describe COMMAND` supplies the schema. Render --slide is zero-based; --all makes slide-01.png etc. `render` always writes PNG bytes even when a path ends .jpg; use convert/file.export for JPEG. Use file.export's schema for PDF notes/handouts parameters, not invented CLI flags. Coordinates use slide points (1/72 inch). Convert to .jpg/.jpeg exports slide 0 as real JPEG; file.export also accepts format=jpeg, slide (zero-based), and scale. JPEG quality is fixed at 92; scale defaults to 2 pixels/point and is clamped 0.01–16.

## Live control and MCP

MCP is headless by default; --connect accepts PORT or HOST:PORT. For raw control methods use `deckcraft-cli app --port 7990 --method document.inspect`; otherwise app expects COMMAND [JSON]. DECKCRAFT_CONTROL_PORT is supported. GUI preferences may be written to %APPDATA%\DeckCraft.

Use GUI when it materially helps. Launch the exact GUI executable, inspect its current document, use visible controls/automation IDs that exist, and save explicitly. GUI fallback does not authorize interfering with an unrelated session.

## Source links

- [Target-version release](https://github.com/storytold/deckcraft/releases/tag/v0.3.0)
- [apps/deckcraft-cli/src/main.rs](https://github.com/storytold/deckcraft/blob/v0.3.0/apps/deckcraft-cli/src/main.rs)
- [crates/engine/src/cmd/file.rs](https://github.com/storytold/deckcraft/blob/v0.3.0/crates/engine/src/cmd/file.rs)
- [docs/mcp.md](https://github.com/storytold/deckcraft/blob/v0.3.0/docs/mcp.md)
- [docs/control-protocol.md](https://github.com/storytold/deckcraft/blob/v0.3.0/docs/control-protocol.md)
- [packaging/windows/package.ps1](https://github.com/storytold/deckcraft/blob/v0.3.0/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
