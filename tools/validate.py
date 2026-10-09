#!/usr/bin/env python3
"""Read-only structural checks for the portable skill template package."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "cadcraft": "0.3.0", "deckcraft": "0.3.0", "designcraft": "0.2.1",
    "effectcraft": "0.4.0", "filmcraft": "0.2.1", "gridcraft": "0.3.0",
    "lightcraft": "0.2.1", "pdfcraft": "0.4.0", "photocraft": "0.3.0",
    "soundcraft": "0.3.0", "vectorcraft": "0.4.0", "wordcraft": "0.3.0",
}


def validate():
    errors = []
    manifest = json.loads((ROOT / "skills.json").read_text(encoding="utf-8"))
    rows = manifest["skills"]
    expected_names = set(EXPECTED)
    names = [row["skill"] for row in rows]
    if manifest.get("schema_version") != 1:
        errors.append("Unsupported manifest schema version")
    if len(rows) != len(EXPECTED) or set(names) != expected_names or len(set(names)) != len(names):
        errors.append("Manifest must contain each of the expected skills exactly once")
    actual = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
    if actual != expected_names:
        errors.append("Skill folders do not match the expected set")
    for row in rows:
        name = row["skill"]
        app = name
        if app not in EXPECTED:
            continue
        version = EXPECTED[app]
        repo = "https://github.com/storytold/" + app
        folder = ROOT / "skills" / name
        skill_path = folder / "SKILL.md"
        ref_path = folder / "references" / "cli-and-formats.md"
        if not skill_path.is_file() or not ref_path.is_file():
            errors.append(name + ": missing skill or reference")
            continue
        text = skill_path.read_text(encoding="utf-8")
        ref = ref_path.read_text(encoding="utf-8")
        match = re.match(r'\A---\nname: ([a-z0-9-]+)\ndescription: "([^\n]+)"\n---\n', text)
        if not match or match[1] != name or len(name) >= 64:
            errors.append(name + ": invalid frontmatter or name")
        if match and (len(match[2]) > 1024 or len(match[2]) < 20):
            errors.append(name + ": unexpected description length")
        if row["app_version"] != version or row["source_tag"] != "v" + version:
            errors.append(name + ": inconsistent version metadata")
        if row["upstream_repository"] != repo:
            errors.append(name + ": unexpected application repository")
        sha = row["source_commit"]
        if not re.fullmatch(r"[a-f0-9]{40}", sha) or sha not in ref:
            errors.append(name + ": missing or invalid source commit")
        notice = (
            f'Target app version: {row["app"]} {version}. '
            f'If the installed or globally available {row["app"]} version is newer, '
            f'check that application’s official repository documentation at {repo} '
            'before relying on these commands.'
        )
        if text.rstrip().splitlines()[-1] != notice:
            errors.append(name + ": final version/documentation notice is missing or changed")
        if f'Written for {row["app"]} {version}.' not in text:
            errors.append(name + ": missing body target version")
        if f'# {row["app"]} {version}: CLI and format reference' not in ref:
            errors.append(name + ": inconsistent reference title")
        for document, contents in [(skill_path, text), (ref_path, ref)]:
            if not contents.endswith("\n") or "\r" in contents:
                errors.append(str(document.relative_to(ROOT)) + ": inconsistent line endings")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", contents):
                if target.startswith("https://"):
                    if target.startswith("https://github.com/storytold/") and target != repo:
                        if not target.startswith(repo + "/"):
                            errors.append(name + ": cross-app source link " + target)
                        if "/blob/" in target and f"/blob/v{version}/" not in target:
                            errors.append(name + ": unpinned source link " + target)
                    continue
                if target.startswith("#"):
                    continue
                resolved = (document.parent / target).resolve()
                if ROOT not in resolved.parents or not resolved.is_file():
                    errors.append(name + ": invalid relative reference " + target)
            if re.search(r"\b(?:TODO|TBD|FIXME)\b", contents):
                errors.append(name + ": unfinished scaffold marker")
    return errors


if __name__ == "__main__":
    try:
        errors = validate()
    except (KeyError, ValueError, OSError) as exc:
        print("Validation error:", exc, file=sys.stderr)
        raise SystemExit(1)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"PASS: {len(EXPECTED)} skills; frontmatter, versions, final notices, references, and source pins")
