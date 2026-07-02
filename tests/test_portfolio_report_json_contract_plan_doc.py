from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "portfolio-report-json-contract-plan.md"


class PortfolioReportJsonContractPlanDocTests(unittest.TestCase):
    def test_portfolio_report_plan_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        portfolio_validation = (ROOT / "docs" / "portfolio-validation.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/portfolio-report-json-contract-plan.md", readme)
        self.assertIn("portfolio-report-json-contract-plan.md", portfolio_validation)

    def test_portfolio_report_plan_preserves_scope_boundary(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "does not add schemas, commands, generators, readiness gates, or dependency",
            "Portfolio Report JSON Contract Plan",
            "verity generate portfolio-report",
            "Planned JSON Shape",
            "Workspace Entries",
            "Impact Warnings",
            "Evidence Gaps",
            "Agent Context Refresh Needs",
            "Acceptance Gates For Implementation",
            "Non-Goals And Non-Claims",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_portfolio_report_plan_names_planned_contract_sections(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            '"type": "portfolio_report"',
            '"schemaVersion": "0.1.0"',
            '"workspaces": []',
            '"relationships": []',
            '"impactWarnings": []',
            '"evidenceGaps": []',
            '"generatedArtifactRefreshNeeds": []',
            '"agentContextRefreshNeeds": []',
            '"followUpRecommendations": []',
            '"claimBoundaries": []',
            "--generated-at",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_portfolio_report_plan_names_planned_fixtures(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "tests/fixtures/portfolio_report/basic",
            "tests/fixtures/portfolio_report/engine-portfolio",
            "tests/fixtures/portfolio_report/evidence-gaps",
            "tests/fixtures/portfolio_report/agent-context-refresh",
            "golden JSON fixture",
            "generatedAt",
            "verityVersion",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_portfolio_report_plan_preserves_non_claims(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "commercial, legal, privacy-law, marketplace,",
            "platform-certification, app-store, store-review, pricing-approval,",
            "support-SLA, security-certification, or production-readiness guarantees",
            "They do not prove external approval",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
