---
name: wordcraft
description: "Use WordCraft for document writing, DOCX editing, styles, tables, sections, comments, tracked changes, mail merge, text extraction, and supported conversions. Trigger on WordCraft document tasks; preserve structure and inspect rendered pagination."
---

# WordCraft

Create, inspect, edit, and convert word-processing documents with WordCraft.

## Target version and setup

Written for WordCraft 0.3.0. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/wordcraft.

- Discover the CLI from `wordcraft-cli` on PATH, or set `WORDCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; on other systems, use the available matching platform build. Resolve the GUI independently when it is needed.
- Confirm the application's actual version using its supported version/help output or release/package metadata. Do not assume every CLI supports `--version` or subcommand `--help`.
- Verify executable provenance and task permission before launch. Start with read-only command/schema discovery, then a tiny copied-file trial. Keep unrelated documents, processes, devices, and ports undisturbed.
- Do not configure persistent MCP access, download models or plugins, enable recording, overwrite originals, or transmit files merely because the skill describes those features.

Example discovery after those checks, in a shell appropriate to the host:

```sh
CLI="${WORDCRAFT_CLI:-$(command -v wordcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set WORDCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" commands --json
```

```powershell
$cli = $env:WORDCRAFT_CLI
if (-not $cli) { $cli = (Get-Command wordcraft-cli -ErrorAction Stop).Source }
& $cli commands --json
```

The command examples in the reference use synthetic relative filenames. Substitute real authorized inputs and distinct output destinations; never assume the example files exist.

## Workflow

1. Confirm audience, purpose, source/template, change scope, output format, and preservation requirements for comments/track changes.
2. Inspect structure/text before edits and use named styles, sections, headers/footers, tables, and reference fields rather than manual spacing.
3. Use the command catalog for exact selectors/parameters; preserve existing comments, revisions, citations, and fields unless explicitly asked to resolve them.
4. Use GUI for pagination, layout, and review controls. Treat macros as executable content and CSV mail merge as data processing, not permission to send mail.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another app's flags.

## Verify and deliver

Reopen the editable output and render pages. Inspect pagination, headings, tables, lists, footnotes, headers/footers, bookmarks, links, and tracked changes. Compare important text against the source; disclose conversion losses.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

Open DOCX/DOCM/DOTX, text, Markdown, HTML, RTF, ODT, native JSON; export DOCX/PDF/text/Markdown/HTML/RTF/ODT/PNG/JSON. PDF is output-only; legacy binary DOC is unverified. PNG convert outputs page 1.

Charts, SmartArt, equation editor, Draw tab, and native printing are roadmap work. Offline proofing uses public-domain Moby data. No external Windows portable runtime dependency is documented.

Distinguish source-build dependencies from packaged-runtime requirements. Check the matching platform release and linked packaging documentation before installing extra dependencies.

## Example request

“Inspect a DOCX, bold one agreed text selection in a copy, convert to PDF, and review pagination.”

Target app version: WordCraft 0.3.0. If the installed or globally available WordCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/wordcraft before relying on these commands.
