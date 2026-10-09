#!/usr/bin/env python3
"""Read-only, unauthenticated GitHub release checks for skills.json.

Python 3.9+, standard library only. Compare the manifest's target versions, not
installed apps. No asset downloads, files written, installs, or automatic retries.
Exit 0: every comparison is known (including updates/ahead); 1: some unknown;
2: invalid/unreadable top-level manifest or command-line arguments.
"""
import sys

sys.dont_write_bytecode = True

import argparse
from dataclasses import dataclass
from functools import total_ordering
import json
from http.client import HTTPException
import math
from pathlib import Path
import re
import socket
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
STATUSES = ("update_available", "current", "ahead", "unknown")
VERSION = re.compile(
    r"[vV]?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)
REPOSITORY = re.compile(
    r"https://github\.com/([A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?)/"
    r"([A-Za-z0-9_.-]{1,100})/?"
)


@total_ordering
@dataclass(frozen=True)
class SemVersion:
    core: Tuple[int, int, int]
    prerelease: Tuple[str, ...] = ()

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, SemVersion):
            return NotImplemented
        if self.core != other.core:
            return self.core < other.core
        if not self.prerelease or not other.prerelease:
            return bool(self.prerelease) and not other.prerelease
        for left, right in zip(self.prerelease, other.prerelease):
            if left == right:
                continue
            if left.isdigit() and right.isdigit():
                return int(left) < int(right)
            if left.isdigit() != right.isdigit():
                return left.isdigit()
            return left < right
        return len(self.prerelease) < len(other.prerelease)


def parse_version(value: Any) -> SemVersion:
    """Parse three-part SemVer with an optional v prefix; ignore build metadata."""
    match = VERSION.fullmatch(value) if isinstance(value, str) and len(value) <= 256 else None
    if not match:
        raise ValueError("Unsupported semantic version")
    prerelease = tuple(match[4].split(".")) if match[4] else ()
    if any(part.isdigit() and len(part) > 1 and part.startswith("0") for part in prerelease):
        raise ValueError("Numeric prerelease identifiers cannot have leading zeroes")
    return SemVersion(tuple(int(match[i]) for i in (1, 2, 3)), prerelease)


def canonical_repository(value: Any) -> str:
    """Allow only plain HTTPS github.com owner/repository URLs, never API input URLs."""
    match = REPOSITORY.fullmatch(value) if isinstance(value, str) else None
    if not match or match[2] in (".", "..") or match[2].endswith(".git"):
        raise ValueError("Repository must be a canonical https://github.com/owner/repository URL")
    return "https://github.com/" + match[1] + "/" + match[2]


class CheckError(Exception):
    def __init__(self, message: str, rate_limited: bool = False):
        super().__init__(message)
        self.rate_limited = rate_limited


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # A moved repository needs explicit manifest review; do not follow it.
        return None


def open_request(request: Request, timeout: float):
    return build_opener(NoRedirects()).open(request, timeout=timeout)


def fetch_release(repository: str, timeout: float) -> Tuple[Dict[str, Any], bool]:
    """One bounded GET to GitHub's designated latest non-draft, non-prerelease release."""
    repository = canonical_repository(repository)
    owner_repo = repository[len("https://github.com/"):]
    request = Request(
        "https://api.github.com/repos/" + owner_repo + "/releases/latest",
        headers={"Accept": "application/vnd.github+json",
                 "User-Agent": "artcraft-skills-update-check/1.0",
                 "X-GitHub-Api-Version": "2022-11-28"},
        method="GET",
    )
    try:
        with open_request(request, timeout) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            exhausted = response.headers.get("X-RateLimit-Remaining") == "0"
    except HTTPError as exc:
        try:
            body = exc.read(8192).decode("utf-8", errors="replace").lower()
        except (OSError, ValueError, HTTPException):
            body = ""
        finally:
            exc.close()
        headers = exc.headers or {}
        limited = exc.code == 429 or (exc.code == 403 and (
            headers.get("X-RateLimit-Remaining") == "0"
            or headers.get("Retry-After") is not None or "rate limit" in body
        ))
        if limited:
            raise CheckError("GitHub rate limit reached; try again later", True) from None
        if exc.code == 404:
            raise CheckError("No accessible stable release (HTTP 404)") from None
        if 300 <= exc.code < 400:
            raise CheckError("GitHub redirected the request; verify the upstream repository") from None
        raise CheckError("GitHub request failed (HTTP {})".format(exc.code)) from None
    except (TimeoutError, socket.timeout):
        raise CheckError("GitHub request timed out") from None
    except URLError as exc:
        if isinstance(exc.reason, (TimeoutError, socket.timeout)):
            raise CheckError("GitHub request timed out") from None
        raise CheckError("GitHub network request failed") from None
    except (OSError, HTTPException):
        raise CheckError("GitHub network request failed") from None
    if len(raw) > MAX_RESPONSE_BYTES:
        raise CheckError("GitHub response exceeded the size limit", exhausted)
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeError):
        raise CheckError("GitHub returned invalid JSON", exhausted) from None
    if not isinstance(payload, dict):
        raise CheckError("GitHub returned an invalid release object", exhausted)
    return payload, exhausted


