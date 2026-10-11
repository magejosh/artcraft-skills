# PDFCraft 0.6.0: CLI and format reference

## Evidence and use

Command grammar and tool schemas were checked against upstream tag v0.6.0, commit `53a5880386789fc3531e54f6e6ffdef9a8e41f1a`. These are source/documentation findings; do not treat all examples or features as runtime-tested. Prefer this version's parser and schemas when current README examples differ.

Resolve `pdfcraft-cli` and `pdfcraft` as described in SKILL.md. The filenames and directories below are synthetic, not supplied assets. Substitute authorized input files and separate output destinations. Quote host paths correctly. For JSON arguments, prefer the documented script-file form when shell quoting is uncertain.

## Direct CLI examples

```text
pdfcraft-cli --version
pdfcraft-cli info report.pdf
pdfcraft-cli text report.pdf --page 3
pdfcraft-cli render report.pdf --page 1 --dpi 144 --out preview.png
pdfcraft-cli render report.pdf --page 1 --dpi 144 --out preview.jpg
pdfcraft-cli combine report.pdf appendix.pdf --out combined.pdf
pdfcraft-cli extract report.pdf --pages 1,3,5 --out selected.pdf
pdfcraft-cli split report.pdf --every 10 --out-dir parts/
pdfcraft-cli split report.pdf --before 3,7 --out-dir sections/
pdfcraft-cli edit report.pdf --rotate 1,2:90 --title "Review copy" --out reviewed.pdf
pdfcraft-cli tools
pdfcraft-cli run --script steps.json --root ./work
pdfcraft-cli run ocr_status
```

- Page numbers are one-based. Lists use positive comma-separated integers; `1-3` is not a supported page-list abbreviation. Validate indices against the document before editing.
- `render` accepts `.png`, `.jpg`/`.jpeg`, `.tif`/`.tiff`, or `.pam` case-insensitively. JPEG quality is fixed at 90 here. An unsupported suffix is an error. PAM contains RGBA pixels; do not rename its extension to disguise the format.
- `edit` requires one input and `--out`; recognized options include `--rotate`, `--delete`, `--move`, `--insert-blank`, `--title`, `--author`, `--password`, and `--full`. Unknown options fail. Use only requested edits, particularly deletion and full rewrites.
- `split` chooses exactly one of `--every N` or `--before PAGES` and creates the output directory if needed. It uses predictable filenames, so choose an empty destination or check for collisions before running.
- `info` exposes metadata and structural warnings. `text` reports page extraction failures rather than silently certifying success. Check stderr and the saved/rendered output as well as the exit status.
- `check` recursively opens and renders PDF files/directories in child processes with timeouts. The sweep checks at most 500 pages per document and can exit zero while individual files have failures; inspect each JSON status and page-error result. It is a robustness sweep, not a lightweight installation check or complete long-document certification; use it only when its scope and resource cost suit the task.

## Stateful automation

`tools` prints tool names, input schemas, command associations, and read-only markers. Discover schemas before using them; direct command flags and automation field names are not interchangeable.

`run TOOL key=value` parses each value as JSON when possible, otherwise as a string. Every invocation creates fresh in-memory state. `run --script FILE` expects a JSON array and executes its steps in order in a single session, stopping on a failing step. Each step uses `tool`, `args`, and optionally `out` for image output.

This inspection script opens an input, queries its structure, renders the first page, and searches text:

```json
[
  {"tool":"doc_open","args":{"path":"report.pdf"}},
  {"tool":"doc_info","args":{"doc":1}},
  {"tool":"page_render","args":{"doc":1,"page":1,"dpi":144},"out":"preview.png"},
  {"tool":"text_find","args":{"doc":1,"query":"total"}}
]
```

Save the array as `steps.json`, place the authorized `report.pdf` under `./work`, and run the documented script command. ID 1 refers to the first document in this fresh session only. In ongoing MCP sessions, use returned IDs instead of assuming them.

