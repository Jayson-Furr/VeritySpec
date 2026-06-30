from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ContributionGuidanceTests(unittest.TestCase):
    def test_contributing_links_pack_and_schema_proposal_requirements(self) -> None:
        text = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

        required_phrases = [
            "Proposing a New Pack",
            "Proposing a Schema Change",
            "pack.json",
            "Strict JSON Schemas",
            "Readiness gates",
            "Reference rules",
            "Generator",
            "Migration",
            "git diff --check",
            "GitHub Actions is unavailable",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_pack_and_schema_issue_templates_capture_required_context(self) -> None:
        pack_template = (ROOT / ".github" / "ISSUE_TEMPLATE" / "pack_proposal.yml").read_text(
            encoding="utf-8"
        )
        schema_template = (ROOT / ".github" / "ISSUE_TEMPLATE" / "schema_change.yml").read_text(
            encoding="utf-8"
        )

        for phrase in [
            "Proposed pack ID",
            "Initial record kinds",
            "Reference rules",
            "Readiness gates",
            "Generator or report",
            "Executable example or fixture",
        ]:
            with self.subTest(template="pack", phrase=phrase):
                self.assertIn(phrase, pack_template)

        for phrase in [
            "Affected pack",
            "Affected record kind",
            "Change type",
            "Before and after examples",
            "Migration or compatibility plan",
            "Tests and fixtures",
        ]:
            with self.subTest(template="schema", phrase=phrase):
                self.assertIn(phrase, schema_template)

    def test_public_docs_link_contribution_guidance(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        packs = (ROOT / "docs" / "packs.md").read_text(encoding="utf-8")

        self.assertIn("[Contributing](CONTRIBUTING.md)", readme)
        self.assertIn("[Contributing](../CONTRIBUTING.md)", packs)


if __name__ == "__main__":
    unittest.main()