def asset_details(name: str) -> Optional[Dict[str, str]]:
    """Conservative filename hints, never a claim that archive contents are verified."""
    if not isinstance(name, str) or not name or len(name) > 255:
        return None
    if not name.isprintable() or "/" in name or "\\" in name:
        return None
    lower = name.lower()
    tokens = set(re.split(r"[^a-z0-9]+", lower))
    # Installers can themselves be wrapped in archives. Reject those too.
    excluded = {"setup", "installer", "install", "msi", "msix", "msixbundle", "appx",
                "appxbundle", "dmg", "pkg", "deb", "rpm", "nupkg", "snap", "flatpak",
                "source", "src", "symbols", "debug", "pdb", "checksum", "checksums",
                "sha256", "sha512", "signature", "sdk", "headers", "docs", "documentation"}
    if tokens & excluded or "setup" in lower or "installer" in lower:
        return None
    platform = "unknown"
    if tokens & {"windows", "win", "win32", "win64"}:
        platform = "windows"
    elif tokens & {"macos", "mac", "osx", "darwin"}:
        platform = "macos"
    elif tokens & {"linux", "appimage"}:
        platform = "linux"
    elif "freebsd" in tokens:
        platform = "freebsd"
    architecture = "unknown"
    if tokens & {"universal", "universal2"}:
        architecture = "universal"
    elif tokens & {"aarch64", "arm64"}:
        architecture = "aarch64"
    elif tokens & {"x64", "amd64", "win64"} or "x86_64" in lower or "x86-64" in lower:
        architecture = "x86_64"
    elif tokens & {"i386", "i686", "x86", "win32"}:
        architecture = "x86"
    elif tokens & {"armv7", "armv7l", "armhf"}:
        architecture = "armv7"
    archive = lower.endswith((".zip", ".7z", ".tar.gz", ".tgz", ".tar.xz", ".tar.bz2", ".tar.zst"))
    explicit = "portable" in tokens
    if lower.endswith(".appimage"):
        kind = "appimage"
    elif archive and explicit:
        kind = "portable_archive"
    elif archive and platform != "unknown":
        kind = "archive_candidate"
    elif lower.endswith(".exe") and explicit:
        kind = "portable_executable"
    else:
        return None
    return {"kind": kind, "platform": platform, "architecture": architecture}


def official_asset_url(url: Any, repository: str, tag: str, name: str) -> bool:
    if not isinstance(url, str) or any(ord(char) < 33 or ord(char) > 126 for char in url):
        return False
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    if parts.scheme != "https" or parts.netloc != "github.com" or parts.query or parts.fragment:
        return False
    actual = [unquote(part) for part in parts.path.split("/")]
    owner_repo = repository[len("https://github.com/"):].split("/")
    expected = [""] + owner_repo + ["releases", "download", tag, name]
    return actual == expected


