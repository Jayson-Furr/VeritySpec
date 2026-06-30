from __future__ import annotations

import re
import unittest
from pathlib import Path

from verityspec import __version__


ROOT = Path(__file__).resolve().parents[1]
CURRENT_TAG = f"v{__version__}"
DOWNSTREAM_FILES = [
    ROOT / ".github" / "workflows" / "product-contract.yml",
    ROOT / "docs" / "downstream-ci.md",
    ROOT / "templates" / "github-actions" / "product-contract-direct.yml",
    ROOT / "templates" / "github-actions" / "product-contract-reusable.yml",
    ROOT / "templates" / "github-actions" / "product-contract-with-local-packs.yml",
]
PYPI_DOC = ROOT / "docs" / "pypi.md"
RELEASE_REF_PATTERN = re.compile(
    r"Jayson-Furr/VeritySpec(?:\.git)?(?:/\.github/workflows/product-contract\.yml)?@"
    r"(v\d+\.\d+\.\d+)"
)


class DownstreamTemplateTests(unittest.TestCase):
    def test_downstream_templates_reference_current_release_tag(self) -> None:
        for path in DOWNSTREAM_FILES:
            text = path.read_text(encoding="utf-8")
            refs = RELEASE_REF_PATTERN.findall(text)
            self.assertGreater(len(refs), 0, f"{path.relative_to(ROOT)} has no release-pinned reference")
            self.assertEqual(
                {CURRENT_TAG},
                set(refs),
                f"{path.relative_to(ROOT)} must reference {CURRENT_TAG}",
            )

    def test_downstream_templates_cover_core_contract_commands(self) -> None:
        command_files = [
            ROOT / ".github" / "workflows" / "product-contract.yml",
            ROOT / "docs" / "downstream-ci.md",
            ROOT / "templates" / "github-actions" / "product-contract-direct.yml",
        ]
        for path in command_files:
            text = path.read_text(encoding="utf-8")
            self.assertIn("verity validate", text, f"{path.relative_to(ROOT)} must validate")
            self.assertIn("verity lint", text, f"{path.relative_to(ROOT)} must lint")
            self.assertIn("verity readiness", text, f"{path.relative_to(ROOT)} must check readiness")

        direct_template = (ROOT / "templates" / "github-actions" / "product-contract-direct.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("verity generate validation-report", direct_template)
        self.assertIn("build/verity-validation-report.json", direct_template)

    def test_reusable_downstream_templates_call_reusable_workflow(self) -> None:
        reusable_template = (ROOT / "templates" / "github-actions" / "product-contract-reusable.yml").read_text(
            encoding="utf-8"
        )
        local_pack_template = (
            ROOT / "templates" / "github-actions" / "product-contract-with-local-packs.yml"
        ).read_text(encoding="utf-8")

        reusable_ref = f"Jayson-Furr/VeritySpec/.github/workflows/product-contract.yml@{CURRENT_TAG}"
        self.assertIn(reusable_ref, reusable_template)
        self.assertIn(reusable_ref, local_pack_template)
        self.assertIn("pack-paths: packs/features packs/security", local_pack_template)

    def test_pypi_docs_reference_current_release_tag_and_safeguards(self) -> None:
        text = PYPI_DOC.read_text(encoding="utf-8")
        refs = RELEASE_REF_PATTERN.findall(text)

        self.assertEqual({CURRENT_TAG}, set(refs))
        self.assertIn("publish_pypi=false", text)
        self.assertIn("trusted publishing", text)
        self.assertIn("No PyPI API token should be committed", text)
        self.assertIn("python3 -m twine check dist/*", text)