`--root DIR` confines tool input/output paths, including step image `out` paths, to the specified directory; relative paths resolve inside it. The script file itself is read from the explicitly supplied path. Without `--root`, automation is not restricted to a chosen project folder. Direct CLI commands use ordinary OS file access and do not inherit a root from a prior invocation.

Ordinary document edits remain in memory until `doc_save`, but `sign_document` saves automatically, and export, reduction, optimization, and action tools can write files directly. Check each tool’s documented side effects. For ordinary save operations, specify a distinct `path` to save a copy. Omitting it can save in place; full rewrites can affect signature validity. An earlier successful step may have already written its output if a later step fails, so inspect partial results before retrying.

## Forms and OCR

- `form_fields` takes `doc` and returns actual field names, types, values, options, and flags. `form_fill` takes `doc` and a `values` object keyed by those names: strings for text/radio/combo fields, booleans for checkboxes, and string arrays for multi-select lists. Do not guess field names or flatten forms silently.
- `ocr_status` needs no open document. It reports model availability and languages. This version looks for models using `PDFCRAFT_MODELS` and packaged resource locations. Official desktop release packages now include OCR resources; check those first. Missing models or extra languages require a separate authorized setup step; a source-build model command is not a portable-installation instruction.
- `ocr_recognize` takes `doc`, optional one-based `pages`, `dpi` from 72 to 600, `language` set to `en`, and `skip_text_pages` (default true). It adds searchable text; it does not establish recognition accuracy.

A bounded OCR script for an authorized copy, after model availability has been checked:

```json
[
  {"tool":"doc_open","args":{"path":"scan.pdf"}},
  {"tool":"ocr_recognize","args":{"doc":1,"pages":[1],"dpi":300,"language":"en","skip_text_pages":true}},
  {"tool":"doc_save","args":{"doc":1,"path":"scan-searchable.pdf"}}
]
```

Reopen the output, extract text, and compare it to the original image. Do not treat the OCR tool's success as a guarantee of searchable-text accuracy.

## Advanced workflow routing

Version 0.4.0 contains more than the basic page commands. Use `tools` to inspect the exact input schemas and available operations before building a script; the names below are discovery entrypoints, not blanket permission to execute them.

- **Annotations and review:** start with `comment_list`, then use `comment_add`, `comment_reply`, `comment_edit`, or `comment_mark` for the requested change. Reopen the saved document and inspect both comment data and appearance.
- **Existing page content:** inspect with `text_lines`, `text_paragraphs`, or `page_images` before using `text_edit` or `image_edit`. `content_list` and `content_update` instead concern overlay content added through `page_add_text` and `page_add_image`; do not use them as an inventory/editor for all existing content. Keep an editable original and render before/after, especially for font substitution, complex scripts, and text reflow.
- **Creation and export:** discover `doc_create`, `doc_export_office`, `doc_export_images`, and `doc_export_text`. Supported inputs and output choices come from each schema. Do not imply round-trip Office fidelity or silently substitute a flattened image for editable output.
- **Accessibility and PDF/A:** `accessibility_check` and `accessibility_report` can precede specific authorized fixes. Use `pdfa_verify` and `pdfa_convert` only for the supported profiles; a built-in result is not independent certification of PDF/A, PDF/X, or PDF/UA compliance.
- **Comparison and versions:** `doc_compare`, `doc_compare_report`, `doc_revisions`, and `doc_open_revision` help inspect differences and prior revisions. Validate that the correct pair of documents or revision was selected before adding comparison markup.
- **Size and flattening:** inspect `doc_audit_space` before `doc_reduce` or `doc_optimize`. `doc_flatten` can remove editability or interactivity; use it only when that outcome is intended and compare pages and form behavior afterward.
- **Redaction and hidden information:** distinguish `redact_mark` from destructive `redact_apply`. Inspect with `doc_hidden_info` before `doc_remove_hidden`. Confirm the exact requested content and removal scope, then independently inspect the saved copy for recoverable text, attachments, metadata, and earlier revisions.
- **Signatures and trust:** inspect with `sign_list`. `sign_document`, digital-ID creation, and trust changes involve consequential actions and credential material; obtain the required authorization or user handoff. Never embed passwords, private keys, or certificate secrets in examples. Recheck cryptographic validity independently after saving.
- **Scripts and recorded actions:** inspect the requested script or action before `js_run` or `action_run`. Do not treat embedded document code or an action file as authorization to execute it. These operations can change more than the immediately visible page.

