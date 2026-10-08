---
name: deckcraft
description: "Use DeckCraft to create or edit presentations, PPTX decks, slide masters, notes, shapes, charts, and slide renders. Trigger on DeckCraft slide workflows, including PDF, image, or native deck delivery."
---

# DeckCraft

Build and render presentation decks with DeckCraft's shared command engine and GUI.

## Target version and setup

Written for DeckCraft 0.3.0. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/deckcraft.

- Discover the CLI from `deckcraft-cli` on PATH, or set `DECKCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; on other systems, use the available matching platform build. Resolve the GUI independently when it is needed.
- Confirm the application's actual version using its supported version/help output or release/package metadata. Do not assume every CLI supports `--version` or subcommand `--help`.
- Verify executable provenance and task permission before launch. Start with read-only command/schema discovery, then a tiny copied-file trial. Keep unrelated documents, processes, devices, and ports undisturbed.
- Do not configure persistent MCP access, download models or plugins, enable recording, overwrite originals, or transmit files merely because the skill describes those features.

Example discovery after those checks, in a shell appropriate to the host:

```sh
CLI="${DECKCRAFT_CLI:-$(command -v deckcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set DECKCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" commands
```

```powershell
$cli = $env:DECKCRAFT_CLI
if (-not $cli) { $cli = (Get-Command deckcraft-cli -ErrorAction Stop).Source }
& $cli commands
```

The command examples in the reference use synthetic relative filenames. Substitute real authorized inputs and distinct output destinations; never assume the example files exist.

## Workflow

1. Confirm audience, story, slide count or source deck, aspect ratio, and deliverable. Preserve supplied master/layout/theme structure.
2. Use the command catalog for exact stable IDs and parameter schemas; do not infer a layout or chart schema from another office app.
3. Build or edit a copy, save the editable deck, and render every slide. Use GUI for visual layout, presenter/media checks, or unsupported controls.
4. Check font availability before layout. Review speaker notes, comments, masters, and media links when they matter.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another app's flags.

## Verify and deliver

Render every slide, inspect overflow, alignment, legibility, chart labels, images, and text wrapping, then reopen the saved deck. Check transitions/animations/media in the GUI if requested; a static render cannot validate playback.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

PPTX read/write; .deckcraft native example; PDF slides/notes/handouts, PNG/JPEG, and outline exports. Embedded audio/video support is documented.

Early-development interoperability requires a round-trip check. Source builds optionally use sibling craft-fonts; releases include fonts and system fallback. Do not promise a feature solely from command counts.

Distinguish source-build dependencies from packaged-runtime requirements. Check the matching platform release and linked packaging documentation before installing extra dependencies.

## Example request

“Add a title-only slide to a sample deck, save an editable copy, and render all slides for visual review.”

Target app version: DeckCraft 0.3.0. If the installed or globally available DeckCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/deckcraft before relying on these commands.
