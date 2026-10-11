---
name: pdfcraft
description: "Use PDFCraft to inspect, render, organize, annotate, fill, and edit PDF documents, or automate PDF workflows through pdfcraft-cli. Preserve originals, discover version-specific tool schemas, and verify saved pages and form values."
---

# PDFCraft

Work with PDF documents through PDFCraft's one-shot CLI, schema-driven automation, or desktop interface.

## Target version and setup

Written for PDFCraft 0.6.0. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/pdfcraft.

Discover `pdfcraft-cli` on PATH or set `PDFCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; use the matching platform build elsewhere. Resolve the GUI separately. Do not assume an installation directory, a running app, or that older `printcraft-cli` instructions apply unchanged.

After verifying executable provenance and task permission, inspect the version and tool schemas:

```sh
CLI="${PDFCRAFT_CLI:-$(command -v pdfcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set PDFCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" --version
"$CLI" tools
```

```powershell
$cli = $env:PDFCRAFT_CLI
if (-not $cli) { $cli = (Get-Command pdfcraft-cli -ErrorAction Stop).Source }
& $cli --version
& $cli tools
```

`--version` is supported; generic `--help` prints usage and exits unsuccessfully in this version. Use the linked parser reference and `tools` schemas instead of inventing a help hierarchy.

## Choose the appropriate workflow

1. Identify authorized inputs, exact page numbers and order, required changes, output path, and whether forms, annotations, bookmarks, metadata, or signatures must be retained.
2. Use `info` and `text` for inspection; use `render` for a page preview. Direct CLI page numbers are one-based. Use comma-separated page numbers for extraction/edit lists, not an assumed range expression.
3. Use direct `combine`, `extract`, `split`, or `edit` commands for simple file operations. Write to distinct destinations and inspect the actual saved output. The direct commands are not confined by automation's `--root` setting.
4. For forms, annotations, OCR, existing-content edits, creation/export, or multiple dependent steps, use the reference’s advanced-workflow routing to discover the exact tool schema and run a JSON-array script. Open the document and use it within the same invocation; a later `run` command starts a new session. Persist ordinary document edits with `doc_save` to a new path; check each advanced tool for direct-write side effects.
5. Use the GUI when visual review or an unsupported control requires it. Verify the application and document before live control. MCP runs over stdio; desktop UI control is a separate token-authenticated loopback channel, not an MCP port to guess.
6. Treat password changes, signatures, destructive redaction, recording or screen capture, model downloads, persistent access, and transmission according to the task's permissions. Do not place credentials in example scripts, command histories, chat, or repository files.

## Forms, OCR, and output checks

- Inspect `form_fields` before filling fields. Match exact names, field types, options, and read-only flags; then save, reopen, inspect values, and render appearances. A visible typed signature is not proof of cryptographic signing.
- Check `ocr_status` before OCR. Use a small copied-file trial, verify recognized text against the image, and save a separate searchable PDF. The desktop release ships OCR resources; check the actual package/session before requesting more models or languages.
- Reopen every saved PDF and check page count, order, rotation, text, metadata, and requested form/annotation changes. Render affected pages; compare important pages at a readable resolution.
- For redaction, verify removal from extracted text, hidden content, and saved bytes with appropriate independent tooling. A black rectangle is not sufficient. Preserve the signed original and verify signature status independently after any edit.
- Report actual output paths, changes, warnings, and what was verified. Distinguish documentation-supported features from runtime-tested behavior; file existence or exit code zero alone does not prove fidelity.

## Important limits

PDFCraft 0.6.0 exposes tools for content editing, Office export, accessibility checks, PDF/A workflows, comparison, and optimization as well as page operations. Coverage varies; complex text edits, script coverage, Office interoperability, XFA, preflight and long-term signature validation require document-specific checks. Discover the relevant schema and test the actual document; a menu item or tool name is not a fidelity guarantee.

The CLI's `render` command at this target version writes real PNG, JPEG, TIFF, or PAM according to the output suffix. This differs from older instructions that describe PAM-only output. Automation `page_render` returns PNG.

## Changes in 0.6.0

Desktop release packages now ship OCR resources. Check ocr_status in the actual session before OCR instead of immediately requesting a download. Compact MCP exposes a core tool set plus discovery; use the returned schemas for advanced operations. Package presence does not establish OCR accuracy or signature validity. These are source-reviewed changes; earlier runtime checks apply only to their recorded versions. See the reference for exact grammar and verification.

PDF/A verification now checks the output-intent color space; image-to-PDF creation retains embedded ICC profiles. The release also improves encrypted-document signing, certificate constraints, OCR/batch result preservation and annotation/page organization. Check the exact schemas, per-file results, saved copies and independent signature/standard validation. Windows portable launches can hand documents to the existing instance, so verify the target window instead of assuming a fresh isolated process. These are tagged-source and release-note findings, not runtime tests.

Target app version: PDFCraft 0.6.0. If the installed or globally available PDFCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/pdfcraft before relying on these commands.
