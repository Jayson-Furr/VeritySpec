from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "lifecycle-readiness-fixture-plan.md"


class LifecycleFixturePlanDocTests(unittest.TestCase):
    def test_lifecycle_fixture_plan_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/lifecycle-readiness-fixture-plan.md", readme)

    def test_lifecycle_fixture_plan_preserves_scope_boundary(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "does not add schemas, runtime behavior, or new readiness claims",
            "engine-prototype readiness",
            "Unity, Godot, and Unreal",
            "Engine Parity Expectations",
            "Integration workspaces remain the recommended transitional pattern",
            "first-class cross-workspace dependency resolution",
            "Future Executable Commands",
            "Acceptance Gates For The Implementation Sprint",
            "Non-Goals And Non-Claims",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_lifecycle_fixture_plan_names_planned_fixture_family(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "tests/fixtures/engine_lifecycle/unity-prototype",
            "tests/fixtures/engine_lifecycle/godot-prototype",
            "tests/fixtures/engine_lifecycle/unreal-prototype",
            "tests/fixtures/engine_lifecycle/integration-prototype",
            "unity.validation-runner",
            "godot.validation-runner",
            "unreal.validation-runner",
            "unity.agent-context-exporter",
            "godot.agent-context-exporter",
            "unreal.agent-context-exporter",
            "evidence.test",
            "evidence.build",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_lifecycle_fixture_plan_preserves_non_claims(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "commercial, legal, privacy-law,",
            "marketplace, platform-certification, app-store, pricing, support-SLA, or",
            "store-review readiness",
            "will only prove that VeritySpec can model and",
            "validate the declared prototype lifecycle contract",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
