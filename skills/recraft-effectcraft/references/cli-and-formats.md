# EffectCraft 0.4.0: CLI and format reference

## Evidence and use

Examples and command notes were checked against upstream tag v0.4.0, commit `f5ebe5f6c5e887dddda4a2be1fcb47154e959b81`. These are source/documentation findings, not a guarantee of behavior on a particular machine. Recheck after upgrading and prefer matching-version documentation over main.

Bare `effectcraft-cli` and `effectcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form where available, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix paths or quoting blindly.

## Supported command examples

```text
effectcraft
effectcraft --control 9877
effectcraft-cli mcp
effectcraft-cli mcp --bridge 9877
effectcraft-cli set Main '#1' transform/position '[100,360]' --time 0 --project main.ecproj --save-as edited.ecproj
effectcraft-cli exec file.exportLottie '{"comp":"Main","path":"main.json"}' main.ecproj
effectcraft-cli commands --filter renderQueue --schemas --json
effectcraft-cli info --project main.ecproj --json
effectcraft-cli props Main '#1' --project main.ecproj --json
effectcraft-cli render-frame --project main.ecproj --comp Main --time 0 --out preview.png
effectcraft-cli render --project main.ecproj --comp Main --out main.mp4
effectcraft-cli exec COMMAND --params JSON --project main.ecproj --save-as edited.ecproj
```

COMMAND, JSON, READ_DIR, WRITE_DIR, and PRIVATE_TOKEN_FILE are grammar placeholders, not ready-to-run values. Discover schemas and fill them deliberately. Demo/sample operations create synthetic content, not a copy of a GUI project.

## Exact grammar and traps

Always pass --project for a real project; without it render uses the demo. exec accepts COMMAND --params JSON or the documented positional COMMAND JSON; run takes COMMAND JSON pairs. --save overwrites the project; prefer --save-as. Time is seconds. Composition refs support IDs/names; layer refs IDs, #n, or names. Full render is headless and rejects --bridge; live rendering uses discovered renderQueue.add/renderQueue.render. CPU is default; --gpu fails if unavailable. Render options include --start/--end, --work-area, --fps, --resolution, --quality, --channels and --audio; inspect exact schema for codecs.

## Live control and MCP

MCP starts empty unless --project or --demo is given. Live MCP uses --bridge PORT or supported address; do not mix bridge with --project/--demo. The v0.4.0 loopback JSON-lines control port has no authentication: enable only when needed, never expose remotely. Lottie is exported via commands/UI, not as a render codec.

Use GUI when it materially helps. Launch the exact GUI executable, inspect its current document, use visible controls/automation IDs that exist, and save explicitly. GUI fallback does not authorize interfering with an unrelated session.

## Source links

- [Target-version release](https://github.com/storytold/effectcraft/releases/tag/v0.4.0)
- [apps/effectcraft-cli/src/main.rs](https://github.com/storytold/effectcraft/blob/v0.4.0/apps/effectcraft-cli/src/main.rs)
- [docs/agents.md](https://github.com/storytold/effectcraft/blob/v0.4.0/docs/agents.md)
- [docs/control-protocol.md](https://github.com/storytold/effectcraft/blob/v0.4.0/docs/control-protocol.md)
- [README.md](https://github.com/storytold/effectcraft/blob/v0.4.0/README.md)
- [packaging/windows/package.ps1](https://github.com/storytold/effectcraft/blob/v0.4.0/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
