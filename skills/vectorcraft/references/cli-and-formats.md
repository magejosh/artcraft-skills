# VectorCraft 0.4.0: CLI and format reference

## Evidence and use

Examples and command notes were checked against upstream tag v0.4.0, commit `a26aa5b203c901979eb447d28e34e7357138c789`. These are source/documentation findings, not a guarantee of behavior on a particular machine. Recheck after upgrading and prefer matching-version documentation over main.

Bare `vectorcraft-cli` and `vectorcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form where available, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix paths or quoting blindly.

## Supported command examples

```text
vectorcraft
vectorcraft --control 7979
vectorcraft-cli run --in drawing.vectorcraft --export out.pdf
vectorcraft-cli mcp --headless
vectorcraft-cli mcp --connect 127.0.0.1:7979
vectorcraft-cli commands
vectorcraft-cli info artwork.vectorcraft
vectorcraft-cli run --in artwork.vectorcraft --export artwork.svg --export artwork.pdf
vectorcraft-cli run --cmd file.new --params '{"colorMode":"cmyk"}' --export blank.vectorcraft
vectorcraft-cli convert artwork.vectorcraft artwork.png --scale 2 --artboard 0
vectorcraft-cli convert artwork.vectorcraft selected.pdf --range 1-3,5
```

COMMAND, JSON, READ_DIR, WRITE_DIR, and PRIVATE_TOKEN_FILE are grammar placeholders, not ready-to-run values. Discover schemas and fill them deliberately. Demo/sample operations create synthetic content, not a copy of a GUI project.

## Exact grammar and traps

`run` accepts --in/-i, --cmd/-c ID immediately followed by --params/-p JSON object, repeated --export/-o, --scale/-s. No run --save, --sample, --script, --connect, --artboard, --range. `convert` supports --scale, --artboard zero-based, --range one-based, --outline-text. PDF defaults to all artboards; most formats default first; EPS uses art bounds. Commands has no filter; no CLI describe/app. run emits JSON per step; read each result and format-loss warning.

## Live control and MCP

Always choose explicit mcp --headless or mcp --connect HOST:PORT (mutually exclusive). Bare mcp attempts live 7979 and silently falls back headless, which can target the wrong document. Loopback control has no authentication; enable only when needed. GUI supports VECTORCRAFT_CONTROL_PORT and has no --sample. `%APPDATA%\VectorCraft` stores preferences. Inspect engine document.formats and returned loss warnings.

Use GUI when it materially helps. Launch the exact GUI executable, inspect its current document, use visible controls/automation IDs that exist, and save explicitly. GUI fallback does not authorize interfering with an unrelated session.

## Source links

- [Target-version release](https://github.com/storytold/vectorcraft/releases/tag/v0.4.0)
- [apps/vectorcraft-cli/src/main.rs](https://github.com/storytold/vectorcraft/blob/v0.4.0/apps/vectorcraft-cli/src/main.rs)
- [crates/engine/src/cmd/fileio/mod.rs](https://github.com/storytold/vectorcraft/blob/v0.4.0/crates/engine/src/cmd/fileio/mod.rs)
- [docs/mcp.md](https://github.com/storytold/vectorcraft/blob/v0.4.0/docs/mcp.md)
- [docs/control-protocol.md](https://github.com/storytold/vectorcraft/blob/v0.4.0/docs/control-protocol.md)
- [packaging/windows/package.ps1](https://github.com/storytold/vectorcraft/blob/v0.4.0/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
