# LightCraft 0.2.1: CLI and format reference

## Evidence and use

Examples and command notes were checked against upstream tag v0.2.1, commit `fc3fa1a71b67b3bb2aeccbf0b164bd9543288b9f`. These are source/documentation findings, not a guarantee of behavior on a particular machine. Recheck after upgrading and prefer matching-version documentation over main.

Bare `lightcraft-cli` and `lightcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form where available, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix paths or quoting blindly.

## Supported command examples

```text
lightcraft --memory
lightcraft --control 7980
lightcraft-cli mcp --connect 127.0.0.1:7980
lightcraft-cli run --import in.dng develop.set control=light.exposure value=0.7 app.export path=out.jpg longEdge=2048
lightcraft-cli render photo.jpg -o out.jpg --set light.exposure=0.5
lightcraft-cli controls --json
lightcraft-cli commands --json
lightcraft-cli run presets.list
lightcraft-cli render in.dng -o out.jpg --preset lc.golden-hour --size 2048
lightcraft-cli render in.dng -o out.tif --opt colorSpace=displayP3 --opt bitDepth=16 --opt percent=50
lightcraft-cli run --library library-dir --script steps.jsonl
lightcraft-cli run --connect 127.0.0.1:7980 ui.inspect
```

COMMAND, JSON, READ_DIR, WRITE_DIR, and PRIVATE_TOKEN_FILE are grammar placeholders, not ready-to-run values. Discover schemas and fill them deliberately. Demo/sample operations create synthetic content, not a copy of a GUI project.

## Exact grammar and traps

`render INPUT -o OUTPUT` accepts repeated --set CONTROL=NUMBER, --settings FILE, --preset ID, --size N, --quality Q, --opt KEY=VALUE. Processing order is preset → settings JSON → individual --set regardless of argument order. Preset IDs are lc.golden-hour/lc.teal-orange/lc.crisp-landscape/lc.bw-selenium; discover current IDs with `run presets.list`. Set the intended size explicitly; do not rely on an old documented 3000px default. `run` supports --demo/--library, repeated --import, --connect, --script FILE|-, --keep-going. Tokens without = begin a command; key=value parses JSON or string. JSONL accepts {command,params} or {method,params}; inspect each ok/error record.

## Live control and MCP

Use full HOST:PORT for explicit --connect; the separated optional address requires a colon. --connect alone defaults 127.0.0.1:7980. Never open a persistent library in another headless process while the GUI owns it; connect to that app. Control has no authentication. --memory is throwaway; persistent --library saves edits. Render protects imported originals/sidecars against overwrite.

Use GUI when it materially helps. Launch the exact GUI executable, inspect its current document, use visible controls/automation IDs that exist, and save explicitly. GUI fallback does not authorize interfering with an unrelated session.

## Source links

- [Target-version release](https://github.com/storytold/lightcraft/releases/tag/v0.2.1)
- [apps/lightcraft-cli/src/main.rs](https://github.com/storytold/lightcraft/blob/v0.2.1/apps/lightcraft-cli/src/main.rs)
- [crates/engine/src/presets.rs](https://github.com/storytold/lightcraft/blob/v0.2.1/crates/engine/src/presets.rs)
- [crates/engine/src/export.rs](https://github.com/storytold/lightcraft/blob/v0.2.1/crates/engine/src/export.rs)
- [docs/mcp.md](https://github.com/storytold/lightcraft/blob/v0.2.1/docs/mcp.md)
- [docs/control-protocol.md](https://github.com/storytold/lightcraft/blob/v0.2.1/docs/control-protocol.md)
- [crates/codecs/src/lib.rs](https://github.com/storytold/lightcraft/blob/v0.2.1/crates/codecs/src/lib.rs)
- [packaging/windows/package.ps1](https://github.com/storytold/lightcraft/blob/v0.2.1/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
