# Testing workflows

## Structural validation

Run the optional package check with Python 3.9 or newer:

```sh
python3 -B tools/validate.py
```

On Windows, `py -3 -B tools/validate.py` is equivalent. This check does not modify files, contact services, install dependencies, or launch the apps.

The validator checks expected manifest entries and skill folders, basic frontmatter/name/description shape, app version/tag/repository consistency, source-commit text, final notices, reference titles, relative links, source-link version syntax, trailing newlines, and unfinished placeholders. It is useful for catching omissions when app names or versions change.

Its scope is deliberately limited: it is not a full YAML parser, privacy scanner, inventory audit, source-link availability test, or application test. A pass does not establish command correctness, current documentation accuracy, export fidelity, or that every file is safe to publish. Independently inspect the complete diff and file inventory for private information, unexpected files, unsafe examples, broken links, and claims stronger than the evidence.

After an authorized repository update, read back the changed files, verify the branch points at the intended commit, and check the repository's actual sharing state. Do not change visibility or invite collaborators as a side effect of a content edit. Stop for clarification if the observed audience conflicts with the approved publication scope.

## Read-only upstream update checks

Use the established checker instead of assembling a new release lookup:

```sh
python3 -B tools/update_check.py
python3 -B tools/update_check.py --json --timeout 10
```

On Windows, replace `python3` with `py -3`. An optional `--manifest path/to/skills.json` selects another manifest explicitly; the default resolves the repository's manifest relative to the script, not the current working directory.

The checker makes at most one unauthenticated metadata request per valid unique upstream repository to GitHub's latest-stable-release endpoint. It does not use tokens, download release assets, write files, install apps, change version pins, or retry failed requests automatically. Requests run sequentially. The per-request socket timeout defaults to 10 seconds and accepts values greater than 0 through 60 seconds. A reported rate limit stops further requests; remaining rows are unknown.

Compare the manifest target against the release's three-part semantic version. A leading `v` is accepted, components compare numerically, prerelease ordering is handled, and build metadata does not change precedence. Drafts, prereleases, unsupported version tags, malformed responses, and failed checks are not reported as current. This uses GitHub's designated latest stable release, not an installed-app scan or a complete release-history search.

Results use four states:

- `update_available`: the latest stable release is newer than the skill's target.
- `current`: the target and latest stable version have equal precedence.
- `ahead`: the manifest target is newer than the release returned by GitHub; review the target and upstream release state.
- `unknown`: the comparison could not be established. Keep the error visible rather than calling the app up to date.

Exit code 0 means every comparison is known, including available updates and ahead targets. Exit code 1 means at least one comparison is unknown; successful rows remain usable. Exit code 2 means invalid command arguments or an unreadable/invalid top-level manifest. With `--json`, inspect `results` and `summary`; do not interpret exit 0 as “no updates.”

Portable asset labels are conservative filename hints, not a compatibility or archive-content guarantee. Installer packages, source archives, signatures, and checksums are excluded. Each accepted asset URL must belong to the same upstream release on GitHub. Use the official release page when no suitable portable asset is recognized, and verify platform, architecture, provenance, and checksums before any separately authorized download.

### Offline checker tests

Run the automated mocked-response suite without network access:

```sh
python3 -B -m unittest discover -s tests -v
```

The tests exercise semantic-version comparisons, stable-release filtering, response failures and rate limits, partial results, manifest and URL validation, and asset selection. These tests validate the checker; they do not certify upstream app releases.

### Verification record

Before the six-app target refresh on 2026-10-09, all 35 mocked checker tests and the 12-skill structural checks passed. A bounded live metadata run covered all twelve upstream repositories. One initial CADCraft timeout was correctly reported as unknown; a separate targeted retry succeeded. The completed check found six newer stable releases and six matching targets, with no unresolved comparisons. No release assets were downloaded and no apps or skill version pins were changed by the check. Rerun the checker for current release information; this record is not a promise that those statuses remain current.

After the six target versions were refreshed later on 2026-10-09, a second bounded live check reported all twelve targets matching GitHub’s latest stable releases, with no unknown comparisons. This verified the manifest/release comparison only, not the installed applications. The 35 mocked checker tests also passed after the manifest update.

### A requested portable app update

1. Run the read-only check and report the target version, newer release, relevant portable assets, and any unknown checks.
2. Wait for a request to update the app; the check alone does not authorize downloading or installing it.
3. Verify the selected official release, platform/architecture, checksum or signature information, and any new prerequisites.
4. Download and extract the authorized portable release into a separate versioned folder alongside the existing app. Keep the old copy for the user to remove; do not overwrite it or change system-wide defaults incidentally.
5. Run a bounded version/help/schema check and a small copied-file trial suited to the app. Read the changed official docs before updating the skill's target version/source pins, then rerun structural checks and relevant tests.

## Twelve-app source and package review (2026-10-11)

The twelve targets below were reviewed against their official tagged CLI source, linked documentation and release notes. Each official Windows x64 portable archive matched both the GitHub asset SHA-256 and the publisher checksum file, passed ZIP CRC verification, and contained GUI/CLI executables and a README. Extraction preserved existing versions. The optional portable marker is package-specific, not a universal requirement.

