from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path

from verityspec.generators import (
    generate_accessibility_report,
    generate_asyncapi,
    generate_compliance_matrix,
    generate_coverage_dashboard,
    generate_deployment_report,
    generate_observability_report,
    generate_openapi,
    generate_pack_capability_index,
    generate_product_impact_report,
    generate_python_models,
    generate_roadmap_report,
    generate_schema_bundle,
    generate_security_report,
    generate_typescript,
    generate_validation_report,
    generated_at_value,
)
from verityspec.envelope import RECORD_ENVELOPE_REQUIRED
from verityspec.issues import Issue, escape_github_property, parse_issue_location
from verityspec.pack_validation import validate_builtin_packs
from verityspec.packs import load_pack_registry
from verityspec.profiles import PROFILES, profile_issues
from verityspec.readiness import evaluate_readiness
from verityspec.validation import validate_workspace
from verityspec.workspace import load_workspace


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_FIXTURE = ROOT / "tests" / "fixtures" / "generator_maturity"
GENERATOR_GOLDEN = ROOT / "tests" / "golden" / "generator_maturity"
SECURITY_REPORT_GOLDEN = ROOT / "tests" / "golden" / "security_report" / "security_report.json"
OBSERVABILITY_GOLDEN = ROOT / "tests" / "golden" / "observability"
DEPLOYMENT_GOLDEN = ROOT / "tests" / "golden" / "deployment" / "deployment_report.json"
COVERAGE_DASHBOARD_GOLDEN = (
    ROOT / "tests" / "golden" / "coverage_dashboard" / "coverage_dashboard.json"
)
COVERAGE_FIXTURE = ROOT / "tests" / "fixtures" / "cross_pack_coverage"
CUSTOM_PACK_WORKSPACE = ROOT / "tests" / "fixtures" / "custom_pack_workspace"
PACK_CAPABILITY_INDEX_GOLDEN = (
    ROOT / "tests" / "golden" / "pack_capability_index" / "pack_capability_index.json"
)
PRODUCT_IMPACT_BASELINE = ROOT / "tests" / "fixtures" / "product_impact" / "baseline"
PRODUCT_IMPACT_CURRENT = ROOT / "tests" / "fixtures" / "product_impact" / "current"
PRODUCT_IMPACT_GOLDEN = ROOT / "tests" / "golden" / "product_impact" / "product_impact.json"
FIXED_GENERATED_AT = "2026-01-02T03:04:05Z"


def normalize_security_report_for_golden(report: dict) -> dict:
    normalized = dict(report)
    normalized["generatedAt"] = "<generatedAt>"
    normalized["verityVersion"] = "<verityVersion>"
    normalized["workspacePath"] = "<workspacePath>"
    return normalized


def normalize_observability_report_for_golden(report: dict) -> dict:
    normalized = dict(report)
    normalized["generatedAt"] = "<generatedAt>"
    normalized["verityVersion"] = "<verityVersion>"
    normalized["workspacePath"] = "<workspacePath>"
    return normalized


def normalize_deployment_report_for_golden(report: dict) -> dict:
    normalized = dict(report)
    normalized["generatedAt"] = "<generatedAt>"
    normalized["verityVersion"] = "<verityVersion>"
    normalized["workspacePath"] = "<workspacePath>"
    return normalized


def normalize_coverage_dashboard_for_golden(report: dict) -> dict:
    normalized = dict(report)
    normalized["generatedAt"] = "<generatedAt>"
    normalized["verityVersion"] = "<verityVersion>"
    normalized["workspacePath"] = "<workspacePath>"
    return normalized


def normalize_product_impact_for_golden(report: dict) -> dict:
    normalized = dict(report)
    normalized["generatedAt"] = "<generatedAt>"
    normalized["verityVersion"] = "<verityVersion>"
    normalized["oldWorkspace"] = dict(report["oldWorkspace"])
    normalized["newWorkspace"] = dict(report["newWorkspace"])
    normalized["oldWorkspace"]["workspacePath"] = "<oldWorkspacePath>"
    normalized["newWorkspace"]["workspacePath"] = "<newWorkspacePath>"
    return normalized


