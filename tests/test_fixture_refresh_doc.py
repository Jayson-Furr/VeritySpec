from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "fixture-refresh.md"


class FixtureRefreshDocTests(unittest.TestCase):
    def test_fixture_refresh_guide_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        generator_docs = (ROOT / "docs" / "generators.md").read_text(encoding="utf-8")
        release_checklist = (ROOT / "docs" / "release-checklist.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/fixture-refresh.md", readme)
        self.assertIn("fixture refresh guide", generator_docs)
        self.assertIn("fixture refresh guidance", release_checklist)

    def test_fixture_refresh_guide_defines_deterministic_refresh_practice(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "golden fixtures under `tests/golden`",
            "deterministic timestamps",
            "`--generated-at`",
            "2026-01-02T03:04:05Z",
            "intentional output drift",
            "python -m json.tool",
            "release-version fixture updates",
            "No automatic fixture rewrite command",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_fixture_refresh_guide_lists_current_golden_outputs(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "security-report examples/security",
            "observability-report examples/observability",
            "accessibility-report examples/accessibility",
            "compliance-matrix examples/compliance",
            "deployment-report examples/deployment",
            "evidence-report examples/evidence",
            "coverage-dashboard tests/fixtures/cross_pack_coverage",
            "pack-capability-index tests/fixtures/custom_pack_workspace",
            "product-impact tests/fixtures/product_impact/baseline",
            "issue-code-catalog",
            "openapi tests/fixtures/generator_maturity",
            "typescript tests/fixtures/generator_maturity",
            "python-models tests/fixtures/generator_maturity",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_fixture_refresh_guide_preserves_release_integrity_boundary(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "tests/test_release_integrity.py",
            "examples/evidence/records/records.json",
            "tests/golden/evidence_report/evidence_report.json",
            "tests/fixtures/cross_pack_coverage/records/all.json",
            "If it fails, update the release surface it names instead of weakening the test.",
            "propose a follow-up organization-patterns write-back",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()

