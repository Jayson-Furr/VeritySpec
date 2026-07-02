from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "installed-pack-compatibility-metadata.md"


class InstalledPackCompatibilityMetadataDocTests(unittest.TestCase):
    def test_design_note_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        packs = (ROOT / "docs" / "packs.md").read_text(encoding="utf-8")
        separation = (ROOT / "docs" / "specialized-pack-separation.md").read_text(
            encoding="utf-8"
        )
        fixtures = (ROOT / "docs" / "official-extension-compatibility-fixtures.md").read_text(
            encoding="utf-8"
        )
        engine_direction = (ROOT / "docs" / "engine-product-delivery-packs.md").read_text(
            encoding="utf-8"
        )
        adr_doc = (ROOT / "docs" / "architecture-decision-records.md").read_text(
            encoding="utf-8"
        )
        branching = (ROOT / "docs" / "branching.md").read_text(encoding="utf-8")

        for text in [
            readme,
            packs,
            separation,
            fixtures,
            engine_direction,
            adr_doc,
            branching,
        ]:
            with self.subTest(source=text[:40]):
                self.assertIn("installed-pack-compatibility-metadata.md", text)

    def test_design_note_defines_metadata_contract(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "No runtime compatibility enforcement is introduced by this design note.",
            "supported VeritySpec versions",
            "workspace format versions",
            "pack API level",
            "official extension-package lifecycle states",
            "\"compatibility\"",
            "\"supportedVersions\"",
            "\"workspaceFormats\"",
            "\"packApi\"",
            "\"officialExtension\"",
            "verityspec.packs",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_design_note_defines_lifecycle_states(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "`bundled`",
            "`mirrored`",
            "`official-preview`",
            "`detached`",
            "`deprecated`",
            "`removed`",
            "Record lifecycle remains governed by the record status model",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_design_note_preserves_runtime_non_goals(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "enforce compatibility metadata at runtime",
            "detach bundled specialized packs",
            "publish official extension packages",
            "change `verityspec.packs` entry-point loading behavior",
            "allow installed packages to shadow built-in pack IDs",
            "rename pack IDs, record kinds, or workspace `packs` entries",
            "change pack manifest validation requirements in this release",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
