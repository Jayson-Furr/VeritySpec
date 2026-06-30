from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "product-surface-pack-boundaries.md"
ENGINE_DOC = ROOT / "docs" / "engine-product-delivery-packs.md"


class ProductSurfaceBoundaryTests(unittest.TestCase):
    def test_boundary_note_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        packs = (ROOT / "docs" / "packs.md").read_text(encoding="utf-8")

        self.assertIn("docs/product-surface-pack-boundaries.md", readme)
        self.assertIn("docs/engine-product-delivery-packs.md", readme)
        self.assertIn("product-surface-pack-boundaries.md", packs)
        self.assertIn("engine-product-delivery-packs.md", packs)

    def test_boundary_note_defines_expected_surface_packs(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "verity.pack.game-core",
            "verity.pack.gameplay",
            "verity.pack.content",
            "verity.pack.economy",
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

    def test_engine_product_delivery_note_defines_future_pack_scope(self) -> None:
        text = ENGINE_DOC.read_text(encoding="utf-8")

        for phrase in [
            "GitHub manages workflow. VeritySpec manages truth.",
            "verity.pack.godot",
            "verity.pack.unreal",
            "verity.pack.product-delivery",
            "unity.agent-context-exporter",
            "games made with Godot",
            "games made with Unreal",
            "godot.validation-runner",
            "unreal.gameplay-ability",
            "product.scope",
            "verity pack validate",
            "commercial, legal, marketplace, or certification guarantees",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
