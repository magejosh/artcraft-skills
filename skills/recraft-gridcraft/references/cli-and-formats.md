# GridCraft 0.3.0: CLI and format reference

## Evidence and use

Examples and command notes were checked against upstream tag v0.3.0, commit `fb823899c57b41703edcad2b6476cf4b8a01dfc4`. These are source/documentation findings, not a guarantee of behavior on a particular machine. Recheck after upgrading and prefer matching-version documentation over main.

Bare `gridcraft-cli` and `gridcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Prefer a documented script-file form where available, or the host's verified argument transport. Validate JSON before invocation and inspect received/resulting values. Never copy Unix paths or quoting blindly.

## Supported command examples

```text
gridcraft book.xlsx
gridcraft --sample sales
gridcraft --sample sales --control 7979
gridcraft-cli mcp
gridcraft-cli mcp --connect 7979
gridcraft-cli eval '=XLOOKUP("b",{"a","b"},{1,2})'
gridcraft-cli run --sample budget --cmd 'home.bold={"range":"B4:F4"}' --out budget.xlsx
gridcraft-cli cat budget.xlsx --range B4:F15
gridcraft-cli commands --search chart
gridcraft-cli run --in book.xlsx --cmd 'sheet.activate={"sheet":"Sales"}' --cmd 'file.printPreview={"sheets":"active"}'
gridcraft-cli run --in book.xlsx --cmd 'sheet.activate={"sheet":"Sales"}' --cmd 'file.exportPdf={"path":"sales.pdf","sheets":"active"}'
gridcraft-cli info book.xlsx --json
gridcraft-cli cat book.xlsx --range A1:F20 --sheet Sales
gridcraft-cli convert book.xlsx data.csv --sheet Sales
gridcraft-cli eval '=SUM(B2:B9)' --in book.xlsx
gridcraft-cli run --in book.xlsx --script steps.jsonl --out edited.xlsx --print A1:D5
```

COMMAND, JSON, READ_DIR, WRITE_DIR, and PRIVATE_TOKEN_FILE are grammar placeholders, not ready-to-run values. Discover schemas and fill them deliberately. Demo/sample operations create synthetic content, not a copy of a GUI project.

## Exact grammar and traps

`run` supports --in, --sample, --cmd, --script, --out, --print RANGE, --sheet, --csv, --formulas, --quiet. Commands may be ID, ID=JSON, ID JSON, or JSONL {command,params}; scripts execute in command-line order and stop on first failure. `cat` reads ranges; `eval --in FILE` evaluates against a workbook. Choose --sheet for flat CSV/TSV/HTML export. CLI convert does not export PDF. Use file.exportPdf with {path, sheets:active|all, range?, fitToPage?}; range selects cells on the active sheet. Explicitly activate the target sheet first. The result includes pages/bytes/path. Never use run --out output.pdf: ordinary save can put XLSX bytes behind a .pdf suffix. functions --search helps discover supported formula names. For PDF, run --sheet only affects console --print, not command selection: use sheet.activate. A Sheet! prefix in range does not select that sheet. Without range, PDF uses stored printArea or used bounds including charts/images/shapes. Page Setup controls margins/paper/scaling/title rows/breaks. sheets=all includes visible sheets; fitToPage bottoms out at 10% and cannot guarantee one page. Inspect file.printPreview before large exports (2,000-page cap). PDF WinAnsi encoding can turn unsupported characters into ?; visually check multilingual text.

## Live control and MCP

Control is newline-delimited JSON on loopback; GRIDCRAFT_CONTROL_PORT is supported. `send 7979 document.inspect` inspects live control. MCP --in book.xlsx creates headless state; --connect PORT selects live state. Screenshot/input require live mode, and those sessions must not be confused.

Use GUI when it materially helps. Launch the exact GUI executable, inspect its current document, use visible controls/automation IDs that exist, and save explicitly. GUI fallback does not authorize interfering with an unrelated session.

## Source links

- [PDF export command and schema](https://github.com/storytold/gridcraft/blob/v0.3.0/crates/engine/src/cmd/print.rs)

- [Target-version release](https://github.com/storytold/gridcraft/releases/tag/v0.3.0)
- [apps/gridcraft-cli/src/main.rs](https://github.com/storytold/gridcraft/blob/v0.3.0/apps/gridcraft-cli/src/main.rs)
- [docs/cli.md](https://github.com/storytold/gridcraft/blob/v0.3.0/docs/cli.md)
- [docs/mcp.md](https://github.com/storytold/gridcraft/blob/v0.3.0/docs/mcp.md)
- [docs/control-protocol.md](https://github.com/storytold/gridcraft/blob/v0.3.0/docs/control-protocol.md)
- [crates/engine/src/io.rs](https://github.com/storytold/gridcraft/blob/v0.3.0/crates/engine/src/io.rs)
- [packaging/windows/package.ps1](https://github.com/storytold/gridcraft/blob/v0.3.0/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
