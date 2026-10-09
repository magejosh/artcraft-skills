"""Offline tests: python3 -B -m unittest discover -s tests -v."""
import contextlib
from http.client import IncompleteRead
import importlib.util
import io
import json
from pathlib import Path
import socket
import sys
import tempfile
import unittest
from unittest import mock
from urllib.error import HTTPError, URLError
from urllib.parse import quote

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "update_check.py"
SPEC = importlib.util.spec_from_file_location("update_check", MODULE_PATH)
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
SPEC.loader.exec_module(checker)

REPO = "https://github.com/example/cadcraft"
OTHER_REPO = "https://github.com/example/pdfcraft"


def entry(version="1.2.3", repository=REPO, app="CADCraft"):
    return {"app": app, "app_version": version, "upstream_repository": repository}


def release(tag="v1.2.3", assets=None, **extra):
    payload = {"tag_name": tag, "draft": False, "prerelease": False,
               "assets": [] if assets is None else assets}
    payload.update(extra)
    return payload


def asset(name, tag="v1.2.3", repository=REPO, url=None):
    return {"name": name, "browser_download_url": url if url is not None else
            repository + "/releases/download/" + quote(tag, safe="") + "/" + quote(name, safe="")}


class Response:
    def __init__(self, payload=None, raw=None, headers=None):
        self.raw = json.dumps(payload).encode() if raw is None else raw
        self.headers = headers or {}
        self.closed = False
        self.read_sizes = []

    def read(self, size):
        self.read_sizes.append(size)
        return self.raw[:size]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.closed = True


class OfflineTest(unittest.TestCase):
    def setUp(self):
        # A forgotten request mock fails immediately, never contacts the network.
        self.network = mock.patch.object(checker, "open_request", side_effect=AssertionError("Unmocked network request"))
        self.network.start()
        self.addCleanup(self.network.stop)


