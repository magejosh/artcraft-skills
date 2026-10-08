# FilmCraft 0.2.1: CLI and format reference

## Evidence and use

Examples and command notes were checked against upstream tag v0.2.1, commit `61ab6f5c7dfc37097b8a28aac235a3e31a84a6ae`. These are source/documentation findings, not a guarantee of behavior on a particular machine. Recheck after upgrading and prefer matching-version documentation over main.

Bare `filmcraft-cli` and `filmcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form where available, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix paths or quoting blindly.

## Supported command examples

```text
filmcraft
filmcraft --control 9876
filmcraft-cli commands
filmcraft-cli mcp
filmcraft-cli help
filmcraft-cli describe timeline.razor
filmcraft-cli --project edit.fcproj inspect sequence
filmcraft-cli --project edit.fcproj export out.mp4
filmcraft-cli --project edit.fcproj export out --preset "YouTube 1080p Full HD" --start 0 --end 10
filmcraft-cli export --list-presets prores
filmcraft-cli --project edit.fcproj render --seconds 2 --out frame.png --scale 0.5
filmcraft-cli --project edit.fcproj --save-as edited.fcproj run script.jsonl
filmcraft-cli mcp --bridge 127.0.0.1:9876
```

COMMAND, JSON, READ_DIR, WRITE_DIR, and PRIVATE_TOKEN_FILE are grammar placeholders, not ready-to-run values. Discover schemas and fill them deliberately. Demo/sample operations create synthetic content, not a copy of a GUI project.

## Exact grammar and traps

Use top-level `help`, not assumed subcommand --help. Global --project chooses the project; --save writes back, --save-as preserves the source. Parameters are a JSON object or key=value pairs; dotted keys nest. `run script.jsonl` expects one {"id":"COMMAND","params":{...}} per line; - reads stdin. `export` waits for completion and supports presets, formats, --range entire|inOut|workArea, paired --start/--end seconds, --settings JSON, and --queue. `render` produces one headless PNG frame, not a movie. Exit 0 success/1 command failure/2 usage; inspect per-line errors with --keep-going.

## Live control and MCP

Live mode uses --bridge, not --connect. Bridge and --project/--demo are mutually exclusive; headless frame render rejects bridge. Verify target session before mutation. Export formats include h264/prores/dnxhr/mjpeg/mxf-op1a/mxf-opatom and still/audio types; .mp4 maps h264, .mov prores, .mxf mxf-op1a. HEVC/AV1 import is not evidence of export support.

Use GUI when it materially helps. Launch the exact GUI executable, inspect its current document, use visible controls/automation IDs that exist, and save explicitly. GUI fallback does not authorize interfering with an unrelated session.

## Source links

- [Target-version release](https://github.com/storytold/filmcraft/releases/tag/v0.2.1)
- [apps/filmcraft-cli/src/main.rs](https://github.com/storytold/filmcraft/blob/v0.2.1/apps/filmcraft-cli/src/main.rs)
- [apps/filmcraft-cli/src/args.rs](https://github.com/storytold/filmcraft/blob/v0.2.1/apps/filmcraft-cli/src/args.rs)
- [docs/agents.md](https://github.com/storytold/filmcraft/blob/v0.2.1/docs/agents.md)
- [docs/control-protocol.md](https://github.com/storytold/filmcraft/blob/v0.2.1/docs/control-protocol.md)
- [README.md](https://github.com/storytold/filmcraft/blob/v0.2.1/README.md)
- [packaging/windows/package.ps1](https://github.com/storytold/filmcraft/blob/v0.2.1/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
