from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from verityspec.generators import (
    generate_asyncapi,
    generate_openapi,
    generate_python_models,
    generate_security_report,
    generate_typescript,
)
from verityspec.envelope import RECORD_ENVELOPE_REQUIRED
from verityspec.pack_validation import validate_builtin_packs
from verityspec.packs import load_pack_registry
from verityspec.readiness import evaluate_readiness
from verityspec.validation import validate_workspace
from verityspec.workspace import load_workspace


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_FIXTURE = ROOT / "tests" / "fixtures" / "generator_maturity"
GENERATOR_GOLDEN = ROOT / "tests" / "golden" / "generator_maturity"


class VeritySpecTests(unittest.TestCase):
    def test_builtin_packs_validate(self) -> None:
        self.assertEqual([], validate_builtin_packs())

    def test_builtin_schemas_require_shared_record_envelope(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "basic")
        registry = load_pack_registry(workspace.pack_ids)

        for binding in registry.schemas.values():
            required = set(binding.schema.get("required", []))
            properties = set(binding.schema.get("properties", {}))
            for field in RECORD_ENVELOPE_REQUIRED:
                self.assertIn(field, required)
                self.assertIn(field, properties)

    def test_basic_example_validates(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "basic")
        registry = load_pack_registry(workspace.pack_ids)

        issues = validate_workspace(workspace, registry, strict=True)

        self.assertEqual([], issues)

    def test_missing_reference_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "broken",
                        "specVersion": "v0.1.0",
                        "packs": ["verity.core"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "product.json").write_text(
                json.dumps(
                    {
                        "id": "product.broken",
                        "kind": "product",
                        "name": "Broken Product",
                        "status": "ready",
                        "owner": "platform",
                        "version": "0.1.0",
                        "references": [{"type": "uses", "target": "schema.missing"}],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = validate_workspace(workspace, registry)

        self.assertTrue(any(issue.code == "reference.missing" for issue in issues))

    def test_readiness_catches_missing_release_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "not-ready",
                        "specVersion": "v0.1.0",
                        "packs": ["verity.pack.api"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "endpoint.json").write_text(
                json.dumps(
                    {
                        "id": "api.users.list",
                        "kind": "api.endpoint",
                        "name": "List Users",
                        "status": "ready",
                        "owner": "platform",
                        "method": "GET",
                        "path": "/users",
                        "responses": [{"statusCode": 200, "description": "OK"}],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertTrue(any(issue.code == "readiness.required" for issue in issues))

    def test_readiness_fails_critical_unverified_security_control(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "critical-security",
                        "specVersion": "v0.1.0",
                        "packs": ["verity.core", "verity.pack.security"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "product.json").write_text(
                json.dumps(
                    {
                        "id": "product.critical_security",
                        "kind": "product",
                        "name": "Critical Security Product",
                        "status": "ready",
                        "owner": "platform",
                        "version": "0.1.0",
                        "references": [{"type": "securedBy", "target": "security.control.mfa"}],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "security.json").write_text(
                json.dumps(
                    {
                        "id": "security.control.mfa",
                        "kind": "security.control",
                        "name": "MFA Enforcement",
                        "status": "ready",
                        "owner": "platform-security",
                        "description": "Require MFA for privileged access.",
                        "category": "authentication",
                        "controlType": "preventive",
                        "riskLevel": "critical",
                        "objective": "Prevent account takeover for privileged users.",
                        "coverage": "implemented",
                        "verification": {
                            "method": "not-verified",
                            "evidence": "MFA implementation exists but has not been verified.",
                        },
                        "references": [
                            {
                                "type": "appliesTo",
                                "target": "product.critical_security",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        matching = [
            issue
            for issue in issues
            if issue.code == "security.control.critical_unverified"
        ]
        self.assertEqual(1, len(matching))
        self.assertEqual("error", matching[0].severity)
        self.assertEqual("security.control.mfa", matching[0].record_id)

    def test_broken_semantic_fixture_reports_graph_and_reference_issues(self) -> None:
        workspace = load_workspace(ROOT / "tests" / "fixtures" / "broken_semantics")
        registry = load_pack_registry(workspace.pack_ids)

        issues = validate_workspace(workspace, registry)
        codes = {issue.code for issue in issues}

        self.assertIn("reference.missing", codes)
        self.assertIn("reference.disallowed", codes)
        self.assertIn("reference.deprecated", codes)
        self.assertIn("reference.removed", codes)
        self.assertIn("graph.cycle", codes)
        self.assertIn("graph.orphan", codes)
        self.assertIn("schema.unused", codes)

    def test_openapi_generator_emits_paths_and_components(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "basic")

        document = generate_openapi(workspace)

        self.assertIn("/users", document["paths"])
        self.assertIn("get", document["paths"]["/users"])
        self.assertIn("post", document["paths"]["/users"])
        self.assertIn("User", document["components"]["schemas"])

    def test_openapi_and_asyncapi_include_verity_metadata(self) -> None:
        workspace = load_workspace(GENERATOR_FIXTURE)

        openapi = generate_openapi(workspace)
        asyncapi = generate_asyncapi(workspace)

        operation = openapi["paths"]["/accounts/{accountId}"]["get"]
        self.assertEqual("api.accounts.get", operation["x-verity-id"])
        self.assertEqual(["platform"], operation["tags"])
        self.assertEqual(
            [
                {
                    "name": "accountId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
            operation["parameters"],
        )
        members_operation = openapi["paths"]["/accounts/{accountId}/members/{memberId}"]["get"]
        self.assertEqual(
            [
                {
                    "name": "accountId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Account identifier.",
                },
                {
                    "name": "memberId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                },
                {
                    "name": "includeInactive",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "boolean"},
                    "description": "Include inactive members.",
                },
            ],
            members_operation["parameters"],
        )
        message = asyncapi["components"]["messages"]["EventAccountChanged"]
        self.assertEqual("event.account.changed", message["x-verity-id"])
        self.assertEqual(
            "subscribe_event_account_changed",
            asyncapi["channels"]["account.changed"]["subscribe"]["operationId"],
        )

    def test_openapi_generator_matches_golden_file(self) -> None:
        workspace = load_workspace(GENERATOR_FIXTURE)
        expected = json.loads((GENERATOR_GOLDEN / "openapi.json").read_text(encoding="utf-8"))

        self.assertEqual(expected, generate_openapi(workspace))

    def test_typescript_generator_matches_golden_file(self) -> None:
        workspace = load_workspace(GENERATOR_FIXTURE)
        expected = (GENERATOR_GOLDEN / "typescript.ts").read_text(encoding="utf-8")

        self.assertEqual(expected, generate_typescript(workspace))

    def test_python_model_generator_matches_golden_file(self) -> None:
        workspace = load_workspace(GENERATOR_FIXTURE)
        expected = (GENERATOR_GOLDEN / "python_models.py").read_text(encoding="utf-8")

        self.assertEqual(expected, generate_python_models(workspace))

    def test_security_report_summarizes_security_controls(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "security")

        report = generate_security_report(workspace)

        self.assertEqual("security_report", report["type"])
        self.assertEqual(1, report["controlCount"])
        self.assertEqual({"verified": 1}, report["summary"]["byCoverage"])
        self.assertEqual({"high": 1}, report["summary"]["byRiskLevel"])
        self.assertEqual(1, report["summary"]["verifiedControls"])
        self.assertEqual([], report["summary"]["criticalUnverified"])
        control = report["controls"][0]
        self.assertEqual("security.control.account_access", control["id"])
        self.assertTrue(control["verified"])
        self.assertEqual(
            ["api.accounts.get", "schema.account"],
            [target["id"] for target in control["targets"]],
        )


if __name__ == "__main__":
    unittest.main()