class VersionTests(OfflineTest):
    def test_numeric_not_lexical_ordering(self):
        self.assertGreater(checker.parse_version("1.10.0"), checker.parse_version("1.9.9"))
        self.assertGreater(checker.parse_version("2.0.0"), checker.parse_version("1.100.100"))
        self.assertGreater(checker.parse_version("0.0.10"), checker.parse_version("0.0.9"))

    def test_prefix_and_build_metadata(self):
        for value in ("v1.2.3", "V1.2.3", "1.2.3+build.001", "v1.2.3+other"):
            with self.subTest(value=value):
                self.assertEqual(checker.parse_version(value), checker.parse_version("1.2.3"))

    def test_semver_prerelease_precedence(self):
        sequence = ["1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.beta", "1.0.0-beta",
                    "1.0.0-beta.2", "1.0.0-beta.11", "1.0.0-rc.1", "1.0.0"]
        versions = [checker.parse_version(value) for value in sequence]
        for left, right in zip(versions, versions[1:]):
            self.assertLess(left, right)
        self.assertEqual(checker.parse_version("1.2.3-rc.1+123"), checker.parse_version("v1.2.3-rc.1+456"))

    def test_invalid_versions(self):
        for value in (None, True, 3, "", "1.2", "release-1.2.3", "01.2.3", "1.02.3", "1.2.03",
                      "1.2.3-01", "1.2.3-rc.01", "1.2.3-", "1.2.3+", "1.2.3+foo..bar", " 1.2.3", "1.2.3\n", "1.2.3/extra"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                checker.parse_version(value)


class ComparisonTests(OfflineTest):
    def test_newer_equal_older_targets(self):
        for target, latest, expected in (("1.2.3", "v1.3.0", "update_available"),
                                         ("1.2.3", "v1.2.3+build", "current"),
                                         ("1.3.0", "v1.2.3", "ahead"),
                                         ("1.9.0", "v1.10.0", "update_available"),
                                         ("1.2.3-rc.1", "v1.2.3", "update_available")):
            with self.subTest(target=target, latest=latest), mock.patch.object(checker, "fetch_release", return_value=(release(latest), False)):
                report = checker.check_updates([entry(target)])
                row = report["results"][0]
                self.assertEqual(row["status"], expected)
                self.assertIsNone(row["error"])
                self.assertEqual(row["latest_version"], latest)
                self.assertEqual(row["release_url"], REPO + "/releases/tag/" + quote(latest, safe=""))
                self.assertEqual(report["summary"][expected], 1)

    def test_invalid_unstable_or_draft_release_is_unknown(self):
        payloads = [release("release-next"), release("1.2.3-rc.1"), release(prerelease=True),
                    release(draft=True), release(prerelease=None), {"tag_name": "v1.2.3"}]
        for payload in payloads:
            with self.subTest(payload=payload), mock.patch.object(checker, "fetch_release", return_value=(payload, False)):
                result = checker.check_updates([entry()])["results"][0]
                self.assertEqual(result["status"], "unknown")
                self.assertTrue(result["error"])
                self.assertEqual(result["release_url"], REPO + "/releases/latest")

    def test_partial_failure_keeps_both_successes(self):
        rows = [entry(), entry(repository=OTHER_REPO, app="PDFCraft"),
                entry(repository="https://github.com/example/deckcraft", app="DeckCraft")]
        with mock.patch.object(checker, "fetch_release", side_effect=[(release("v1.3.0"), False),
                              checker.CheckError("GitHub request timed out"), (release(), False)]) as fetch:
            report = checker.check_updates(rows)
        self.assertEqual([r["status"] for r in report["results"]], ["update_available", "unknown", "current"])
        self.assertEqual(fetch.call_count, 3)
        self.assertEqual(report["summary"]["unknown"], 1)

    def test_rate_limit_does_not_hammer_remaining_repositories(self):
        with mock.patch.object(checker, "fetch_release", side_effect=checker.CheckError("Rate limited", True)) as fetch:
            report = checker.check_updates([entry(), entry(repository=OTHER_REPO)])
        self.assertEqual(fetch.call_count, 1)
        self.assertEqual(report["summary"]["unknown"], 2)
        self.assertIn("Not requested", report["results"][1]["error"])

    def test_successful_last_quota_response_is_kept(self):
        with mock.patch.object(checker, "fetch_release", return_value=(release(), True)) as fetch:
            report = checker.check_updates([entry(), entry(repository=OTHER_REPO)])
        self.assertEqual(fetch.call_count, 1)
        self.assertEqual([r["status"] for r in report["results"]], ["current", "unknown"])

    def test_valid_version_missing_asset_metadata_keeps_comparison(self):
        payload = release()
        del payload["assets"]
        with mock.patch.object(checker, "fetch_release", return_value=(payload, False)):
            result = checker.check_updates([entry()])["results"][0]
        self.assertEqual(result["status"], "current")
        self.assertIn("unavailable", result["notes"][0])


class RequestTests(OfflineTest):
    def test_only_bounded_get_metadata_without_authentication(self):
        response = Response(release())
        with mock.patch.object(checker, "open_request", return_value=response) as opened:
            payload, exhausted = checker.fetch_release(REPO, 3.5)
        request, timeout = opened.call_args.args
        self.assertEqual(request.full_url, "https://api.github.com/repos/example/cadcraft/releases/latest")
        self.assertEqual(request.get_method(), "GET")
        self.assertIsNone(request.data)
        self.assertNotIn("authorization", {key.lower() for key in request.headers})
        self.assertEqual(timeout, 3.5)
        self.assertEqual(response.read_sizes, [checker.MAX_RESPONSE_BYTES + 1])
        self.assertTrue(response.closed)
        self.assertFalse(exhausted)
        self.assertEqual(payload, release())

    def test_redirects_are_not_followed(self):
        self.assertIsNone(checker.NoRedirects().redirect_request(None, None, 302, "Found", {}, "https://example.org"))

    def test_http_errors_and_rate_limits(self):
        cases = [(404, {}, b"", False, "404"), (500, {}, b"", False, "500"),
                 (301, {}, b"", False, "redirected"), (403, {}, b"Forbidden", False, "403"),
                 (403, {"X-RateLimit-Remaining": "0"}, b"", True, "rate limit"),
                 (403, {"Retry-After": "60"}, b"", True, "rate limit"),
                 (403, {}, b'{"message":"secondary rate limit"}', True, "rate limit"),
                 (429, {}, b"", True, "rate limit")]
        for code, headers, body, limited, message in cases:
            stream = io.BytesIO(body)
            error = HTTPError("https://api.github.com/", code, "error", headers, stream)
            with self.subTest(code=code, headers=headers), mock.patch.object(checker, "open_request", side_effect=error):
                with self.assertRaises(checker.CheckError) as raised:
                    checker.fetch_release(REPO, 1)
            self.assertEqual(raised.exception.rate_limited, limited)
            self.assertIn(message, str(raised.exception))
            self.assertTrue(stream.closed)

    def test_network_and_read_errors(self):
        for error in (socket.timeout(), TimeoutError(), URLError(socket.timeout()),
                      URLError("network details must not be printed"), OSError("private detail"), IncompleteRead(b"partial")):
            with self.subTest(error=type(error)), mock.patch.object(checker, "open_request", side_effect=error):
                with self.assertRaises(checker.CheckError) as raised:
                    checker.fetch_release(REPO, 1)
                self.assertNotIn("private detail", str(raised.exception))
                self.assertNotIn("network details", str(raised.exception))

    def test_truncated_rate_limit_body_stops_remaining_requests(self):
        stream = mock.Mock()
        stream.read.side_effect = IncompleteRead(b"truncated rate-limit response")
        error = HTTPError("https://api.github.com/", 429, "Too Many Requests", {}, stream)
        with mock.patch.object(checker, "open_request", side_effect=error) as opened:
            report = checker.check_updates([entry(), entry(repository=OTHER_REPO)])
        self.assertEqual(opened.call_count, 1)
        self.assertEqual(report["summary"]["unknown"], 2)
        self.assertIn("rate limit", report["results"][0]["error"])
        self.assertIn("Not requested", report["results"][1]["error"])
        stream.close.assert_called_once()

    def test_truncated_success_body_preserves_other_results(self):
        broken = Response(release())
        broken.read = mock.Mock(side_effect=IncompleteRead(b"truncated JSON"))
        responses = [Response(release("v1.3.0")), broken, Response(release())]
        rows = [entry(), entry(repository=OTHER_REPO, app="PDFCraft"),
                entry(repository="https://github.com/example/deckcraft", app="DeckCraft")]
        with mock.patch.object(checker, "open_request", side_effect=responses) as opened:
            report = checker.check_updates(rows)
        self.assertEqual(opened.call_count, 3)
        self.assertEqual([row["status"] for row in report["results"]],
                         ["update_available", "unknown", "current"])
        self.assertIn("network request failed", report["results"][1]["error"])
        self.assertTrue(all(response.closed for response in responses))

    def test_bad_json_and_response_shape(self):
        for raw in (b"not json", b"\xff", b"[]", b"null"):
            with self.subTest(raw=raw), mock.patch.object(checker, "open_request", return_value=Response(raw=raw)):
                with self.assertRaises(checker.CheckError):
                    checker.fetch_release(REPO, 1)

    def test_response_size_limit(self):
        with mock.patch.object(checker, "open_request", return_value=Response(raw=b" " * (checker.MAX_RESPONSE_BYTES + 1))):
            with self.assertRaisesRegex(checker.CheckError, "size limit"):
                checker.fetch_release(REPO, 1)

    def test_remaining_quota_detected_even_if_json_is_invalid(self):
        with mock.patch.object(checker, "open_request", return_value=Response(raw=b"bad", headers={"X-RateLimit-Remaining": "0"})):
            with self.assertRaises(checker.CheckError) as raised:
                checker.fetch_release(REPO, 1)
        self.assertTrue(raised.exception.rate_limited)


class ManifestTests(OfflineTest):
    def test_canonical_repositories(self):
        self.assertEqual(checker.canonical_repository(REPO + "/"), REPO)
        for value in (None, "http://github.com/example/app", "https://api.github.com/repos/example/app",
                      "https://github.com.evil.example/example/app", "https://github.com@example.org/example/app",
                      "https://example@github.com/example/app", REPO + "?token=secret", REPO + "#tag",
                      REPO + "/releases", "https://github.com:443/example/app", "https://github.com/example/..",
                      "https://github.com/example/%2e%2e", "https://github.com/example/app.git",
                      "https://github.com/example\\name/app", REPO + "\n"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                checker.canonical_repository(value)

    def test_invalid_rows_make_no_requests(self):
        rows = [None, {}, entry(version="invalid"), entry(repository="https://example.org/app"), entry(app="bad\nname")]
        with mock.patch.object(checker, "fetch_release") as fetch:
            report = checker.check_updates(rows)
        fetch.assert_not_called()
        self.assertEqual(report["summary"]["unknown"], len(rows))
        self.assertTrue(all(result["error"] for result in report["results"]))

    def test_invalid_row_does_not_block_valid_row(self):
        with mock.patch.object(checker, "fetch_release", return_value=(release(), False)) as fetch:
            report = checker.check_updates([None, entry()])
        self.assertEqual(fetch.call_count, 1)
        self.assertEqual([result["status"] for result in report["results"]], ["unknown", "current"])

    def test_duplicate_repositories_not_repeated(self):
        with mock.patch.object(checker, "fetch_release", return_value=(release(), False)) as fetch:
            report = checker.check_updates([entry(), entry(repository=REPO + "/")])
        self.assertEqual(fetch.call_count, 1)
        self.assertEqual(report["results"][1]["status"], "unknown")

    def test_bad_top_level_manifest(self):
        cases = ["bad", "\ufeff{}", "[]", "{}", '{"schema_version":true,"skills":[{}]}',
                 '{"schema_version":2,"skills":[{}]}', '{"schema_version":1,"skills":[]}',
                 '{"schema_version":1,"skills":{}}']
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "skills.json"
            for contents in cases:
                path.write_text(contents)
                with self.subTest(contents=contents), self.assertRaises(ValueError):
                    checker.load_manifest(path)
            path.write_bytes(b"\xff")
            with self.assertRaises(ValueError):
                checker.load_manifest(path)
            with self.assertRaises(ValueError):
                checker.load_manifest(Path(directory) / "missing.json")
            path.write_text(json.dumps({"schema_version": 1, "skills": [{}] * 101}))
            with self.assertRaises(ValueError):
                checker.load_manifest(path)

    def test_real_manifest_has_expected_twelve_apps_and_pdfcraft(self):
        rows = checker.load_manifest(MODULE_PATH.parents[1] / "skills.json")
        expected = {"CADCraft", "DeckCraft", "DesignCraft", "EffectCraft", "FilmCraft", "GridCraft",
                    "LightCraft", "PDFCraft", "PhotoCraft", "SoundCraft", "VectorCraft", "WordCraft"}
        self.assertEqual(len(rows), 12)
        self.assertEqual({row["app"] for row in rows}, expected)
        self.assertEqual(next(row["app_version"] for row in rows if row["app"] == "PDFCraft"), "0.4.0")
        for row in rows:
            checker.canonical_repository(row["upstream_repository"])
            checker.parse_version(row["app_version"])


class AssetTests(OfflineTest):
    def test_portable_asset_classification(self):
        cases = [("App-1.2.3-windows-x64-portable.zip", "portable_archive", "windows", "x86_64"),
                 ("App-linux-aarch64.tar.gz", "archive_candidate", "linux", "aarch64"),
                 ("App-linux-x86_64.AppImage", "appimage", "linux", "x86_64"),
                 ("App-macos-universal2.zip", "archive_candidate", "macos", "universal"),
                 ("App-darwin-arm64.tar.xz", "archive_candidate", "macos", "aarch64"),
                 ("App-win32-portable.exe", "portable_executable", "windows", "x86"),
                 ("App-linux-armv7l.tgz", "archive_candidate", "linux", "armv7"),
                 ("App-freebsd-x86_64.tar.gz", "archive_candidate", "freebsd", "x86_64"),
                 ("App-portable.7z", "portable_archive", "unknown", "unknown")]
        for name, kind, platform, architecture in cases:
            with self.subTest(name=name):
                self.assertEqual(checker.asset_details(name), {"kind": kind, "platform": platform, "architecture": architecture})

    def test_installers_sources_and_unclassified_assets_excluded(self):
        names = ["AppSetup.exe", "App-windows-x64.msi", "App-portable-setup.zip", "AppInstaller-windows.zip",
                 "App-windows-installer.zip", "App-macos.dmg", "App-macos.pkg", "App-linux.deb",
                 "App-linux.rpm", "App-windows.msix.zip", "App-windows-x64.exe", "App-source-windows.zip",
                 "App-linux-debug.tar.gz", "App-linux-sdk.zip", "App-linux.AppImage.sha256", "source.zip",
                 "App.zip", "App-windows.zip.sha256", "../App-windows.zip", "App\nwindows.zip", "App\u202ewindows.zip", None, 5]
        for name in names:
            with self.subTest(name=name):
                self.assertIsNone(checker.asset_details(name))

    def test_only_official_asset_urls_are_returned(self):
        name = "App-windows-x64.zip"
        assets = [asset(name), asset("Other-linux.zip", url="https://example.org/app.zip"),
                  asset("Wrong-linux.zip", repository=OTHER_REPO), {"name": "NoURL-linux.zip"}, None]
        matches, notes = checker.portable_assets(release(assets=assets), REPO, "v1.2.3")
        self.assertEqual([match["name"] for match in matches], [name])
        self.assertEqual(matches[0]["browser_download_url"], assets[0]["browser_download_url"])
        self.assertTrue(notes)

    def test_unsafe_asset_urls_are_rejected(self):
        name = "App-windows-x64.zip"
        good = asset(name)["browser_download_url"]
        for url in (good.replace("https:", "http:"), good + "?key=secret", good + "#fragment",
                    good.replace("github.com", "github.com.evil.example"),
                    good.replace("github.com", "name@github.com"),
                    good.replace("v1.2.3", "v1.2.4"), good + "\n", "https://[invalid"):
            with self.subTest(url=url):
                self.assertFalse(checker.official_asset_url(url, REPO, "v1.2.3", name))

    def test_encoded_tag_and_filename(self):
        tag = "v1.2.3+build"
        name = "App windows x64 portable.zip"
        self.assertTrue(checker.official_asset_url(asset(name, tag=tag)["browser_download_url"], REPO, tag, name))

    def test_no_portable_match_preserves_full_release_link(self):
        with mock.patch.object(checker, "fetch_release", return_value=(release(assets=[asset("AppSetup.exe")]), False)):
            result = checker.check_updates([entry()])["results"][0]
        self.assertEqual(result["portable_assets"], [])
        self.assertEqual(result["release_url"], REPO + "/releases/tag/v1.2.3")


class CommandLineTests(OfflineTest):
    def test_json_output_exit_policy_and_no_file_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "skills.json"
            raw = json.dumps({"schema_version": 1, "skills": [entry()]})
            path.write_text(raw)
            before = {item.name: item.read_bytes() for item in root.iterdir()}
            cases = [(release("v1.3.0"), 0, "update_available"), (release("v1.0.0"), 0, "ahead"),
                     (release(), 0, "current"), (release("not-semver"), 1, "unknown")]
            for payload, status, expected in cases:
                response = Response(payload)
                stdout = io.StringIO()
                with self.subTest(expected=expected), mock.patch.object(checker, "open_request", return_value=response) as opened, contextlib.redirect_stdout(stdout):
                    result = checker.main(["--manifest", str(path), "--json", "--timeout", "2"])
                self.assertEqual(result, status)
                report = json.loads(stdout.getvalue())
                self.assertEqual(report["results"][0]["status"], expected)
                self.assertEqual(opened.call_count, 1)
                self.assertTrue(opened.call_args.args[0].full_url.endswith("/releases/latest"))
            self.assertEqual(before, {item.name: item.read_bytes() for item in root.iterdir()})

    def test_invalid_manifest_json_output_exit_two_without_network(self):
        stdout = io.StringIO()
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(stdout):
            result = checker.main(["--manifest", str(Path(directory) / "missing.json"), "--json"])
        self.assertEqual(result, 2)
        report = json.loads(stdout.getvalue())
        self.assertEqual(report["results"], [])
        self.assertIn("Cannot read", report["error"])

    def test_default_text_explains_unknown_and_asset_limits(self):
        with mock.patch.object(checker, "fetch_release", side_effect=checker.CheckError("GitHub request timed out")):
            report = checker.check_updates([entry()])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            checker.print_text(report)
        self.assertIn("CADCraft: unknown", stdout.getvalue())
        self.assertIn("timed out", stdout.getvalue())
        self.assertIn("filename hints", stdout.getvalue())
        self.assertIn("No release assets were downloaded", stdout.getvalue())

    def test_timeout_bounds_and_invalid_options(self):
        for value in ("0", "-1", "61", "nan", "inf", "nonsense"):
            with self.subTest(value=value), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
                checker.main(["--timeout", value])
            self.assertEqual(raised.exception.code, 2)
        self.assertEqual(checker.bounded_timeout("0.5"), 0.5)
        self.assertEqual(checker.bounded_timeout("60"), 60)


if __name__ == "__main__":
    unittest.main()
