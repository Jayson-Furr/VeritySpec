from __future__ import annotations

import unittest
from pathlib import Path

from verityspec.pack_compatibility import compare_pack_mirror


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "product-surface-pack-boundaries.md"
ENGINE_DOC = ROOT / "docs" / "engine-product-delivery-packs.md"
SEPARATION_DOC = ROOT / "docs" / "specialized-pack-separation.md"
EXTENSION_FIXTURE_DOC = ROOT / "docs" / "official-extension-compatibility-fixtures.md"
UNITY_MIRROR = ROOT / "tests" / "fixtures" / "official_extension_mirrors" / "verityspec-pack-unity" / "pack"


class ProductSurfaceBoundaryTests(unittest.TestCase):
    def test_boundary_note_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        packs = (ROOT / "docs" / "packs.md").read_text(encoding="utf-8")

        self.assertIn("docs/product-surface-pack-boundaries.md", readme)
        self.assertIn("docs/engine-product-delivery-packs.md", readme)
        self.assertIn("docs/specialized-pack-separation.md", readme)
        self.assertIn("docs/official-extension-compatibility-fixtures.md", readme)
        self.assertIn("product-surface-pack-boundaries.md", packs)
        self.assertIn("engine-product-delivery-packs.md", packs)
        self.assertIn("specialized-pack-separation.md", packs)
        self.assertIn("official-extension-compatibility-fixtures.md", packs)

    def test_boundary_note_defines_expected_surface_packs(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "verity.pack.game-core",
            "verity.pack.gameplay",
            "verity.pack.content",
            "verity.pack.economy",
            "verity.pack.unreal",
            "verity.pack.gui",
            "verity.pack.desktop",
            "verity.pack.mobile",
            "verity.pack.liveops",
            "verity.pack.game",
            "First-Schema Gate",
            "strict JSON Schemas using the shared record envelope",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_specialized_pack_separation_plan_defines_candidate_packages(self) -> None:
        text = SEPARATION_DOC.read_text(encoding="utf-8")

        for phrase in [
            "verityspec-pack-game",
            "verityspec-pack-mobile",
            "verityspec-pack-liveops",
            "verityspec-pack-unity",
            "verityspec-pack-godot",
            "verityspec-pack-unreal",
            "verity.pack.game-core",
            "verity.pack.game-assets",
            "verity.pack.gameplay",
            "verity.pack.content",
            "verity.pack.economy",
            "verity.pack.progression",
            "verity.pack.mobile",
            "verity.pack.liveops",
            "verity.pack.unity",
            "verity.pack.godot",
            "verity.pack.unreal",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_specialized_pack_separation_plan_preserves_detach_gates(self) -> None:
        text = SEPARATION_DOC.read_text(encoding="utf-8")

        for phrase in [
            "This is not an immediate removal plan.",
            "Existing bundled packs remain available",
            "Built-in pack IDs are reserved until an official detach gate exists.",
            "compatibility metadata",
            "bundled-versus-installed parity tests",
            "migration guidance",
            "rollback criteria",
            "Do not remove specialized bundled packs in the first separation sprint.",
            "Do not rename pack IDs or record kinds for packaging reasons.",
            "Do not make arbitrary installed packages shadow built-in pack IDs.",
            "verity pack compare",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_official_extension_fixture_guidance_defines_mirror_contract(self) -> None:
        text = EXTENSION_FIXTURE_DOC.read_text(encoding="utf-8")

        for phrase in [
            "verity pack compare verity.pack.unity",
            "manifest identity",
            "schema declarations",
            "schema JSON content",
            "readiness gates",
            "reference rules",
            "generator metadata",
            "does not detach bundled packs",
            "does not allow arbitrary installed packages to shadow built-in pack IDs",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_official_extension_unity_mirror_matches_bundled_pack(self) -> None:
        report, issues = compare_pack_mirror("verity.pack.unity", UNITY_MIRROR)

        self.assertEqual([], issues)
        self.assertTrue(report["passed"])
        self.assertEqual(0, report["summary"]["differences"])
        self.assertEqual(report["source"]["schemaDeclarations"], report["mirror"]["schemaDeclarations"])
        self.assertEqual(report["source"]["readinessGates"], report["mirror"]["readinessGates"])
        self.assertEqual(report["source"]["referenceRules"], report["mirror"]["referenceRules"])
        self.assertEqual(report["source"]["generatorMetadata"], report["mirror"]["generatorMetadata"])

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
            "Engine Pack Parity Rule",
            "Unity, Godot, and Unreal coverage",
            "godot.validation-runner",
            "unreal.gameplay-ability",
            "product.scope",
            "product-delivery source of truth",
            "verity pack validate",
            "commercial, legal, marketplace, or certification guarantees",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