| App | Target | Evidence scope |
| --- | --- | --- |
| CADCraft | 0.5.0 | Tagged source/docs and portable package verification |
| DeckCraft | 0.5.0 | Tagged source/docs and portable package verification |
| DesignCraft | 0.6.0 | Tagged source/docs and portable package verification |
| EffectCraft | 0.7.0 | Tagged source/docs and portable package verification |
| FilmCraft | 0.6.0 | Tagged source/docs and portable package verification |
| GridCraft | 0.5.0 | Tagged source/docs and portable package verification |
| LightCraft | 0.6.0 | Tagged source/docs and portable package verification |
| PDFCraft | 0.6.0 | Tagged source/docs and portable package verification |
| PhotoCraft | 0.6.0 | Tagged source/docs and portable package verification |
| SoundCraft | 0.5.0 | Tagged source/docs and portable package verification |
| VectorCraft | 0.9.0 | Tagged source/docs and portable package verification |
| WordCraft | 0.5.0 | Tagged source/docs and portable package verification |

GUI executable version resources matched all twelve targets, and their publisher signatures were valid. No application CLI or GUI was launched for this review; no settings/library migration, model installation, live control, document editing or new runtime smoke test was performed. Version-resource and signature inspection are file metadata checks, not proof of launch, command behavior or output fidelity. Historical runtime checks below retain their original version scope. Verify relevant commands and a bounded copied-file trial when an application task separately authorizes execution.

The final bounded official release check completed on 2026-10-11 at 01:41:32 UTC. Eleven targets matched; PDFCraft 0.6.0 had just become available. After its package and guide refresh, all twelve installed package versions and skill targets matched that release snapshot, with no unknown comparisons. All twelve structural checks and all 35 mocked checker tests passed. The BOM fixture now writes explicit UTF-8 so the same test works under Windows legacy text encodings. This timestamp records a release snapshot, not a promise about future releases.

## Historical six-app Windows checks

On 2026-10-09, bounded Windows x64 CLI trials used the six official portable releases below. Each archive matched both its published checksum file and GitHub asset digest. The CLI and GUI executable files had valid publisher signatures; CLI output and GUI file-version metadata matched the requested versions. GUI applications were not launched by these checks.

| App version | Observed small-fixture behavior |
| --- | --- |
| DesignCraft 0.4.0 | Two source records merged into a new two-page document and PDF, with no reported warnings or overset; the source template hash stayed unchanged. |
| EffectCraft 0.6.0 | CPU backend diagnostic, native project save/reopen, and a 64 × 48 frame render passed. |
| FilmCraft 0.4.0 | Schema/preset reads, native project save/reopen, and a 64 × 48 blank-frame render passed. |
| LightCraft 0.4.0 | Exposure adjustment and 16 × 12 to 8 × 6 resizing passed without changing the source image. Segmentation reported available, with the optional model absent. |
| PhotoCraft 0.5.0 | Explicit layered TIFF retained two layer records; the default TIFF export reopened as one flattened layer. |
| VectorCraft 0.7.0 | SVG, native, PDF, and PNG outputs reported no warnings; native paths and types were preserved, and the PNG was visually checked. |

These trials do not establish GUI launch or library compatibility, GPU behavior, full-video export, model-dependent features, persistent MCP operation, or broad format fidelity. No segmentation model was downloaded or executed. FilmCraft codec/platform claims in the skill remain source-reviewed unless separately exercised on the intended host. Read each skill's version-pinned reference before using a newly documented feature.

## Recorded verification background

Current command references are pinned to the versions and commits in skills.json. The historical checks below apply only to the explicitly named app versions, not automatically to newer skill targets. Eleven apps received bounded Linux x86_64 CLI smoke checks using release archives whose SHA-256 values matched release checksums and GitHub asset digests, on Debian 13 with glibc 2.41. These checks established only the following small-fixture behaviors:

- CADCraft 0.3.0: DXF create/save/reopen/render with geometry, units, and layers preserved
- DeckCraft 0.3.0: PPTX title save/reopen/render
- DesignCraft 0.2.1: editable native text-frame save/reopen/render
- EffectCraft 0.4.0: native project reopen and a small CPU-rendered frame
- FilmCraft 0.2.1: native project reopen and a small PNG frame render
- GridCraft 0.3.0: XLSX formula retention and recalculation after saving again
- LightCraft 0.2.1: exposure/rating persistence and PNG export
- PhotoCraft 0.3.0: two-layer native/PSD save/reopen/edit
- SoundCraft 0.3.0: session reopen and a byte-identical short WAV bounce
- VectorCraft 0.4.0: editable native shapes and SVG path/render parity
- WordCraft 0.3.0: DOCX text retention and rendering

Those checks do not certify every reference example, GUI behavior, GPU rendering, physical audio devices, large-file performance, complex format fidelity, or cross-platform interoperability. LightCraft timestamp metadata was not established as reliable. Availability of source code does not imply that a packaged binary exists for every platform. Recheck package provenance, prerequisites, app version, CLI schemas, and output fidelity on the actual host.

These files do not grant permission to run an untrusted executable, overwrite originals, record audio, install plugins/models, expose a network listener, add persistent access, or send files. Respect the current task's permissions. Do not expose unauthenticated control ports, reuse another session's port, or publish token-file contents.

### PDFCraft 0.4.0

A separate bounded Windows CLI check confirmed the version, enumerated the automation schemas, and inspected and searched text in a synthetic PDF. Its command reference was also checked against the pinned upstream parser and tool schemas.

Those checks do not establish GUI behavior, OCR accuracy, image rendering, form edits, signature validity, or broad format fidelity. OCR execution requires model availability and was not verified by this check. Recheck relevant behavior on the actual document before claiming task completion.

Do not assume one app's checks certify another app or version. Record newly added coverage and its limitations separately.
