from __future__ import annotations

import unittest
from pathlib import Path

from verityspec.packs import load_pack_registry
from verityspec.readiness import evaluate_readiness
from verityspec.validation import lint_workspace, validate_workspace
from verityspec.workspace import load_workspace


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "portfolio-validation.md"
EXAMPLE = ROOT / "examples" / "portfolio"


class PortfolioValidationDocTests(unittest.TestCase):
    def test_portfolio_validation_note_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/portfolio-validation.md", readme)
        self.assertIn("examples/portfolio/verityspec.json", readme)

    def test_portfolio_validation_note_preserves_scope_boundary(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "No schema changes are introduced by this design note.",
            "portfolio-level validation",
            "multi-workspace product, service, library, and game portfolios",
            "workspace inventory",
            "validation status",
            "readiness status",
            "impact warnings",
            "integration workspaces",
            "cross-workspace dependencies",
            "First-Implementation Gate",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_portfolio_validation_note_preserves_non_claims(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "commercial, legal, privacy-law, marketplace, platform-certification,",
            "store-review, pricing-approval, app-store-approval, or support-SLA guarantees",
            "They do not prove external approval",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_portfolio_example_validates_lints_and_passes_readiness(self) -> None:
        workspace = load_workspace(EXAMPLE)
        registry = load_pack_registry(workspace.pack_ids)

        self.assertEqual([], validate_workspace(workspace, registry, strict=True))
        self.assertEqual([], lint_workspace(workspace, registry, strict=True))
        self.assertEqual([], evaluate_readiness(workspace, registry, strict=True))

    def test_portfolio_example_documents_transitional_report_capabilities(self) -> None:
        text = (EXAMPLE / "records" / "capabilities.json").read_text(encoding="utf-8")

        for phrase in [
            "portfolio-workspace-matrix.json",
            "portfolio-summary.json",
            "verity graph examples/portfolio",
            "Portfolio Agent Context Exporter",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()

