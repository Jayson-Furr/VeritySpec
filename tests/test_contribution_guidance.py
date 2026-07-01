from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_PACK_CHECKLIST = ROOT / "docs" / "external-pack-review-checklist.md"


class ContributionGuidanceTests(unittest.TestCase):
    def test_contributing_links_pack_and_schema_proposal_requirements(self) -> None:
        text = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

        required_phrases = [
            "Proposing a New Pack",
            "Proposing a Schema Change",
            "External pack maintainer review checklist",
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
            "external pack maintainer review checklist",
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
        self.assertIn("docs/external-pack-review-checklist.md", readme)
        self.assertIn("external-pack-review-checklist.md", packs)

    def test_external_pack_review_checklist_defines_acceptance_gates(self) -> None:
        text = EXTERNAL_PACK_CHECKLIST.read_text(encoding="utf-8")

        for phrase in [
            "Review Inputs",
            "Identity Gate",
            "Contract Gate",
            "Executability Gate",
            "Documentation Gate",
            "Compatibility Gate",
            "PR Review Gate",
            "Acceptance Outcomes",
            "Pack proposal",
            "pack.json",
            "strict JSON Schemas",
            "shared record envelope",
            "readiness gates",
            "reference rules",
            "generator metadata",
            "verity pack validate",
            "verity validate",
            "verity lint --strict",
            "verity readiness --strict",
            "GitHub Actions is unavailable",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_external_pack_review_checklist_preserves_boundaries(self) -> None:
        text = EXTERNAL_PACK_CHECKLIST.read_text(encoding="utf-8")

        for phrase in [
            "not mean the pack is",
            "bundled, official, detached from core",
            "does not shadow built-in pack IDs",
            "avoid becoming a broad static catalog",
            "Specialized pack separation plan",
            "review gate, not a shortcut",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
