---
name: printcraft
description: "Use PrintCraft to inspect, render, combine, split, extract, annotate, fill forms, or organize PDF files. Trigger on PrintCraft PDF work; preserve originals and verify pages, forms, redactions, and saved output."
---

# PrintCraft

Inspect and edit PDF files with PrintCraft's headless tools or token-authenticated GUI control.

## Target version and setup

Written for PrintCraft 0.2.1. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/pdfcraft.

- Discover the CLI from `printcraft-cli` on PATH, or set `PRINTCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; on other systems, use the available matching platform build. Resolve the GUI independently when it is needed.
- Confirm the application's actual version using its supported version/help output or release/package metadata. Do not assume every CLI supports `--version` or subcommand `--help`.
- Verify executable provenance and task permission before launch. Start with read-only command/schema discovery, then a tiny copied-file trial. Keep unrelated documents, processes, devices, and ports undisturbed.
- Do not configure persistent MCP access, download models or plugins, enable recording, overwrite originals, or transmit files merely because the skill describes those features.

Example discovery after those checks, in a shell appropriate to the host:

```sh
CLI="${PRINTCRAFT_CLI:-$(command -v printcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set PRINTCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" tools
```

```powershell
$cli = $env:PRINTCRAFT_CLI
if (-not $cli) { $cli = (Get-Command printcraft-cli -ErrorAction Stop).Source }
& $cli tools
```

The command examples in the reference use synthetic relative filenames. Substitute real authorized inputs and distinct output destinations; never assume the example files exist.

## Workflow

1. Identify input PDFs, one-based requested page ranges, order, destination, and whether content/forms/metadata must be retained.
2. Use info/text for inspection and combine/extract/split/edit for file operations. Use tools for exact schemas. Run scripts are a JSON array in one fresh session; open the document before using its ID.
3. Use a new output copy; headless document edits remain in memory until doc_save. Restrict tool access with --root to the required folder.
4. Use GUI for visual annotations/forms and page review. Password/security changes, signatures, destructive redaction, and transmission still follow task-specific confirmation requirements.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another app's flags.

## Verify and deliver

Reopen the saved PDF, verify page count/order/rotation, text, annotations, metadata, form values, and output size, and render affected pages. For redaction, verify removed text and hidden content rather than judging the visual black box. Never claim a legal/digital signature validation from appearance alone.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

PDF documents; direct CLI render writes PAM RGBA, while automation page_render and GUI screenshots can write PNG. Text extraction and JSON info/tool schemas are available.

GUI --control takes a token-file path, not a port, and chooses a random loopback port. MCP is stdio; no --connect bridge. Keep tokens private and verify user-only file access. OCR needs text-detection.rten and text-recognition.rten, not Tesseract; models may be absent from the portable ZIP. Existing text edits, Office conversion, non-Latin OCR, XFA, advanced signatures/preflight remain limited.

Distinguish source-build dependencies from packaged-runtime requirements. Check the matching platform release and linked packaging documentation before installing extra dependencies.

## Example request

“Extract pages 1, 3, and 5 into a new PDF, then verify page order and render all three.”

Target app version: PrintCraft 0.2.1. If the installed or globally available PrintCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/pdfcraft before relying on these commands.
