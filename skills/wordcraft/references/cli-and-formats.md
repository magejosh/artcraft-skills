# WordCraft 0.6.1: CLI and format reference

## Evidence and use

Examples and command notes were checked against upstream tag v0.6.1, commit `7dfa6b0ee2aeeafec004c51fdd2ab9a697da3cc4`. These are source/documentation findings, not a guarantee of behavior on a particular machine. Recheck after upgrading and prefer matching-version documentation over main.

Bare `wordcraft-cli` and `wordcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form where available, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix paths or quoting blindly.

## Supported command examples

```text
wordcraft --sample
wordcraft report.docx
wordcraft-cli convert report.docx report.pdf
wordcraft-cli text report.docx
wordcraft-cli inspect report.docx
wordcraft-cli run --template sample --cmd 'select.text={"text":"Membership"}' --cmd format.bold --save out.docx
wordcraft-cli mcp
wordcraft --control 7981
wordcraft-cli mcp --connect 127.0.0.1:7981
wordcraft-cli info report.docx
wordcraft-cli render report.docx page.png --page 2 --scale 2
wordcraft-cli commands --json
wordcraft-cli run --file report.docx --cmd 'select.text={"text":"Membership"}' --cmd format.bold --save edited.docx --print
```

COMMAND, JSON, READ_DIR, WRITE_DIR, and PRIVATE_TOKEN_FILE are grammar placeholders, not ready-to-run values. Discover schemas and fill them deliberately. Demo/sample operations create synthetic content, not a copy of a GUI project.

## Exact grammar and traps

`run` uses --file or --template, repeated --cmd ID[=JSON], --save, --print. It does not use --in/--out or implement run --script. --print emits command results, not physical print. `render` page is 1-based; control ui.clickText page is zero-based. Convert to PNG emits page 1 only; choose render --page for another page. PDF is not input. The updated save path preserves DOCM macros/signatures and DOCM/DOTX/DOTM content types. Verify retained package parts and signature status; preservation is not permission to execute macros. LaTeX .tex import/export is available. Legacy binary .doc/.dot import supports text, formatting, sections and some pictures/shapes; inspect pagination, lists and image placement for partial fidelity. Mail-merge recipient input includes XLSX/XLSM/ODS; verify NEXT/SKIPIF/IF preview results and header/footer fields before saving the merged copy.

## Live control and MCP

MCP --connect HOST:PORT selects live mode. CLI run itself has no --connect. Headless tools include open/save, type/select text, inspect_document, render_page, execute and batch; screenshot/click/key/ui_inspect require live mode. Preserve review metadata and verify pagination on copies.

Use GUI when it materially helps. Launch the exact GUI executable, inspect its current document, use visible controls/automation IDs that exist, and save explicitly. GUI fallback does not authorize interfering with an unrelated session.

## Changes and verification for 0.6.1

Legacy DOC/DOT import includes partial support for pictures, shapes, formatting and sections; compare the result against the original. Mail merge supports spreadsheet recipient lists and conditional/next-record fields. Verify merged header/footer fields, lists, pagination and preserved DOCX XML rather than assuming a lossless round trip. These are source/documentation findings; no new CLI or GUI workflow was executed for this refresh.

## Previously documented behavior and verification

DOCM macros/signatures and DOTX/DOTM content types are preserved by the updated save path; verify retained package parts and signature status after editing. LaTeX .tex import/export is available, and DOCX charts/SmartArt/OLE preservation improves. Unknown CLI options are rejected before side effects. Live control now requires a per-window key. This review does not include launching the application or executing these new workflows.

Live control requires the per-window key for every request, or an initial `auth` request. MCP reads `WORDCRAFT_CONTROL_KEY` or the port-specific key file and sends it only to loopback hosts; a restart replaces the key. Never publish key contents. Missing/wrong keys, invalid JSON and oversized lines close the connection. Verify the intended session and recover state before replaying any mutation; headless `run` does not use this channel.

## Source links

- [Target-version release](https://github.com/storytold/wordcraft/releases/tag/v0.6.1)
- [apps/wordcraft-cli/src/main.rs](https://github.com/storytold/wordcraft/blob/v0.6.1/apps/wordcraft-cli/src/main.rs)
- [crates/engine/src/io.rs](https://github.com/storytold/wordcraft/blob/v0.6.1/crates/engine/src/io.rs)
- [docs/mcp.md](https://github.com/storytold/wordcraft/blob/v0.6.1/docs/mcp.md)
- [docs/control-protocol.md](https://github.com/storytold/wordcraft/blob/v0.6.1/docs/control-protocol.md)
- [README.md](https://github.com/storytold/wordcraft/blob/v0.6.1/README.md)
- [packaging/windows/package.ps1](https://github.com/storytold/wordcraft/blob/v0.6.1/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
