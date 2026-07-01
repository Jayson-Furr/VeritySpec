from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "engine-full-lifecycle-support.md"


class EngineLifecycleDocTests(unittest.TestCase):
    def test_engine_lifecycle_design_note_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/engine-full-lifecycle-support.md", readme)

    def test_engine_lifecycle_design_note_preserves_scope_boundary(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "No schema changes are introduced by this design note.",
            "Core stays small.",
            "Unity, Godot, and Unreal",
            "Engine Parity Rule",
            "shared engine library workspace",
            "integration workspaces",
            "portfolio examples",
            "First-Implementation Gate",
            "integration workspaces remain the recommended transitional pattern",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_engine_lifecycle_design_note_defines_lifecycle_readiness_and_evidence(
        self,
    ) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "game-concept-complete",
            "engine-prototype-ready",
            "vertical-slice-ready",
            "engine-production-ready",
            "game-release-ready",
            "liveops-ready",
            "maintenance-ready",
            "decommission-ready",
            "archive-ready",
            "Evidence should connect lifecycle claims to proof records.",
            "telemetry dashboards",
            "archive manifests",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_engine_lifecycle_design_note_preserves_non_claims(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "commercial, legal, privacy-law, marketplace, platform-certification,",
            "or store-review guarantees",
            "Evidence records do not prove legal, privacy-law, marketplace,",
            "pricing, or certification approval",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
