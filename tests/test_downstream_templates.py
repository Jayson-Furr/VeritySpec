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
    ROOT / "templates" / "github-actions" / "product-contract-monorepo.yml",
    ROOT / "templates" / "github-actions" / "product-contract-profiles.yml",
    ROOT / "templates" / "github-actions" / "product-contract-reusable.yml",
    ROOT / "templates" / "github-actions" / "product-contract-with-local-packs.yml",
]
PYPI_DOC = ROOT / "docs" / "pypi.md"
RELEASE_REF_PATTERN = re.compile(
    r"Jason-Furr/verity-spec(?:\.git)?(?:/\.github/workflows/product-contract\.yml)?@"
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
            self.assertIn(
                "--github-annotations",
                text,
                f"{path.relative_to(ROOT)} must preserve CI annotation guidance",
            )

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
        monorepo_template = (ROOT / "templates" / "github-actions" / "product-contract-monorepo.yml").read_text(
            encoding="utf-8"
        )

        reusable_ref = f"Jason-Furr/verity-spec/.github/workflows/product-contract.yml@{CURRENT_TAG}"
        self.assertIn(reusable_ref, reusable_template)
        self.assertIn(reusable_ref, local_pack_template)
        self.assertIn(reusable_ref, monorepo_template)
        self.assertIn("pack-paths: packs/features packs/security", local_pack_template)

    def test_monorepo_downstream_template_checks_multiple_workspaces_with_shared_packs(self) -> None:
        text = (ROOT / "templates" / "github-actions" / "product-contract-monorepo.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("strategy:", text)
        self.assertIn("fail-fast: false", text)
        self.assertIn("matrix:", text)
        self.assertIn("services/catalog/specs", text)
        self.assertIn("apps/admin/specs", text)
        self.assertIn("packages/cli/specs", text)
        self.assertIn("packs/shared", text)
        self.assertIn("pack-paths: ${{ matrix.pack_paths }}", text)
        self.assertIn("strict: ${{ matrix.strict }}", text)

    def test_reusable_workflow_accepts_profile_input(self) -> None:
        text = (ROOT / ".github" / "workflows" / "product-contract.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("profile:", text)
        self.assertIn("PROFILE: ${{ inputs.profile }}", text)
        self.assertIn("profile_args=()", text)
        self.assertIn('profile_args+=(--profile "$PROFILE")', text)
        self.assertIn('"${profile_args[@]}"', text)
        self.assertIn('verity doctor "$WORKSPACE" --format json', text)

    def test_profile_downstream_template_covers_builtin_enforcement_profiles(self) -> None:
        text = (ROOT / "templates" / "github-actions" / "product-contract-profiles.yml").read_text(
            encoding="utf-8"
        )

        reusable_ref = f"Jason-Furr/verity-spec/.github/workflows/product-contract.yml@{CURRENT_TAG}"
        self.assertIn(reusable_ref, text)
        self.assertIn("fail-fast: false", text)
        self.assertIn("profile: release", text)
        self.assertIn("profile: regulated", text)
        self.assertIn("profile: public-api", text)
        self.assertIn("profile: internal-tool", text)
        self.assertIn("workspace: specs/release", text)
        self.assertIn("workspace: specs/regulated", text)
        self.assertIn("workspace: specs/public-api", text)
        self.assertIn("workspace: specs/internal-tool", text)
        self.assertRegex(text, r"profile: internal-tool\n\s+strict: false")
        self.assertIn("profile: ${{ matrix.profile }}", text)

    def test_downstream_profile_docs_preserve_profile_guidance_and_non_claims(self) -> None:
        text = (ROOT / "docs" / "downstream-ci.md").read_text(encoding="utf-8")

        for phrase in [
            "templates/github-actions/product-contract-profiles.yml",
            "profile: release",
            "profile: regulated",
            "profile: public-api",
            "profile: internal-tool",
            "strict: false",
            "The reusable workflow passes `profile` to `verity validate`, `verity lint`,",
            "These profiles are VeritySpec enforcement postures only.",
            "commercial, legal, privacy-law, marketplace, platform-certification,",
            "app-store, store-review, pricing-approval, or support-SLA readiness",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_pypi_docs_reference_current_release_tag_and_safeguards(self) -> None:
        text = PYPI_DOC.read_text(encoding="utf-8")
        refs = RELEASE_REF_PATTERN.findall(text)

        self.assertEqual({CURRENT_TAG}, set(refs))
        self.assertIn("publish_pypi=false", text)
        self.assertIn("trusted publishing", text)
        self.assertIn("No PyPI API token should be committed", text)
        self.assertIn("python3 -m twine check dist/*", text)
