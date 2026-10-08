# PrintCraft 0.2.1: CLI and format reference

## Evidence and use

Examples and command notes were checked against upstream tag v0.2.1, commit `dcb00238896e418b357e6dd777ee35bad36f0b97`. These are source/documentation findings, not a guarantee of behavior on a particular machine. Recheck after upgrading and prefer matching-version documentation over main.

Bare `printcraft-cli` and `printcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form where available, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix paths or quoting blindly.

## Supported command examples

```text
printcraft-cli info form.pdf
printcraft-cli text paper.pdf --page 3
printcraft-cli combine report.pdf appendix.pdf --out combined.pdf
printcraft-cli extract report.pdf --pages 1,3,5 --out highlights.pdf
printcraft-cli split report.pdf --every 10 --out-dir parts/
printcraft-cli edit in.pdf --rotate 1,2:90 --delete 5 --title "Q3" --out out.pdf
printcraft-cli tools
printcraft-cli run --script steps.json --root ./work
printcraft-cli mcp --root ./work
printcraft some.pdf
printcraft-cli render paper.pdf --page 3 --dpi 96 --out page.pam
printcraft --control PRIVATE_TOKEN_FILE report.pdf
printcraft-cli ui --control PRIVATE_TOKEN_FILE inspect query=rotate
printcraft-cli ui --control PRIVATE_TOKEN_FILE screenshot --out window.png
```

COMMAND, JSON, READ_DIR, WRITE_DIR, and PRIVATE_TOKEN_FILE are grammar placeholders, not ready-to-run values. Discover schemas and fill them deliberately. Demo/sample operations create synthetic content, not a copy of a GUI project.

## Exact grammar and traps

Direct pages and automation page_render pages are 1-based. Extract/edit lists are comma-separated integers, not 1-3 range strings. Split requires its output directory to exist. Direct render writes PAM RGBA, regardless of filename suffix; use automation page_render for PNG. No rich subcommand help tree. `run --script` reads a JSON ARRAY; each invocation is a new session, so open then query/render/save inside that session. Tool schemas come from `tools`; do not invent parameters. `doc_save` is necessary to persist in-memory changes.

## Live control and MCP

GUI writes chosen random loopback port, token and pid to the control file; CLI reads/authenticates. Do not use mcp --connect, --port, or --control 7979. Never disclose token-file contents; Windows owner-only ACL protection is not verified by the Unix mode-setting source. Repository renamed to pdfcraft; v0.2.1 executables remain printcraft. OCR model lookup: PRINTCRAFT_MODELS, models beside EXE, then other resource/source locations; verify both RTEN files before OCR.

Use GUI when it materially helps. Launch the exact GUI executable, inspect its current document, use visible controls/automation IDs that exist, and save explicitly. GUI fallback does not authorize interfering with an unrelated session.

## Complete fresh-session script

```json
[
  {"tool":"doc_open","args":{"path":"report.pdf"}},
  {"tool":"page_render","args":{"doc":1,"page":1,"dpi":144},"out":"preview.png"},
  {"tool":"text_find","args":{"doc":1,"query":"invoice"}}
]
```

Save this array as steps.json under the authorized root and invoke the documented run command. Document ID 1 applies only to this fresh session; use returned IDs in ongoing MCP sessions.

## OCR on a copy

First inspect `printcraft-cli run ocr_status`; it is read-only and reports models/languages. If models are unavailable, stop OCR and obtain any required download/install approval; do not run the source-build `cargo xtask models` command against a portable-only folder.

When models are available, use one fresh run-script session and a distinct output path:

```json
[
  {"tool":"doc_open","args":{"path":"scan.pdf"}},
  {"tool":"ocr_recognize","args":{"doc":1,"pages":[1],"dpi":300,"language":"en","skip_text_pages":true}},
  {"tool":"doc_save","args":{"doc":1,"path":"scan-searchable.pdf"}}
]
```

Omit pages only when all pages are intended; dpi is 72–600 and the supported language is en. OCR adds invisible searchable text without changing the page image. Reopen the saved result, extract and compare recognized text to the scan, and inspect layout. Do not assume OCR accuracy or silently overwrite a signed document.

## Source links

- [Target-version release](https://github.com/storytold/pdfcraft/releases/tag/v0.2.1)
- [apps/printcraft-cli/src/main.rs](https://github.com/storytold/pdfcraft/blob/v0.2.1/apps/printcraft-cli/src/main.rs)
- [crates/automation/src/tools.rs](https://github.com/storytold/pdfcraft/blob/v0.2.1/crates/automation/src/tools.rs)
- [crates/automation/src/lib.rs](https://github.com/storytold/pdfcraft/blob/v0.2.1/crates/automation/src/lib.rs)
- [apps/printcraft/src/main.rs](https://github.com/storytold/pdfcraft/blob/v0.2.1/apps/printcraft/src/main.rs)
- [crates/ocr/src/lib.rs](https://github.com/storytold/pdfcraft/blob/v0.2.1/crates/ocr/src/lib.rs)
- [packaging/windows/package.ps1](https://github.com/storytold/pdfcraft/blob/v0.2.1/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
