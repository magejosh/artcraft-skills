# Repository guidance for agents and contributors

## Purpose and structure

Maintain portable, app-specific skills that help an assistant use the named application correctly. Keep the root README focused on what the collection offers and how a person can use it. Put repository-maintenance instructions here and app-operation details inside each skill.

- `skills/<app>/SKILL.md`: entrypoint with the app-only lowercase skill name and a specific trigger description.
- `skills/<app>/references/cli-and-formats.md`: exact command grammar, format limitations, and version-pinned sources.
- `skills.json`: app names, target versions, upstream repositories, tags, and source commits.

## Adding or changing a skill

1. Confirm the application identity, official repository, target app version, and matching source tag/commit. Distinguish package metadata, source/documentation review, and observed runtime behavior. Never promote a source-only finding to a tested claim.
2. Use an app-only folder/frontmatter name, for example `cadcraft`. Keep each skill independently usable with its references; do not depend on unrelated sibling skills or repository-only instructions for essential app behavior.
3. Discover actual command grammar from that version's documentation, source, or available help/schema output. Do not transfer flags or page-index conventions between apps.
4. Use portable executable discovery or a per-app environment variable. Use synthetic relative example filenames; never embed a contributor's installation paths, account or device identifiers, private project details, credentials, task links, or local history.
5. Update the human-facing skill table, `skills.json`, and the validator's expected app/version mapping when adding or changing an app. Preserve unrelated content and any user edits.
6. Preserve editable outputs and describe meaningful visual/data checks. Make overwrite, live-control, batch, and persistent-state side effects clear without implying that a skill grants permission for them.
7. End each SKILL.md with the required notice below, substituting the display name, target version, and the individual application's official repository URL. Keep it as the last nonempty line; do not point the notice at this collection's repository.

```text
Target app version: APP VERSION. If the installed or globally available APP version is newer, check that application’s official repository documentation at APP_REPOSITORY_URL before relying on these commands.
```

Use the same target version in the skill, reference title, manifest, source links, and expected-version mapping.

## App update checks

For requested upstream update checks, use `tools/update_check.py` and the workflow in TESTING.md. Compare against the versions in `skills.json`; do not describe the result as an installed-app inventory. Report unknown or failed checks explicitly. Checking releases does not authorize downloads, installation, or changing version pins.

When a portable app update is requested, extract the approved new version alongside the existing folder and leave the old copy for the user to remove. Review changed app documentation before updating its skill's version and source pins.

## Testing

Read [TESTING.md](TESTING.md) for established checks and testing workflows before inventing new ones.
