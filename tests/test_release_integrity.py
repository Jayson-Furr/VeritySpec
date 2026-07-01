from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from verityspec import __version__


ROOT = Path(__file__).resolve().parents[1]
CURRENT_VERSION = __version__
CURRENT_TAG = f"v{CURRENT_VERSION}"
CURRENT_RELEASE_NOTES = ROOT / "docs" / f"release-notes-{CURRENT_TAG}.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def pyproject_version() -> str:
    text = read(ROOT / "pyproject.toml")
    match = re.search(r'^version = "([^"]+)"$', text, flags=re.MULTILINE)
    if not match:
        raise AssertionError("pyproject.toml must declare a project version")
    return match.group(1)


class ReleaseIntegrityTests(unittest.TestCase):
    def test_package_version_sources_match(self) -> None:
        self.assertEqual(CURRENT_VERSION, pyproject_version())

    def test_readme_current_release_surfaces_match_package_version(self) -> None:
        text = read(ROOT / "README.md")

        expected = [
            f"badge/release-{CURRENT_TAG}-blue",
            f"releases/tag/{CURRENT_TAG}",
            f"Latest release: `{CURRENT_TAG}`",
            f"git@{CURRENT_TAG}",
            f"VeritySpec package `{CURRENT_TAG}` supports workspace formats",
            f"[{CURRENT_TAG} release notes](docs/release-notes-{CURRENT_TAG}.md)",
        ]
        for phrase in expected:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_changelog_and_release_notes_match_package_version(self) -> None:
        changelog = read(ROOT / "CHANGELOG.md")
        self.assertIn(f"## {CURRENT_VERSION}", changelog)
        self.assertTrue(CURRENT_RELEASE_NOTES.exists(), f"{CURRENT_RELEASE_NOTES.relative_to(ROOT)} must exist")

        release_notes = read(CURRENT_RELEASE_NOTES)
        self.assertIn(f"# VeritySpec {CURRENT_TAG} Release Notes", release_notes)
        self.assertIn(f"git@{CURRENT_TAG}", release_notes)

    def test_release_docs_and_downstream_pins_match_package_version(self) -> None:
        files = [
            ROOT / ".github" / "workflows" / "product-contract.yml",
            ROOT / "docs" / "downstream-ci.md",
            ROOT / "docs" / "pypi.md",
            ROOT / "docs" / "release-checklist.md",
            ROOT / "templates" / "github-actions" / "product-contract-direct.yml",
            ROOT / "templates" / "github-actions" / "product-contract-monorepo.yml",
            ROOT / "templates" / "github-actions" / "product-contract-profiles.yml",
            ROOT / "templates" / "github-actions" / "product-contract-reusable.yml",
            ROOT / "templates" / "github-actions" / "product-contract-with-local-packs.yml",
        ]

        for path in files:
            with self.subTest(path=path.relative_to(ROOT)):
                text = read(path)
                self.assertIn(CURRENT_TAG, text)

        checklist = read(ROOT / "docs" / "release-checklist.md")
        self.assertIn(f"VERSION={CURRENT_TAG}", checklist)

    def test_evidence_fixtures_match_package_version(self) -> None:
        evidence_records = json.loads(read(ROOT / "examples" / "evidence" / "records" / "records.json"))
        evidence_report = json.loads(read(ROOT / "tests" / "golden" / "evidence_report" / "evidence_report.json"))
        coverage_records = json.loads(read(ROOT / "tests" / "fixtures" / "cross_pack_coverage" / "records" / "all.json"))

        expected_wheel = f"dist/verityspec-{CURRENT_VERSION}-py3-none-any.whl"

        evidence_builds = [
            record
            for record in evidence_records.get("records", [])
            if record.get("kind") == "evidence.build" and record.get("id") == "evidence.build.release_wheel"
        ]
        self.assertEqual(1, len(evidence_builds))
        self.assertEqual(expected_wheel, evidence_builds[0].get("artifactPath"))
        self.assertEqual(CURRENT_VERSION, evidence_builds[0].get("buildVersion"))

        report_uris = {item.get("uri") for item in evidence_report.get("evidence", [])}
        self.assertIn(expected_wheel, report_uris)

        coverage_builds = [
            record
            for record in coverage_records.get("records", [])
            if record.get("kind") == "evidence.build" and record.get("id") == "evidence.build.coverage_wheel"
        ]
        self.assertEqual(1, len(coverage_builds))
        self.assertEqual(CURRENT_VERSION, coverage_builds[0].get("buildVersion"))


if __name__ == "__main__":
    unittest.main()
