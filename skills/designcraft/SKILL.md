---
name: designcraft
description: "Use DesignCraft for publication page layout, magazines, spreads, threaded text frames, styles, parent pages, IDML, and page PNG rendering. Trigger on DesignCraft publishing tasks; verify the target version’s export capabilities."
---

# DesignCraft

Compose multipage publications and verify text flow and page appearance in DesignCraft.

## Target version and setup

Written for DesignCraft 0.2.1. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/designcraft.

- Discover the CLI from `designcraft-cli` on PATH, or set `DESIGNCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; on other systems, use the available matching platform build. Resolve the GUI independently when it is needed.
- Confirm the application's actual version using its supported version/help output or release/package metadata. Do not assume every CLI supports `--version` or subcommand `--help`.
- Verify executable provenance and task permission before launch. Start with read-only command/schema discovery, then a tiny copied-file trial. Keep unrelated documents, processes, devices, and ports undisturbed.
- Do not configure persistent MCP access, download models or plugins, enable recording, overwrite originals, or transmit files merely because the skill describes those features.

Example discovery after those checks, in a shell appropriate to the host:

```sh
CLI="${DESIGNCRAFT_CLI:-$(command -v designcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set DESIGNCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" commands
```

```powershell
$cli = $env:DESIGNCRAFT_CLI
if (-not $cli) { $cli = (Get-Command designcraft-cli -ErrorAction Stop).Source }
& $cli commands
```

The command examples in the reference use synthetic relative filenames. Substitute real authorized inputs and distinct output destinations; never assume the example files exist.

## Workflow

1. Establish page size, margins, facing pages, columns, page count, assets, and required exchange format.
2. Preserve parent-page relationships, named paragraph/character styles, threaded stories, swatches, and layers when adapting a publication.
3. Discover supported commands, then choose deterministic CLI page renders or GUI layout operations. Use GUI for frame fitting, spread inspection, and fine typography.
4. Inspect overset text, missing fonts/images, baseline and column alignment, page numbering, and spread order.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another app's flags.

## Verify and deliver

Render every page and inspect at reading size. Check story overset and reopen the saved native/IDML output. Verify page count, text flow, fonts, and assets. PDF/EPUB are implemented in the matching v0.2.1 source; confirm the available CLI before using them.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

.designcraft native JSON and IDML input; native/IDML, PNG/JPEG, PDF, and EPUB output are implemented in tagged v0.2.1 source. Do not promise INDD input.

Some README text calls PDF roadmap work; prefer the matching parser/engine evidence, then verify the binary. GUI writes preferences under %APPDATA%\DesignCraft. Web builds lack desktop control. Run exports execute in option order; lowercase extensions avoid case-sensitive checks.

Distinguish source-build dependencies from packaged-runtime requirements. Check the matching platform release and linked packaging documentation before installing extra dependencies.

## Example request

“Render the sample magazine to a new output folder and review all pages for clipping and overset text.”

Target app version: DesignCraft 0.2.1. If the installed or globally available DesignCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/designcraft before relying on these commands.
