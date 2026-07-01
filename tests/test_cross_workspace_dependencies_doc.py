from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "cross-workspace-dependencies.md"


class CrossWorkspaceDependencyDocTests(unittest.TestCase):
    def test_dependency_note_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        packs = (ROOT / "docs" / "packs.md").read_text(encoding="utf-8")
        workspace_format = (ROOT / "docs" / "workspace-format.md").read_text(encoding="utf-8")
        graph_checks = (ROOT / "docs" / "graph-checks.md").read_text(encoding="utf-8")

        for text in [readme, packs, workspace_format, graph_checks]:
            with self.subTest(document=text[:40]):
                self.assertIn("cross-workspace-dependencies.md", text)

    def test_dependency_note_preserves_first_phase_boundary(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "Current Prototype Boundary",
            "local path dependencies",
            "readonly dependencies",
            "direct dependencies",
            "remote registries",
            "Git authentication",
            "record-level `visibility`",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_dependency_note_defines_resolution_and_lockfile_concepts(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "Pack Versus Workspace",
            "Exported Records",
            "sharedUnity::unity.package.save_system",
            "verity://workspace/studio.library.shared_unity_runtime@1.2.4/record/unity.package.save_system",
            "verityspec.lock.json",
            "recordSetHash",
            "Validation Issue Codes",
            "dependency-aware validation and graph reporting",
            "integration workspaces",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
