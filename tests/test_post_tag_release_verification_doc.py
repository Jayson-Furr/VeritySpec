from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "post-tag-release-verification.md"


class PostTagReleaseVerificationDocTests(unittest.TestCase):
    def test_checklist_is_publicly_linked(self) -> None:
        sources = [
            ROOT / "README.md",
            ROOT / "docs" / "release-checklist.md",
            ROOT / "docs" / "release-integrity.md",
            ROOT / "docs" / "ci.md",
            ROOT / "docs" / "branching.md",
        ]

        for source in sources:
            with self.subTest(source=source.relative_to(ROOT)):
                text = source.read_text(encoding="utf-8")
                self.assertIn("post-tag-release-verification.md", text)

    def test_checklist_preserves_required_evidence_categories(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "Release Workflow Evidence",
            "GitHub Release Asset Evidence",
            "Downloaded Wheel Smoke Test",
            "Public GitHub Tag Install Smoke Test",
            "Milestone And Issue Closure Evidence",
            "Final Repository And Agent Evidence",
            "CI Outage Fallback",
            "Evidence Summary Template",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_checklist_covers_release_asset_and_install_commands(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "gh release view \"$TAG\"",
            "gh release download \"$TAG\"",
            "shasum -a 256",
            "verityspec-${VERSION}-py3-none-any.whl",
            "verityspec-${VERSION}.tar.gz",
            "verityspec @ git+https://github.com/$REPO.git@$TAG",
            "\"$WHEEL_ENV/bin/verity\" pack validate",
            "\"$GITHUB_ENV/bin/verity\" validate examples/basic",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_checklist_preserves_pypi_and_agent_boundaries(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "does not enable PyPI publishing",
            "The PyPI publish job is absent or skipped unless",
            "publish_pypi=true",
            "AGENTS.md has been reread",
            "Do not use this fallback for normal test failures.",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
