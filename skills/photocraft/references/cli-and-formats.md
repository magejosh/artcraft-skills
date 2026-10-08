# PhotoCraft 0.3.0: CLI and format reference

## Evidence and use

Examples and command notes were checked against upstream tag v0.3.0, commit `60224d3fb7d4006bcfcc97603c1611b9b756aebd`. These are source/documentation findings, not a guarantee of behavior on a particular machine. Recheck after upgrading and prefer matching-version documentation over main.

Bare `photocraft-cli` and `photocraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form where available, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix paths or quoting blindly.

## Supported command examples

```text
photocraft image.psd
photocraft --control
photocraft-cli run wave.psd --cmd filter.sharpen.smartSharpen --params '{"amount":80}' --cmd layer.newAdjustmentLayer.curves --params '{"points":[[0,0],[64,48],[192,212],[255,255]]}' --out wave-final.png
photocraft-cli batch --help
photocraft-cli batch --actions grade.json --in ./raw --out ./graded
photocraft-cli mcp
photocraft-cli info input.psd --compact
photocraft-cli convert input.psd output.jpg --quality 90
photocraft-cli commands --json --filter sharpen
photocraft-cli mcp --automation-read-root READ_DIR --automation-write-root WRITE_DIR
photocraft --control 7878 --control-token-file PRIVATE_TOKEN_FILE --automation-read-root READ_DIR --automation-write-root WRITE_DIR
photocraft-cli mcp --bridge 127.0.0.1:7878 --control-token-file PRIVATE_TOKEN_FILE
```

COMMAND, JSON, READ_DIR, WRITE_DIR, and PRIVATE_TOKEN_FILE are grammar placeholders, not ready-to-run values. Discover schemas and fill them deliberately. Demo/sample operations create synthetic content, not a copy of a GUI project.

## Exact grammar and traps

`run` takes exactly one file or --new JSON. Each --params belongs immediately after the preceding --cmd; without --out, normal edits are not saved. Batch actions accept [id,params] pairs, {command,params} objects, or IDs (possibly wrapped in actions/steps/droplet). Batch keeps each input extension by default; --format psd requests PSD output. It processes all recognized image files in the input directory, so use a PSD-only staging folder when only PSDs are intended. Separate output is the safe default; same-directory output requires --in-place. Inspect and validate action JSON before use. Ordinary CLI run/convert/batch uses normal OS paths and is not confined by MCP roots.

## Live control and MCP

Headless MCP has only explicit read/write roots: missing root means no corresponding file permission. Bridge inherits desktop roots, takes relative paths, and rejects absolute paths/escapes. Desktop control is token-authenticated; absent token file is created, existing one reused. Keep token values out of chat, logs, args, and skills. Verify appropriate user-only file protection on Windows through authorized means; do not silently alter ACLs. Starting/configuring ongoing roots or credentials needs the appropriate authorization. Prefer one-shot CLI when it suffices.

Use GUI when it materially helps. Launch the exact GUI executable, inspect its current document, use visible controls/automation IDs that exist, and save explicitly. GUI fallback does not authorize interfering with an unrelated session.

## Source links

- [Target-version release](https://github.com/storytold/photocraft/releases/tag/v0.3.0)
- [apps/photocraft-cli/src/lib.rs](https://github.com/storytold/photocraft/blob/v0.3.0/apps/photocraft-cli/src/lib.rs)
- [book/src/automation/cli.md](https://github.com/storytold/photocraft/blob/v0.3.0/book/src/automation/cli.md)
- [book/src/automation/mcp.md](https://github.com/storytold/photocraft/blob/v0.3.0/book/src/automation/mcp.md)
- [docs/control-protocol.md](https://github.com/storytold/photocraft/blob/v0.3.0/docs/control-protocol.md)
- [README.md](https://github.com/storytold/photocraft/blob/v0.3.0/README.md)
- [packaging/windows/package.ps1](https://github.com/storytold/photocraft/blob/v0.3.0/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
