from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "golden-fixture-refresh-automation-plan.md"


class GoldenFixtureRefreshAutomationPlanDocTests(unittest.TestCase):
    def test_golden_fixture_refresh_automation_plan_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        fixture_refresh = (ROOT / "docs" / "fixture-refresh.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/golden-fixture-refresh-automation-plan.md", readme)
        self.assertIn("golden-fixture-refresh-automation-plan.md", fixture_refresh)

    def test_golden_fixture_refresh_automation_plan_preserves_scope_boundary(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "does not add CLI commands, schemas, generators, readiness gates",
            "No automatic fixture rewrite command",
            "verity fixtures refresh",
            "--dry-run",
            "--generator security-report",
            "--golden tests/golden/security_report/security_report.json",
            "--generated-at 2026-01-02T03:04:05Z",
            "Acceptance Gates For Implementation",
            "Non-Goals And Non-Claims",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_golden_fixture_refresh_automation_plan_names_planned_contract_sections(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            '"type": "golden_fixture_refresh_plan"',
            '"schemaVersion": "0.1.0"',
            '"mode": "dry_run"',
            '"allowlist"',
            '"inputs": []',
            '"generatedOutputs": []',
            '"fixtureComparisons": []',
            '"placeholderPreservation": []',
            '"diffSummary": {}',
            '"approvalGates": []',
            '"blockedRewrites": []',
            '"claimBoundaries": []',
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_golden_fixture_refresh_automation_plan_names_planned_safety_rules(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "generator allowlists",
            "placeholder preservation",
            "maintainer approval gates",
            "broad all-fixture refreshes",
            "private path leakage",
            "focused golden tests run",
            "changed fixture paths match the allowlist",
            "no default rewrite mode",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_golden_fixture_refresh_automation_plan_names_planned_fixtures_and_non_claims(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "tests/fixtures/fixture_refresh/basic-dry-run",
            "tests/fixtures/fixture_refresh/placeholder-preservation",
            "tests/fixtures/fixture_refresh/blocked-rewrite",
            "tests/fixtures/fixture_refresh/allowlist",
            "golden JSON fixture",
            "commercial, legal,",
            "platform-certification, pricing-approval,",
            "support-SLA, security-certification, or production-readiness guarantees",
            "does not prove external",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