def portable_assets(payload: Dict[str, Any], repository: str, tag: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    assets = payload.get("assets")
    if not isinstance(assets, list):
        return [], ["Asset metadata is unavailable; use the release page"]
    matches = []
    rejected_url = False
    for asset in assets:
        if not isinstance(asset, dict):
            continue
        name = asset.get("name")
        details = asset_details(name)
        if details is None:
            continue
        url = asset.get("browser_download_url")
        if not official_asset_url(url, repository, tag, name):
            rejected_url = True
            continue
        matches.append(dict(name=name, browser_download_url=url, **details))
    notes = ["Some asset links were omitted because they were not canonical upstream release URLs"] if rejected_url else []
    return sorted(matches, key=lambda asset: asset["name"].lower()), notes


def load_manifest(path: Path) -> List[Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except OSError:
        raise ValueError("Cannot read the manifest") from None
    except (ValueError, UnicodeError):
        raise ValueError("Manifest is not valid UTF-8 JSON") from None
    if not isinstance(document, dict) or type(document.get("schema_version")) is not int or document["schema_version"] != 1:
        raise ValueError("Manifest must use schema_version 1")
    rows = document.get("skills")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Manifest skills must be a nonempty array")
    if len(rows) > 100:
        raise ValueError("Manifest exceeds the 100-entry safety limit")
    return rows


def check_updates(rows: List[Any], timeout: float = 10.0) -> Dict[str, Any]:
    results = []
    limited = False
    seen = set()
    for index, row in enumerate(rows, 1):
        result = {"app": "Manifest entry {}".format(index), "target_version": None,
                  "latest_version": None, "status": "unknown", "repository": None,
                  "release_url": None, "portable_assets": [], "notes": [], "error": None}
        results.append(result)
        if not isinstance(row, dict) or not isinstance(row.get("app"), str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9 ]{0,63}", row["app"]):
            result["error"] = "Manifest entry has an invalid app name"
            continue
        result["app"] = row["app"]
        try:
            repository = canonical_repository(row.get("upstream_repository"))
        except ValueError as exc:
            result["error"] = str(exc)
            continue
        result["repository"] = repository
        result["release_url"] = repository + "/releases/latest"
        if repository.lower() in seen:
            result["error"] = "Duplicate upstream repository in manifest; not requested again"
            continue
        seen.add(repository.lower())
        try:
            target = parse_version(row.get("app_version"))
        except ValueError:
            result["error"] = "Manifest target version is not a supported semantic version"
            continue
        result["target_version"] = row["app_version"]
        if limited:
            result["error"] = "Not requested because GitHub's rate limit was reached"
            continue
        try:
            payload, exhausted = fetch_release(repository, timeout)
            limited = exhausted
            if payload.get("draft") is not False or payload.get("prerelease") is not False:
                raise CheckError("GitHub did not return a confirmed stable, published release")
            try:
                latest = parse_version(payload.get("tag_name"))
            except ValueError:
                raise CheckError("Latest release tag is not a supported semantic version") from None
            if latest.prerelease:
                raise CheckError("Latest release tag is a prerelease; no stable comparison was made")
            tag = payload["tag_name"]
            result["latest_version"] = tag
            result["release_url"] = repository + "/releases/tag/" + quote(tag, safe="")
            result["portable_assets"], result["notes"] = portable_assets(payload, repository, tag)
            result["status"] = "update_available" if target < latest else ("ahead" if target > latest else "current")
        except CheckError as exc:
            limited = limited or exc.rate_limited
            result["error"] = str(exc)
    return {"schema_version": 1, "results": results,
            "summary": {status: sum(item["status"] == status for item in results) for status in STATUSES}}


def print_text(report: Dict[str, Any]) -> None:
    if report.get("error"):
        print("Cannot check updates: " + report["error"])
        return
    print("Manifest targets compared with GitHub's latest stable releases:")
    for result in report["results"]:
        label = result["status"].replace("_", " ")
        print("{}: {} (target {}; latest {})".format(
            result["app"], label, result["target_version"] or "unknown", result["latest_version"] or "unknown"))
        if result["error"]:
            print("  " + result["error"])
        if result["release_url"]:
            print("  Release: " + result["release_url"])
        for asset in result["portable_assets"]:
            print("  {} [{}; {}; {}]: {}".format(asset["name"], asset["platform"],
                  asset["architecture"], asset["kind"].replace("_", " "), asset["browser_download_url"]))
        if result["status"] != "unknown" and not result["portable_assets"]:
            print("  No portable asset matched by filename; check the release page")
        for note in result["notes"]:
            print("  " + note)
    print("Summary: " + ", ".join("{} {}".format(report["summary"][status], status.replace("_", " ")) for status in STATUSES))
    print("Asset labels are filename hints; contents and compatibility were not verified. No release assets were downloaded; nothing was installed or changed.")


def bounded_timeout(value: str) -> float:
    try:
        timeout = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError("timeout must be a number between 0 and 60 seconds (exclusive of 0)") from None
    if not math.isfinite(timeout) or not 0 < timeout <= 60:
        raise argparse.ArgumentTypeError("timeout must be greater than 0 and at most 60 seconds")
    return timeout


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--manifest", type=Path, default=ROOT / "skills.json", help="manifest path (default: repository skills.json)")
    parser.add_argument("--timeout", type=bounded_timeout, default=10.0, help="per-request socket timeout in seconds, maximum 60 (default: 10)")
    parser.add_argument("--json", action="store_true", help="emit a machine-readable report instead of text")
    args = parser.parse_args(argv)
    try:
        report = check_updates(load_manifest(args.manifest), args.timeout)
        status = 1 if report["summary"]["unknown"] else 0
    except ValueError as exc:
        report = {"schema_version": 1, "error": str(exc), "results": [],
                  "summary": {status: 0 for status in STATUSES}}
        status = 2
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        print_text(report)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