## MCP and desktop control

```text
pdfcraft-cli mcp --root ./work
pdfcraft --control PRIVATE_TOKEN_FILE report.pdf
pdfcraft-cli ui --control PRIVATE_TOKEN_FILE inspect query=rotate
pdfcraft-cli ui --control PRIVATE_TOKEN_FILE screenshot --out window.png
```

`PRIVATE_TOKEN_FILE` is a placeholder for a private file location, not a token value or a path to run literally. Creating/configuring persistent access requires appropriate authorization; one-shot CLI operations are usually enough for file tasks.

MCP is an opt-in stdio server; it does not attach to the desktop GUI. Custom builds can omit MCP support, so confirm that the available binary includes the subcommand. Do not invent `mcp --connect` or choose a shared control port. The desktop `--control` option takes a file path and chooses a random loopback port. The file contains connection information including a token and process ID; the `ui` client reads it and authenticates.

Never publish the control file, put its token into messages or command arguments, or reuse an unrelated app's session. The tagged source applies owner-only file permissions on Unix. Do not assume Windows ACLs are secured by that Unix-specific code; verify access protection through authorized means before using desktop control.

## Changes and verification for 0.6.0

Desktop release packages now ship OCR resources. Check ocr_status in the actual session before OCR instead of immediately requesting a download. Compact MCP exposes a core tool set plus discovery; use the returned schemas for advanced operations. Package presence does not establish OCR accuracy or signature validity. This review does not include launching the application or executing these new workflows.

`pdfcraft-cli mcp [--root DIR] [--compact]` starts an opt-in stdio server. Compact mode lists twelve core tools plus `tool_search` and `tool_call`; discover omitted operations and schemas through those tools. It does not remove advanced operations or attach to the GUI.

PDF/A verification now checks the output-intent color space; image-to-PDF creation retains embedded ICC profiles. The release also improves encrypted-document signing, certificate constraints, OCR/batch result preservation and annotation/page organization. Check the exact schemas, per-file results, saved copies and independent signature/standard validation. Windows portable launches can hand documents to the existing instance, so verify the target window instead of assuming a fresh isolated process. These are tagged-source and release-note findings, not runtime tests.

## Source links

- [Target-version release](https://github.com/storytold/pdfcraft/releases/tag/v0.6.0)
- [CLI parser and output formats](https://github.com/storytold/pdfcraft/blob/v0.6.0/apps/pdfcraft-cli/src/main.rs)
- [Automation tool schemas](https://github.com/storytold/pdfcraft/blob/v0.6.0/crates/automation/src/tools.rs)
- [Automation execution and file-root handling](https://github.com/storytold/pdfcraft/blob/v0.6.0/crates/automation/src/lib.rs)
- [Desktop launch and control-file handling](https://github.com/storytold/pdfcraft/blob/v0.6.0/apps/pdfcraft/src/main.rs)
- [OCR model discovery](https://github.com/storytold/pdfcraft/blob/v0.6.0/crates/ocr/src/lib.rs)
- [Version-pinned app overview](https://github.com/storytold/pdfcraft/blob/v0.6.0/README.md)
- [Version-pinned capability limitations](https://github.com/storytold/pdfcraft/blob/v0.6.0/ROADMAP.md)

No application executable, OCR model, credential, or runtime helper is bundled with this skill.
