# CADCraft 0.3.0: CLI and format reference

## Evidence and use

Examples and command notes were checked against upstream tag v0.3.0, commit `59631c8d4f9ffe6c08c5c2065ea17504e53bf821`. These are source/documentation findings, not a guarantee of behavior on a particular machine. Recheck after upgrading and prefer matching-version documentation over main.

Bare `cadcraft-cli` and `cadcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form where available, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix paths or quoting blindly.

## Supported command examples

```text
cadcraft-cli info drawing.dxf
cadcraft-cli convert drawing.dxf drawing.svg
cadcraft-cli run --sample --script 'CIRCLE 22,3 1\n' --save out.dxf
cadcraft-cli convert out.dxf out.png
cadcraft-cli commands
cadcraft --sample
cadcraft --control 7979
cadcraft-cli mcp
cadcraft-cli mcp --connect 127.0.0.1:7979
cadcraft-cli run drawing.dxf --script-file edits.scr --save edited.dxf
cadcraft-cli run --metric --cmd 'circle {"center":[10,10],"radius":4}' --save circle.dxf
```

COMMAND, JSON, READ_DIR, WRITE_DIR, and PRIVATE_TOKEN_FILE are grammar placeholders, not ready-to-run values. Discover schemas and fill them deliberately. Demo/sample operations create synthetic content, not a copy of a GUI project.

## Exact grammar and traps

`run` takes a positional input, not --in. Its --cmd takes one argument `id {json}`, split at the first space, not ID=JSON; there is no --params. --script expands literal \\n; --script-file reads UTF-8. Supported flags: --sample, --metric, --script, --script-file, --cmd, --save, --export. Save/export share one extension-selected output slot, so repeated flags keep only the last output. PNG conversion defaults to 2400×1600 and fitted model extents; do not invent run --scale/--page/--all-pages. Commands supports a positional filter; no describe/app subcommand.

## Live control and MCP

MCP is headless by default. --connect requires HOST:PORT for a live app. Control is newline-delimited JSON on loopback, not HTTP. Verify the app/session on the port before mutation. GUI accepts --control PORT; CADCRAFT_CONTROL_PORT is also supported.

Use GUI when it materially helps. Launch the exact GUI executable, inspect its current document, use visible controls/automation IDs that exist, and save explicitly. GUI fallback does not authorize interfering with an unrelated session.

## Source links

- [Target-version release](https://github.com/storytold/cadcraft/releases/tag/v0.3.0)
- [apps/cadcraft-cli/src/main.rs](https://github.com/storytold/cadcraft/blob/v0.3.0/apps/cadcraft-cli/src/main.rs)
- [crates/io/src/lib.rs](https://github.com/storytold/cadcraft/blob/v0.3.0/crates/io/src/lib.rs)
- [docs/mcp.md](https://github.com/storytold/cadcraft/blob/v0.3.0/docs/mcp.md)
- [docs/control-protocol.md](https://github.com/storytold/cadcraft/blob/v0.3.0/docs/control-protocol.md)
- [packaging/windows/package.ps1](https://github.com/storytold/cadcraft/blob/v0.3.0/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
