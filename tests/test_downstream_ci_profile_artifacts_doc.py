from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "downstream-ci-profile-artifacts.md"


class DownstreamCiProfileArtifactsDocTests(unittest.TestCase):
    def test_downstream_ci_profile_artifacts_guidance_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        downstream_ci = (ROOT / "docs" / "downstream-ci.md").read_text(
            encoding="utf-8"
        )
        profiles = (ROOT / "docs" / "product-contract-profiles.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/downstream-ci-profile-artifacts.md", readme)
        self.assertIn("downstream-ci-profile-artifacts.md", downstream_ci)
        self.assertIn("downstream-ci-profile-artifacts.md", profiles)

    def test_downstream_ci_profile_artifacts_guidance_names_profile_bundles(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "release/",
            "regulated/",
            "public-api/",
            "internal-tool/",
            "validation.json",
            "lint.json",
            "readiness.json",
            "doctor.json",
            "graph.json",
            "validation-report.json",
            "evidence-report.json",
            "security-report.json",
            "accessibility-report.json",
            "compliance-matrix.json",
            "openapi.json",
            "schema-bundle.json",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_downstream_ci_profile_artifacts_guidance_includes_upload_and_fallback(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "actions/upload-artifact@v4",
            "if: always()",
            "retention-days: 14",
            "if-no-files-found: warn",
            "github.run_id",
            "github.run_attempt",
            "GitHub Actions cannot run because of billing, credits, quota",
            "run equivalent commands locally",
            "PYTHONPATH=src python3 -m verityspec validate",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_downstream_ci_profile_artifacts_guidance_preserves_redaction_and_non_claims(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "private paths, secrets, tokens, customer data",
            "unpublished product data",
            "build/verity-artifacts/**",
            "redaction step before `actions/upload-artifact`",
            "commercial, legal, privacy-law, marketplace, app-store,",
            "platform-certification, pricing-approval, support-SLA, security-certification,",
            "or production-readiness approval",
            "does not change the reusable workflow",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_downstream_ci_profile_artifacts_guidance_names_organization_follow_up(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        self.assertIn("Organization Follow-Up", text)
        self.assertIn("propose a follow-up write-back", text)
        self.assertIn("Jason-Furr/organization-patterns", text)


if __name__ == "__main__":
    unittest.main()
