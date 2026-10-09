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

On 2026-10-09, all 35 mocked checker tests and the 12-skill structural checks passed. A bounded live metadata run covered all twelve upstream repositories. One initial CADCraft timeout was correctly reported as unknown; a separate targeted retry succeeded. The completed check found six newer stable releases and six matching targets, with no unresolved comparisons. No release assets were downloaded and no apps or skill version pins were changed by the check. Rerun the checker for current release information; this record is not a promise that those statuses remain current.

### A requested portable app update

1. Run the read-only check and report the target version, newer release, relevant portable assets, and any unknown checks.
2. Wait for a request to update the app; the check alone does not authorize downloading or installing it.
3. Verify the selected official release, platform/architecture, checksum or signature information, and any new prerequisites.
4. Download and extract the authorized portable release into a separate versioned folder alongside the existing app. Keep the old copy for the user to remove; do not overwrite it or change system-wide defaults incidentally.
5. Run a bounded version/help/schema check and a small copied-file trial suited to the app. Read the changed official docs before updating the skill's target version/source pins, then rerun structural checks and relevant tests.

## Recorded verification background

Command references were checked against the exact upstream versions and commits in skills.json. The eleven app guides listed below have bounded Linux x86_64 CLI smoke coverage using release archives whose SHA-256 values matched release checksums and GitHub asset digests, on Debian 13 with glibc 2.41. These checks established only the following small-fixture behaviors:

- CADCraft: DXF create/save/reopen/render with geometry, units, and layers preserved
- DeckCraft: PPTX title save/reopen/render
- DesignCraft: editable native text-frame save/reopen/render
- EffectCraft: native project reopen and a small CPU-rendered frame
- FilmCraft: native project reopen and a small PNG frame render
- GridCraft: XLSX formula retention and recalculation after saving again
- LightCraft: exposure/rating persistence and PNG export
- PhotoCraft: two-layer native/PSD save/reopen/edit
- SoundCraft: session reopen and a byte-identical short WAV bounce
- VectorCraft: editable native shapes and SVG path/render parity
- WordCraft: DOCX text retention and rendering

Those checks do not certify every reference example, GUI behavior, GPU rendering, physical audio devices, large-file performance, complex format fidelity, or cross-platform interoperability. LightCraft timestamp metadata was not established as reliable. Availability of source code does not imply that a packaged binary exists for every platform. Recheck package provenance, prerequisites, app version, CLI schemas, and output fidelity on the actual host.

These files do not grant permission to run an untrusted executable, overwrite originals, record audio, install plugins/models, expose a network listener, add persistent access, or send files. Respect the current task's permissions. Do not expose unauthenticated control ports, reuse another session's port, or publish token-file contents.

### PDFCraft 0.4.0

A separate bounded Windows CLI check confirmed the version, enumerated the automation schemas, and inspected and searched text in a synthetic PDF. Its command reference was also checked against the pinned upstream parser and tool schemas.

Those checks do not establish GUI behavior, OCR accuracy, image rendering, form edits, signature validity, or broad format fidelity. OCR execution requires model availability and was not verified by this check. Recheck relevant behavior on the actual document before claiming task completion.

Do not assume one app's checks certify another app or version. Record newly added coverage and its limitations separately.
