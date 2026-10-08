# ArtCraft Skills

Twelve separate, portable assistant skills for the reCraft creative applications. Each skill contains an application workflow, a version-pinned CLI reference, format caveats, and output-verification guidance.

These are reusable templates. They do not contain a user's installation paths, personal project details, credentials, app binaries, models, or icons. They do not install or launch an application, and they do not change existing skill installations.

## Target versions

| Application | Written for | Skill | Official application repository |
| --- | --- | --- | --- |
| CADCraft | 0.3.0 | [recraft-cadcraft](skills/recraft-cadcraft/SKILL.md) | [storytold/cadcraft](https://github.com/storytold/cadcraft) |
| DeckCraft | 0.3.0 | [recraft-deckcraft](skills/recraft-deckcraft/SKILL.md) | [storytold/deckcraft](https://github.com/storytold/deckcraft) |
| DesignCraft | 0.2.1 | [recraft-designcraft](skills/recraft-designcraft/SKILL.md) | [storytold/designcraft](https://github.com/storytold/designcraft) |
| EffectCraft | 0.4.0 | [recraft-effectcraft](skills/recraft-effectcraft/SKILL.md) | [storytold/effectcraft](https://github.com/storytold/effectcraft) |
| FilmCraft | 0.2.1 | [recraft-filmcraft](skills/recraft-filmcraft/SKILL.md) | [storytold/filmcraft](https://github.com/storytold/filmcraft) |
| GridCraft | 0.3.0 | [recraft-gridcraft](skills/recraft-gridcraft/SKILL.md) | [storytold/gridcraft](https://github.com/storytold/gridcraft) |
| LightCraft | 0.2.1 | [recraft-lightcraft](skills/recraft-lightcraft/SKILL.md) | [storytold/lightcraft](https://github.com/storytold/lightcraft) |
| PhotoCraft | 0.3.0 | [recraft-photocraft](skills/recraft-photocraft/SKILL.md) | [storytold/photocraft](https://github.com/storytold/photocraft) |
| PrintCraft | 0.2.1 | [recraft-printcraft](skills/recraft-printcraft/SKILL.md) | [storytold/pdfcraft](https://github.com/storytold/pdfcraft) |
| SoundCraft | 0.3.0 | [recraft-soundcraft](skills/recraft-soundcraft/SKILL.md) | [storytold/soundcraft](https://github.com/storytold/soundcraft) |
| VectorCraft | 0.4.0 | [recraft-vectorcraft](skills/recraft-vectorcraft/SKILL.md) | [storytold/vectorcraft](https://github.com/storytold/vectorcraft) |
| WordCraft | 0.3.0 | [recraft-wordcraft](skills/recraft-wordcraft/SKILL.md) | [storytold/wordcraft](https://github.com/storytold/wordcraft) |

PrintCraft's official repository is named `pdfcraft`; the v0.2.1 executable names remain `printcraft` and `printcraft-cli`.

The machine-readable [skills.json](skills.json) records the target versions and exact upstream source commits used for command research. A target version is not a claim of compatibility with every newer version. The last line of every SKILL.md directs the reader to the individual application's official repository if the installed or globally available app is newer.

## Use or install a skill

1. Review the selected SKILL.md and its linked reference.
2. Copy that entire `skills/recraft-<app>` folder into the skill directory configured by your assistant, or use that assistant's supported local skill-import workflow. Preserve the `references` subfolder. Follow the host's current skill-discovery instructions; importing these files does not install the application.
3. If a same-named skill already exists, compare and deliberately merge or choose a different destination. Do not overwrite a customized installation by default.
4. Find an authorized, trusted application build for your platform. Discover its CLI on PATH or set the per-app variable, such as `CADCRAFT_CLI`, to the verified executable path. No common installation root is assumed.
5. Confirm the actual app version. Read the matching app's help/schema output, use copied inputs and separate outputs, and verify the result before broader use.

Optional copy examples, run from this repository root only after setting `SKILLS_DIR` to the intended destination:

```sh
: "${SKILLS_DIR:?Set SKILLS_DIR to the intended assistant skill directory}"
mkdir -p "$SKILLS_DIR"
test ! -e "$SKILLS_DIR/recraft-cadcraft" || { printf '%s\n' 'Destination exists; compare it first.' >&2; exit 1; }
cp -R skills/recraft-cadcraft "$SKILLS_DIR/"
```

```powershell
if (-not $env:SKILLS_DIR) { throw 'Set SKILLS_DIR to the intended assistant skill directory.' }
$destination = Join-Path $env:SKILLS_DIR 'recraft-cadcraft'
if (Test-Path $destination) { throw 'Destination exists; compare it first.' }
New-Item -ItemType Directory -Path $env:SKILLS_DIR -Force | Out-Null
Copy-Item -Recurse 'skills/recraft-cadcraft' $destination
```

To use a skill without installing it, give a capable assistant its SKILL.md path and the task. For example:

- “Use recraft-cadcraft to inspect drawing.dxf, preserve its units and layers, and save a separate SVG preview.”
- “Use recraft-gridcraft to inspect formulas in budget.xlsx and verify totals after saving an edited copy.”
- “Use recraft-printcraft to extract pages 1, 3, and 5 into a separate PDF, then verify page order and render the result.”

Example filenames are synthetic. Supply actual authorized files; do not assume they are included here. Resolve shell quoting on the host, particularly for JSON arguments in Windows PowerShell. The CLI grammar differs across apps: `--connect`, `--bridge`, `--in`, `--file`, `--save`, `--out`, and page indices are not interchangeable.

## Verification and limitations

Command references were checked against the exact upstream versions and commits in skills.json. Bounded Linux x86_64 CLI smoke checks used release archives whose SHA-256 values matched release checksums and GitHub asset digests, on Debian 13 with glibc 2.41. These checks established only the following small-fixture behaviors:

- CADCraft: DXF create/save/reopen/render with geometry, units, and layers preserved
- DeckCraft: PPTX title save/reopen/render
- DesignCraft: editable native text-frame save/reopen/render
- EffectCraft: native project reopen and a small CPU-rendered frame
- FilmCraft: native project reopen and a small PNG frame render
- GridCraft: XLSX formula retention and recalculation after saving again
- LightCraft: exposure/rating persistence and PNG export
- PhotoCraft: two-layer native/PSD save/reopen/edit
- PrintCraft: one-page PDF inspect/text/render and title/rotation edit/reopen
- SoundCraft: session reopen and a byte-identical short WAV bounce
- VectorCraft: editable native shapes and SVG path/render parity
- WordCraft: DOCX text retention and rendering

Those checks do not certify every reference example, GUI behavior, GPU rendering, physical audio devices, large-file performance, complex format fidelity, or cross-platform interoperability. LightCraft timestamp metadata was not established as reliable. Availability of source code does not imply that a packaged binary exists for every platform. Recheck package provenance, prerequisites, app version, CLI schemas, and output fidelity on the actual host.

These files do not grant permission to run an untrusted executable, overwrite originals, record audio, install plugins/models, expose a network listener, add persistent access, or send files. Respect the current task's permissions. Do not expose unauthenticated control ports, reuse another session's port, or publish token-file contents.

## Validate the template package

Run the repository's read-only structural checks with Python 3.9 or newer:

```sh
python3 tools/validate.py
```

On Windows, `py -3 tools/validate.py` is an equivalent option. The validator checks the twelve expected apps, frontmatter, target versions, final-line notices, reference links, and source pins. It does not execute reCraft applications or prove feature correctness.

No license has been selected for these templates. Upstream software and documentation retain their own licenses; this repository does not redistribute app binaries, fonts, models, or icons.
