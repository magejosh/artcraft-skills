# DesignCraft 0.2.1: CLI and format reference

## Evidence and use

Examples and command notes were checked against upstream tag v0.2.1, commit `80b3e3cb74618b02f40b80ac7c2fa35e5da4e1af`. These are source/documentation findings, not a guarantee of behavior on a particular machine. Recheck after upgrading and prefer matching-version documentation over main.

Bare `designcraft-cli` and `designcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form where available, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix paths or quoting blindly.

## Supported command examples

```text
designcraft
designcraft --sample
designcraft --sample --control 7979
designcraft-cli run --sample --all-pages out/
designcraft-cli commands
designcraft-cli describe frame.create
designcraft-cli run --in document.idml --page 0 --scale 2 --export first.png
designcraft-cli run --sample --export sample.designcraft --export sample.pdf
designcraft-cli run --sample --export sample.epub
designcraft-cli script page.dcs --save page.designcraft --export page.pdf
designcraft-cli mcp
designcraft-cli mcp --connect 7979
```

COMMAND, JSON, READ_DIR, WRITE_DIR, and PRIVATE_TOKEN_FILE are grammar placeholders, not ready-to-run values. Discover schemas and fill them deliberately. Demo/sample operations create synthetic content, not a copy of a GUI project.

## Exact grammar and traps

`run` accepts --in, --sample, --cmd ID[=JSON], --page, --scale, --pdf-options JSON, --export, --all-pages. No run --save: use --export output.designcraft. Options execute sequentially: open/create, edit, configure render options, then export. Page indices are zero-based, but placed-PDF pdfPage is one-based. Separate `script FILE|-` accepts --in/--sample, --connect, --save, repeated --export and --keep-going. Scripts support command-per-line, JSONL, or arrays of {command,params}; earlier result references $0.story/$last and ${0.id}. Check each result when --keep-going is used. Use lowercase suffixes.

## Live control and MCP

MCP defaults to an isolated empty Letter document; --sample is optional. --connect accepts PORT or HOST:PORT with no silent fallback. GUI/control supports DESIGNCRAFT_CONTROL_PORT. `app --port 7979 --method document.inspect` uses raw control. Layout positions are spread-space points, y down. Inspect_document/get_story expose overset; render_page supplies visual evidence.

Use GUI when it materially helps. Launch the exact GUI executable, inspect its current document, use visible controls/automation IDs that exist, and save explicitly. GUI fallback does not authorize interfering with an unrelated session.

## Source links

- [Target-version release](https://github.com/storytold/designcraft/releases/tag/v0.2.1)
- [apps/designcraft-cli/src/main.rs](https://github.com/storytold/designcraft/blob/v0.2.1/apps/designcraft-cli/src/main.rs)
- [crates/engine/src/cmd/file.rs](https://github.com/storytold/designcraft/blob/v0.2.1/crates/engine/src/cmd/file.rs)
- [docs/agents.md](https://github.com/storytold/designcraft/blob/v0.2.1/docs/agents.md)
- [docs/mcp.md](https://github.com/storytold/designcraft/blob/v0.2.1/docs/mcp.md)
- [docs/control-protocol.md](https://github.com/storytold/designcraft/blob/v0.2.1/docs/control-protocol.md)
- [packaging/windows/package.ps1](https://github.com/storytold/designcraft/blob/v0.2.1/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