def normalize_pack_capability_index_for_golden(report: dict) -> dict:
    def normalize_value(value):
        if isinstance(value, dict):
            normalized = {}
            for key, inner in value.items():
                if key == "path" and isinstance(inner, str):
                    normalized[key] = normalize_repo_path(inner)
                else:
                    normalized[key] = normalize_value(inner)
            return normalized
        if isinstance(value, list):
            return [normalize_value(item) for item in value]
        return value

    def normalize_repo_path(path: str) -> str:
        candidate = Path(path)
        try:
            relative = candidate.resolve().relative_to(ROOT)
        except ValueError:
            return path
        return f"<repo>/{relative}"

    normalized = normalize_value(report)
    normalized["generatedAt"] = "<generatedAt>"
    normalized["verityVersion"] = "<verityVersion>"
    normalized["workspacePath"] = "<workspacePath>"
    return normalized


def write_security_freshness_workspace(root: Path, last_verified: str | None, cadence_days: int = 30) -> None:
    (root / "records").mkdir()
    (root / "verityspec.json").write_text(
        json.dumps(
            {
                "workspace": "security-freshness",
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
                "id": "product.security_freshness",
                "kind": "product",
                "name": "Security Freshness Product",
                "status": "ready",
                "owner": "platform",
                "version": "0.1.0",
                "references": [{"type": "securedBy", "target": "security.control.session_review"}],
            }
        ),
        encoding="utf-8",
    )
    verification = {
        "method": "manual-review",
        "evidence": "docs/security/session-review.md",
        "reviewCadenceDays": cadence_days,
    }
    if last_verified is not None:
        verification["lastVerified"] = last_verified
    (root / "records" / "security.json").write_text(
        json.dumps(
            {
                "id": "security.control.session_review",
                "kind": "security.control",
                "name": "Session Review",
                "status": "ready",
                "owner": "platform-security",
                "description": "Review session handling controls.",
                "category": "authentication",
                "controlType": "detective",
                "riskLevel": "high",
                "objective": "Keep session security evidence current.",
                "coverage": "verified",
                "verification": verification,
                "references": [
                    {
                        "type": "appliesTo",
                        "target": "product.security_freshness",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


class VeritySpecTests(unittest.TestCase):
    def test_issue_location_details_parse_record_index_and_field_pointer(self) -> None:
        details = parse_issue_location("records/batch.json#records/2:responses[0].statusCode")

        self.assertEqual("records/batch.json", details["path"])
        self.assertEqual("records/2", details["fragment"])
        self.assertEqual(2, details["recordIndex"])
        self.assertEqual("responses[0].statusCode", details["fieldPath"])
        self.assertEqual(["responses", 0, "statusCode"], details["fieldParts"])
        self.assertEqual("/responses/0/statusCode", details["jsonPointer"])

    def test_issue_location_details_preserve_windows_paths_without_fields(self) -> None:
        details = parse_issue_location("C:\\repo\\workspace\\verityspec.json")

        self.assertEqual({"path": "C:\\repo\\workspace\\verityspec.json"}, details)

    def test_github_annotation_escapes_workflow_command_data(self) -> None:
        issue = Issue(
            "error",
            "schema.validation:bad,field",
            "Message with % percent\nnext line\rcarriage",
            "records/path:with,chars.json:field",
            "record.with:colon,comma",
        )

        annotation = issue.github_annotation()

        self.assertIn("::error ", annotation)
        self.assertIn("file=records/path%3Awith%2Cchars.json", annotation)
        self.assertIn("title=schema.validation%3Abad%2Cfield", annotation)
        self.assertIn("Message with %25 percent%0Anext line%0Dcarriage", annotation)
        self.assertEqual("a%3Ab%2Cc", escape_github_property("a:b,c"))

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

    def test_regulated_profile_reports_missing_governance_packs(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "basic")

        issues = profile_issues(workspace, PROFILES["regulated"])

        self.assertEqual(["profile.required_pack"] * 3, [issue.code for issue in issues])
        self.assertTrue(all(issue.severity == "error" for issue in issues))

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

        matching = [issue for issue in issues if issue.code == "reference.missing"]
        self.assertEqual(1, len(matching))
        self.assertTrue(matching[0].location.endswith("records/product.json:references[0].target"))

    def test_schema_validation_location_includes_nested_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "schema-location",
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
                        "responses": [{"statusCode": "OK", "description": "OK"}],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = validate_workspace(workspace, registry)

        matching = [issue for issue in issues if issue.code == "schema.validation"]
        self.assertEqual(1, len(matching))
        self.assertTrue(matching[0].location.endswith("records/endpoint.json:responses[0].statusCode"))

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

        matching = [issue for issue in issues if issue.code == "readiness.required"]
        self.assertEqual(1, len(matching))
        self.assertTrue(matching[0].location.endswith("records/endpoint.json:summary"))

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

    def test_readiness_accepts_fresh_security_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            last_verified = date.today().isoformat()
            write_security_freshness_workspace(root, last_verified)

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertFalse(any(issue.code == "security.control.evidence_stale" for issue in issues))

    def test_readiness_fails_stale_security_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            last_verified = (date.today() - timedelta(days=31)).isoformat()
            write_security_freshness_workspace(root, last_verified, cadence_days=30)

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        matching = [issue for issue in issues if issue.code == "security.control.evidence_stale"]
        self.assertEqual(1, len(matching))
        self.assertEqual("error", matching[0].severity)
        self.assertEqual("security.control.session_review", matching[0].record_id)
        self.assertTrue(matching[0].location.endswith("records/security.json:verification.lastVerified"))

    def test_readiness_fails_security_evidence_missing_last_verified_when_cadence_declared(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_security_freshness_workspace(root, None, cadence_days=30)

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertTrue(any(issue.code == "security.control.evidence_stale" for issue in issues))

    def test_readiness_fails_critical_unverified_accessibility_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "critical-accessibility",
                        "specVersion": "v0.1.0",
                        "packs": ["verity.core", "verity.pack.accessibility"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "product.json").write_text(
                json.dumps(
                    {
                        "id": "product.critical_accessibility",
                        "kind": "product",
                        "name": "Critical Accessibility Product",
                        "description": "A product with a critical accessibility claim.",
                        "status": "ready",
                        "owner": "platform",
                        "version": "0.1.0",
                        "references": [],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "accessibility.json").write_text(
                json.dumps(
                    {
                        "id": "accessibility.claim.keyboard",
                        "kind": "accessibility.claim",
                        "name": "Keyboard Operation",
                        "description": "Core workflow supports keyboard-only use.",
                        "status": "ready",
                        "owner": "design-systems",
                        "standard": "wcag-2.2",
                        "criterion": "2.1.1 Keyboard",
                        "level": "a",
                        "userNeed": "Keyboard users can complete the workflow.",
                        "surface": "critical workflow",
                        "impact": "critical",
                        "coverage": "implemented",
                        "verification": {
                            "method": "not-verified",
                            "evidence": "Manual test plan exists but has not run.",
                        },
                        "references": [
                            {
                                "type": "appliesTo",
                                "target": "product.critical_accessibility",
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
            if issue.code == "accessibility.claim.critical_unverified"
        ]
        self.assertEqual(1, len(matching))
        self.assertEqual("error", matching[0].severity)
        self.assertEqual("accessibility.claim.keyboard", matching[0].record_id)

    def test_readiness_fails_reviewed_unverified_compliance_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "reviewed-compliance",
                        "specVersion": "v0.1.0",
                        "packs": ["verity.core", "verity.pack.compliance"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "product.json").write_text(
                json.dumps(
                    {
                        "id": "product.reviewed_compliance",
                        "kind": "product",
                        "name": "Reviewed Compliance Product",
                        "description": "A product with a reviewed compliance mapping.",
                        "status": "ready",
                        "owner": "platform",
                        "version": "0.1.0",
                        "references": [
                            {
                                "type": "complianceMappedBy",
                                "target": "compliance.mapping.reviewed",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "compliance.json").write_text(
                json.dumps(
                    {
                        "id": "compliance.mapping.reviewed",
                        "kind": "compliance.mapping",
                        "name": "Reviewed Mapping",
                        "description": "A reviewed mapping that still lacks real verification.",
                        "status": "ready",
                        "owner": "risk",
                        "framework": {
                            "name": "internal",
                            "requirementId": "INT-1",
                        },
                        "mappingType": "control",
                        "coverage": "reviewed",
                        "attestation": False,
                        "verification": {
                            "method": "not-verified",
                            "evidence": "Mapping is drafted but verification has not run.",
                        },
                        "references": [
                            {
                                "type": "covers",
                                "target": "product.reviewed_compliance",
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
            if issue.code == "compliance.mapping.reviewed_unverified"
        ]
        self.assertEqual(1, len(matching))
        self.assertEqual("error", matching[0].severity)
        self.assertEqual("compliance.mapping.reviewed", matching[0].record_id)

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

    def test_roadmap_report_summarizes_release_governance(self) -> None:
        report = generate_roadmap_report(ROOT)

        datetime.fromisoformat(report["generatedAt"])
        self.assertEqual("roadmap_report", report["type"])
        self.assertEqual(str(ROOT / "ROADMAP.md"), report["roadmapPath"])
        self.assertIsInstance(report["verityVersion"], str)
        self.assertGreater(report["summary"]["milestones"], 0)
        self.assertGreater(report["summary"]["completedSprints"], 0)
        self.assertEqual(20, report["summary"]["nextRoadmapPoints"])
        self.assertEqual(list(range(1, 21)), [point["number"] for point in report["nextRoadmapPoints"]])
        milestone_versions = {milestone["version"] for milestone in report["milestones"]}
        self.assertIn(report["latestReleasedMilestone"], milestone_versions)

    def test_report_generators_accept_explicit_generated_at(self) -> None:
        security_workspace = load_workspace(ROOT / "examples" / "security")
        observability_workspace = load_workspace(ROOT / "examples" / "observability")
        deployment_workspace = load_workspace(ROOT / "examples" / "deployment")
        registry = load_pack_registry(security_workspace.pack_ids, security_workspace.pack_paths)

        self.assertEqual(
            FIXED_GENERATED_AT,
            generate_security_report(security_workspace, generated_at=FIXED_GENERATED_AT)["generatedAt"],
        )
        self.assertEqual(
            FIXED_GENERATED_AT,
            generate_observability_report(
                observability_workspace,
                generated_at=FIXED_GENERATED_AT,
            )["generatedAt"],
        )
        self.assertEqual(
            FIXED_GENERATED_AT,
            generate_validation_report(
                security_workspace,
                registry,
                [],
                generated_at=FIXED_GENERATED_AT,
            )["generatedAt"],
        )
        self.assertEqual(
            FIXED_GENERATED_AT,
            generate_roadmap_report(ROOT, generated_at=FIXED_GENERATED_AT)["generatedAt"],
        )
        self.assertEqual(
            FIXED_GENERATED_AT,
            generate_deployment_report(
                deployment_workspace,
                generated_at=FIXED_GENERATED_AT,
            )["generatedAt"],
        )
        self.assertEqual(
            FIXED_GENERATED_AT,
            generate_product_impact_report(
                load_workspace(PRODUCT_IMPACT_BASELINE),
                load_workspace(PRODUCT_IMPACT_CURRENT),
                generated_at=FIXED_GENERATED_AT,
            )["generatedAt"],
        )

    def test_generated_at_value_rejects_invalid_datetime(self) -> None:
        with self.assertRaisesRegex(ValueError, "ISO 8601"):
            generated_at_value("not-a-datetime")

    def test_security_report_matches_golden_file(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "security")
        expected = json.loads(SECURITY_REPORT_GOLDEN.read_text(encoding="utf-8"))

        report = generate_security_report(workspace)

        datetime.fromisoformat(report["generatedAt"])
        self.assertEqual(str(ROOT / "examples" / "security"), report["workspacePath"])
        self.assertIsInstance(report["verityVersion"], str)
        self.assertEqual(expected, normalize_security_report_for_golden(report))

    def test_observability_report_matches_golden_file(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "observability")
        expected = json.loads((OBSERVABILITY_GOLDEN / "observability_report.json").read_text(encoding="utf-8"))

        report = generate_observability_report(workspace)

        datetime.fromisoformat(report["generatedAt"])
        self.assertEqual(str(ROOT / "examples" / "observability"), report["workspacePath"])
        self.assertIsInstance(report["verityVersion"], str)
        self.assertEqual(expected, normalize_observability_report_for_golden(report))

    def test_observability_schema_bundle_matches_golden_file(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "observability")
        registry = load_pack_registry(workspace.pack_ids, workspace.pack_paths)
        expected = json.loads((OBSERVABILITY_GOLDEN / "schema_bundle.json").read_text(encoding="utf-8"))

        self.assertEqual(expected, generate_schema_bundle(registry))

    def test_accessibility_report_summarizes_accessibility_claims(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "accessibility")

        report = generate_accessibility_report(workspace)

        self.assertEqual("accessibility_report", report["type"])
        self.assertEqual(1, report["claimCount"])
        self.assertEqual({"checkout-platform": 1}, report["summary"]["byOwner"])
        self.assertEqual({"wcag-2.2": 1}, report["summary"]["byStandard"])
        self.assertEqual({"a": 1}, report["summary"]["byLevel"])
        self.assertEqual({"high": 1}, report["summary"]["byImpact"])
        self.assertEqual({"verified": 1}, report["summary"]["byCoverage"])
        self.assertEqual(1, report["summary"]["verifiedClaims"])
        self.assertEqual([], report["summary"]["criticalUnverified"])
        self.assertEqual(
            {
                "criticalUnverified": [],
                "claimsWithoutTargets": [],
                "missingOwners": [],
                "missingVerificationDates": [],
            },
            report["summary"]["releaseGaps"],
        )
        claim = report["claims"][0]
        self.assertEqual("accessibility.claim.checkout_keyboard", claim["id"])
        self.assertTrue(claim["verified"])
        self.assertEqual(
            ["product.accessible_checkout"],
            [target["id"] for target in claim["targets"]],
        )

    def test_compliance_matrix_summarizes_compliance_mappings(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "compliance")

        matrix = generate_compliance_matrix(workspace)

        self.assertEqual("compliance_matrix", matrix["type"])
        self.assertEqual(1, matrix["mappingCount"])
        self.assertEqual({"risk-and-compliance": 1}, matrix["summary"]["byOwner"])
        self.assertEqual({"internal-access-review": 1}, matrix["summary"]["byFramework"])
        self.assertEqual({"internal-access-review:IAR-1": 1}, matrix["summary"]["byRequirement"])
        self.assertEqual({"control": 1}, matrix["summary"]["byMappingType"])
        self.assertEqual({"reviewed": 1}, matrix["summary"]["byCoverage"])
        self.assertEqual(1, matrix["summary"]["verifiedMappings"])
        self.assertEqual(
            {
                "mappingsWithoutTargets": [],
                "mappingsWithoutEvidence": [],
                "reviewedUnverified": [],
                "missingOwners": [],
                "targetsWithoutOwners": [],
            },
            matrix["summary"]["releaseGaps"],
        )
        row = matrix["matrix"][0]
        self.assertEqual("compliance.mapping.checkout_access_review", row["id"])
        self.assertTrue(row["verified"])
        self.assertFalse(row["attestation"])
        self.assertEqual(
            [
                "security.control.checkout_access",
                "accessibility.claim.checkout_keyboard",
                "observability.metric.checkout_success_rate",
            ],
            [target["id"] for target in row["targets"]],
        )
        self.assertEqual(
            ["security.control.checkout_access"],
            [item["id"] for item in row["evidence"]["securityControls"]],
        )
        self.assertEqual(
            ["accessibility.claim.checkout_keyboard"],
            [item["id"] for item in row["evidence"]["accessibilityClaims"]],
        )
        self.assertEqual(
            ["observability.metric.checkout_success_rate"],
            [item["id"] for item in row["evidence"]["observabilitySignals"]],
        )

    def test_compliance_matrix_reports_release_gaps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "compliance-gaps",
                        "specVersion": "v0.1.0",
                        "packs": ["verity.core", "verity.pack.compliance"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "product.json").write_text(
                json.dumps(
                    {
                        "id": "product.unowned",
                        "kind": "product",
                        "name": "Unowned Product",
                        "description": "A product with placeholder ownership.",
                        "status": "ready",
                        "owner": "todo",
                        "version": "0.1.0",
                        "references": [],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "compliance.json").write_text(
                json.dumps(
                    {
                        "id": "compliance.mapping.unverified",
                        "kind": "compliance.mapping",
                        "name": "Unverified Mapping",
                        "description": "A reviewed mapping that still needs verification.",
                        "status": "ready",
                        "owner": "risk",
                        "framework": {
                            "name": "internal",
                            "requirementId": "INT-1",
                        },
                        "mappingType": "control",
                        "coverage": "reviewed",
                        "attestation": False,
                        "verification": {
                            "method": "not-verified",
                            "evidence": "Review has not run yet.",
                        },
                        "references": [
                            {
                                "type": "covers",
                                "target": "product.unowned",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            matrix = generate_compliance_matrix(workspace)

        self.assertEqual(0, matrix["summary"]["verifiedMappings"])
        self.assertEqual(
            ["compliance.mapping.unverified"],
            matrix["summary"]["releaseGaps"]["reviewedUnverified"],
        )
        self.assertEqual(
            ["product.unowned"],
            matrix["summary"]["releaseGaps"]["targetsWithoutOwners"],
        )

    def test_deployment_report_summarizes_targets_and_runtimes(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "deployment")

        report = generate_deployment_report(workspace)

        self.assertEqual("deployment_report", report["type"])
        self.assertEqual(1, report["targetCount"])
        self.assertEqual(1, report["runtimeCount"])
        self.assertEqual({"production": 1}, report["summary"]["byEnvironment"])
        self.assertEqual({"aws": 1}, report["summary"]["byProvider"])
        self.assertEqual({"kubernetes": 1}, report["summary"]["byPlatform"])
        self.assertEqual({"container": 1}, report["summary"]["runtimesByType"])
        self.assertEqual(
            {
                "targetsWithoutRuntime": [],
                "runtimesWithoutTargets": [],
                "productionWithoutApproval": [],
                "productionWithoutHealthChecks": [],
                "targetsWithoutRollbackPlan": [],
                "missingOwners": [],
            },
            report["summary"]["releaseGaps"],
        )
        self.assertEqual("deployment.target.checkout_production", report["targets"][0]["id"])
        self.assertEqual(
            "deployment.runtime.checkout_api",
            report["targets"][0]["runtime"]["id"],
        )

    def test_coverage_dashboard_summarizes_cross_pack_surfaces(self) -> None:
        workspace = load_workspace(COVERAGE_FIXTURE)

        report = generate_coverage_dashboard(workspace)

        self.assertEqual("coverage_dashboard", report["type"])
        self.assertEqual(14, report["recordCount"])
        self.assertEqual(1, report["productCount"])
        self.assertEqual(8, report["summary"]["trackedSurfaces"])
        self.assertEqual(8, report["summary"]["loadedSurfacePacks"])
        self.assertEqual(8, report["summary"]["coveredSurfaces"])
        self.assertEqual(100.0, report["summary"]["coveragePercent"])
        self.assertEqual(
            {
                "accessibility": 1,
                "api": 1,
                "cli": 1,
                "compliance": 1,
                "deployment": 2,
                "events": 1,
                "observability": 4,
                "security": 1,
            },
            report["summary"]["bySurface"],
        )
        self.assertEqual(
            {
                "missingSurfaceRecords": [],
                "loadedPacksWithoutSurfaceRecords": [],
                "productsWithoutSurfaceReferences": [],
                "productSurfaceGaps": [],
            },
            report["summary"]["releaseGaps"],
        )
        surfaces = {surface["id"]: surface for surface in report["surfaces"]}
        self.assertEqual("verity.pack.api", surfaces["api"]["packId"])
        self.assertEqual(["api.coverage.status"], [record["id"] for record in surfaces["api"]["records"]])
        self.assertEqual(
            ["deployment.runtime.coverage_api", "deployment.target.coverage_production"],
            [record["id"] for record in surfaces["deployment"]["records"]],
        )
        self.assertEqual([], report["products"][0]["missingSurfaces"])

    def test_pack_capability_index_summarizes_builtin_and_external_packs(self) -> None:
        workspace = load_workspace(CUSTOM_PACK_WORKSPACE)
        registry = load_pack_registry(workspace.pack_ids, workspace.pack_paths, workspace.base_path)

        report = generate_pack_capability_index(workspace, registry)

        self.assertEqual("pack_capability_index", report["type"])
        self.assertEqual(["verity.core", "verity.pack.features"], report["loadedPacks"])
        self.assertEqual(2, report["summary"]["packCount"])
        self.assertEqual(1, report["summary"]["builtInPackCount"])
        self.assertEqual(1, report["summary"]["externalPackCount"])
        self.assertEqual(3, report["summary"]["schemaCount"])
        self.assertEqual(3, report["summary"]["readinessGateCount"])
        self.assertEqual(5, report["summary"]["referenceRuleCount"])
        self.assertIn("pack-capability-index", report["summary"]["generators"])
        self.assertIn("schema-bundle", report["summary"]["generators"])
        schemas = {entry["kind"]: entry for entry in report["capabilities"]["schemas"]}
        self.assertEqual("verity.pack.features", schemas["feature.flag"]["packId"])
        gates = {entry["id"]: entry for entry in report["capabilities"]["readinessGates"]}
        self.assertEqual("feature.flag", gates["feature.flag.release"]["kind"])
        reference_rules = {
            (entry["sourceKind"], entry["relationship"], entry["targetKind"])
            for entry in report["capabilities"]["referenceRules"]
        }
        self.assertIn(("product", "configures", "feature.flag"), reference_rules)
        generator_index = {entry["id"]: entry for entry in report["capabilities"]["generators"]}
        self.assertIn("verity.core", generator_index["schema-bundle"]["packIds"])
        self.assertIn("verity.pack.features", generator_index["schema-bundle"]["packIds"])
        pack_details = {entry["id"]: entry for entry in report["packDetails"]}
        self.assertEqual("external", pack_details["verity.pack.features"]["source"])
        self.assertEqual(
            [
                {
                    "id": "schema-bundle",
                    "packId": "verity.pack.features",
                    "name": "",
                    "description": "",
                    "artifactType": "",
                    "outputFormats": [],
                    "recordKinds": [],
                }
            ],
            pack_details["verity.pack.features"]["generators"],
        )

    def test_pack_capability_index_matches_golden_file(self) -> None:
        workspace = load_workspace(CUSTOM_PACK_WORKSPACE)
        registry = load_pack_registry(workspace.pack_ids, workspace.pack_paths, workspace.base_path)
        expected = json.loads(PACK_CAPABILITY_INDEX_GOLDEN.read_text(encoding="utf-8"))

        report = generate_pack_capability_index(workspace, registry)

        datetime.fromisoformat(report["generatedAt"])
        self.assertEqual(str(CUSTOM_PACK_WORKSPACE), report["workspacePath"])
        self.assertIsInstance(report["verityVersion"], str)
        self.assertEqual(expected, normalize_pack_capability_index_for_golden(report))

    def test_coverage_dashboard_matches_golden_file(self) -> None:
        workspace = load_workspace(COVERAGE_FIXTURE)
        expected = json.loads(COVERAGE_DASHBOARD_GOLDEN.read_text(encoding="utf-8"))

        report = generate_coverage_dashboard(workspace)

        datetime.fromisoformat(report["generatedAt"])
        self.assertEqual(str(COVERAGE_FIXTURE), report["workspacePath"])
        self.assertIsInstance(report["verityVersion"], str)
        self.assertEqual(expected, normalize_coverage_dashboard_for_golden(report))

    def test_product_impact_report_expands_changed_record_graph(self) -> None:
        old_workspace = load_workspace(PRODUCT_IMPACT_BASELINE)
        new_workspace = load_workspace(PRODUCT_IMPACT_CURRENT)

        report = generate_product_impact_report(old_workspace, new_workspace)

        self.assertEqual("product_impact_report", report["type"])
        self.assertEqual(6, report["summary"]["changedRecordCount"])
        self.assertEqual(6, report["summary"]["impactedRecordCount"])
        self.assertEqual(0, report["summary"]["missingReferenceCount"])
        self.assertEqual("high", report["summary"]["releaseReview"]["riskLevel"])
        self.assertIn("breaking changes", report["summary"]["releaseReview"]["focus"])
        changed = {record["id"]: record for record in report["changedRecords"]}
        self.assertEqual("record.changed", changed["api.orders.list"]["changeType"])
        self.assertTrue(changed["api.orders.list"]["breaking"])
        self.assertEqual(
            ["product.orders", "security.control.order_access"],
            changed["api.orders.list"]["upstream"]["directRecordIds"],
        )
        self.assertEqual(
            ["event.orders.exported", "schema.order_list"],
            changed["api.orders.list"]["downstream"]["directRecordIds"],
        )
        self.assertEqual(
            ["api.orders.list", "product.orders", "security.control.order_access"],
            changed["schema.order_list"]["upstream"]["recordIds"],
        )
        self.assertEqual("baseline", changed["cli.orders.export"]["graphSource"])
        self.assertEqual(["product.orders"], changed["cli.orders.export"]["upstream"]["recordIds"])
        impacted = {record["id"]: record for record in report["impactedRecords"]}
        self.assertEqual(["upstream"], impacted["product.orders"]["directions"])
        self.assertIn("schema.order_list", impacted["product.orders"]["changedRecordIds"])

    def test_product_impact_report_detects_missing_references(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = root / "old"
            new = root / "new"
            (old / "records").mkdir(parents=True)
            (new / "records").mkdir(parents=True)
            config = {
                "workspace": "missing-reference-impact",
                "specVersion": "v0.2.0",
                "packs": ["verity.core"],
                "records": ["records/*.json"],
            }
            (old / "verityspec.json").write_text(json.dumps(config), encoding="utf-8")
            (new / "verityspec.json").write_text(json.dumps(config), encoding="utf-8")
            base_product = {
                "id": "product.missing_reference",
                "kind": "product",
                "name": "Missing Reference Product",
                "description": "Baseline product.",
                "status": "ready",
                "owner": "platform",
                "version": "0.1.0",
                "references": [],
            }
            current_product = {
                **base_product,
                "version": "0.2.0",
                "references": [{"type": "uses", "target": "schema.missing"}],
            }
            (old / "records" / "product.json").write_text(json.dumps(base_product), encoding="utf-8")
            (new / "records" / "product.json").write_text(json.dumps(current_product), encoding="utf-8")

            report = generate_product_impact_report(load_workspace(old), load_workspace(new))

        self.assertEqual(1, report["summary"]["missingReferenceCount"])
        self.assertEqual(
            {
                "source": "product.missing_reference",
                "target": "schema.missing",
                "relationship": "uses",
                "field": "references[0].target",
                "graphSource": "current",
            },
            report["missingReferences"][0],
        )

    def test_product_impact_report_matches_golden_file(self) -> None:
        old_workspace = load_workspace(PRODUCT_IMPACT_BASELINE)
        new_workspace = load_workspace(PRODUCT_IMPACT_CURRENT)
        expected = json.loads(PRODUCT_IMPACT_GOLDEN.read_text(encoding="utf-8"))
        expected.pop("validation", None)

        report = generate_product_impact_report(old_workspace, new_workspace)

        datetime.fromisoformat(report["generatedAt"])
        self.assertEqual(str(PRODUCT_IMPACT_BASELINE), report["oldWorkspace"]["workspacePath"])
        self.assertEqual(str(PRODUCT_IMPACT_CURRENT), report["newWorkspace"]["workspacePath"])
        self.assertIsInstance(report["verityVersion"], str)
        self.assertEqual(expected, normalize_product_impact_for_golden(report))

    def test_deployment_report_matches_golden_file(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "deployment")
        expected = json.loads(DEPLOYMENT_GOLDEN.read_text(encoding="utf-8"))

        report = generate_deployment_report(workspace)

        datetime.fromisoformat(report["generatedAt"])
        self.assertEqual(str(ROOT / "examples" / "deployment"), report["workspacePath"])
        self.assertIsInstance(report["verityVersion"], str)
        self.assertEqual(expected, normalize_deployment_report_for_golden(report))

    def test_deployment_readiness_requires_production_controls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "deployment-gaps",
                        "specVersion": "v0.1.0",
                        "packs": ["verity.core", "verity.pack.deployment"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "runtime.json").write_text(
                json.dumps(
                    {
                        "id": "deployment.runtime.api",
                        "kind": "deployment.runtime",
                        "name": "API Runtime",
                        "description": "Runtime under test.",
                        "status": "ready",
                        "owner": "platform",
                        "runtimeType": "container",
                        "runtimeName": "python",
                        "version": "3.12",
                        "artifactType": "container-image",
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "target.json").write_text(
                json.dumps(
                    {
                        "id": "deployment.target.production",
                        "kind": "deployment.target",
                        "name": "Production",
                        "description": "Production target missing release controls.",
                        "status": "ready",
                        "owner": "platform",
                        "environment": "production",
                        "provider": "aws",
                        "platform": "kubernetes",
                        "runtimeRef": "deployment.runtime.api",
                        "regions": ["us-east-1"],
                        "releasePolicy": {
                            "strategy": "rolling",
                            "approvalRequired": False,
                            "owner": "release-management",
                        },
                        "rollbackPlan": "docs/rollback.md",
                        "references": [],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertIn(
            "deployment.target.production_release_controls_missing",
            [issue.code for issue in issues],
        )


if __name__ == "__main__":
    unittest.main()
