from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "product-surface-pack-boundaries.md"


class ProductSurfaceBoundaryTests(unittest.TestCase):
    def test_boundary_note_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        packs = (ROOT / "docs" / "packs.md").read_text(encoding="utf-8")

        self.assertIn("docs/product-surface-pack-boundaries.md", readme)
        self.assertIn("product-surface-pack-boundaries.md", packs)

    def test_boundary_note_defines_expected_surface_packs(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "verity.pack.game-core",
            "verity.pack.gui",
            "verity.pack.desktop",
            "verity.pack.mobile",
            "verity.pack.game",
            "First-Schema Gate",
            "strict JSON Schemas using the shared record envelope",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_boundary_note_preserves_cross_cutting_ownership(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for pack_id in [
            "verity.pack.security",
            "verity.pack.accessibility",
            "verity.pack.observability",
            "verity.pack.compliance",
        ]:
            with self.subTest(pack_id=pack_id):
                self.assertIn(pack_id, text)

        for concern in [
            "release",
            "evidence",
            "deployment",
            "dependency",
            "portfolio",
        ]:
            with self.subTest(concern=concern):
                self.assertIn(concern, text)


if __name__ == "__main__":
    unittest.main()
