# SoundCraft 0.3.0: CLI and format reference

## Evidence and use

Examples and command notes were checked against upstream tag v0.3.0, commit `c51e5d5ec52f11c6264b72e26661fa712feb5345`. These are source/documentation findings, not a guarantee of behavior on a particular machine. Recheck after upgrading and prefer matching-version documentation over main.

Bare `soundcraft-cli` and `soundcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form where available, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix paths or quoting blindly.

## Supported command examples

```text
soundcraft --demo
soundcraft-cli commands
soundcraft-cli run --demo --cmd 'mix.volume={"track":"Kick","db":-6}' --cmd 'mix.insert={"track":"Bass","plugin":"eq_7band"}' --bounce mix.wav
soundcraft --demo --control 7801
soundcraft-cli app --port 7801 transport.play
soundcraft-cli app --port 7801 ui.screenshot '{"path":"shot.png"}'
soundcraft-cli mcp --demo
soundcraft-cli info session.scraft
soundcraft-cli plugins
soundcraft-cli describe mix.volume
soundcraft-cli run --in session.scraft --cmd 'mix.volume={"track":"Kick","db":-6}' --bounce mix.wav --save edited.scraft --inspect
soundcraft-cli script edits.txt --in session.scraft --save edited.scraft --bounce mix.wav
soundcraft-cli mcp --connect 7801
```

COMMAND, JSON, READ_DIR, WRITE_DIR, and PRIVATE_TOKEN_FILE are grammar placeholders, not ready-to-run values. Discover schemas and fill them deliberately. Demo/sample operations create synthetic content, not a copy of a GUI project.

## Exact grammar and traps

`run` takes --in, repeated --cmd ID=JSON, --save, --bounce, --inspect. Scripts contain COMMAND_ID followed by JSON per line; blanks and # comments are skipped, and malformed JSON fails. Validate JSON before run/app because malformed JSON can silently become {}. run --start/--end accept numeric seconds or time strings; engine time may use samples, {seconds:2.5}, or prefixed bars_beats. Use inspected track names/IDs and clip IDs. Top-level --help works; general subcommand --help does not.

## Live control and MCP

Live MCP uses --connect, not --bridge. Explicitly set app --port 7801: parser default is 7979. Bare app IDs map to engine.execute, except session.* are treated as raw methods; use explicit engine.execute for ambiguity. Headless MCP needs no window/audio device. Keep session media in Audio Files/ with the .scraft project.

Use GUI when it materially helps. Launch the exact GUI executable, inspect its current document, use visible controls/automation IDs that exist, and save explicitly. GUI fallback does not authorize interfering with an unrelated session.

## Source links

- [Target-version release](https://github.com/storytold/soundcraft/releases/tag/v0.3.0)
- [apps/soundcraft-cli/src/main.rs](https://github.com/storytold/soundcraft/blob/v0.3.0/apps/soundcraft-cli/src/main.rs)
- [apps/soundcraft/src/main.rs](https://github.com/storytold/soundcraft/blob/v0.3.0/apps/soundcraft/src/main.rs)
- [docs/mcp.md](https://github.com/storytold/soundcraft/blob/v0.3.0/docs/mcp.md)
- [docs/control-protocol.md](https://github.com/storytold/soundcraft/blob/v0.3.0/docs/control-protocol.md)
- [README.md](https://github.com/storytold/soundcraft/blob/v0.3.0/README.md)
- [packaging/windows/package.ps1](https://github.com/storytold/soundcraft/blob/v0.3.0/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
