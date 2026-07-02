from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from verityspec.generators import (
    generate_accessibility_report,
    generate_agent_context_markdown,
    generate_agent_context_report,
    generate_asyncapi,
    generate_compliance_matrix,
    generate_coverage_dashboard,
    generate_coverage_dashboard_markdown,
    generate_decision_index,
    generate_decision_index_markdown,
    generate_deployment_report,
    generate_issue_code_catalog,
    generate_issue_code_catalog_markdown,
    generate_lifecycle_readiness_report,
    generate_observability_report,
    generate_openapi,
    generate_pack_capability_index,
    generate_product_impact_report,
    generate_python_models,
    generate_roadmap_report,
    generate_roadmap_report_markdown,
    generate_schema_bundle,
    generate_security_report,
    generate_security_report_markdown,
    generate_typescript,
    generate_validation_report,
    generated_at_value,
)
from verityspec.envelope import RECORD_ENVELOPE_REQUIRED
from verityspec.explain import ISSUE_EXPLANATIONS
from verityspec.graph import build_graph
from verityspec.issues import Issue, escape_github_property, parse_issue_location
from verityspec.pack_validation import list_pack_summaries, validate_builtin_packs, validate_packs
from verityspec.pack_diagnostics import diagnose_pack_discovery
from verityspec.packs import PACK_ENTRY_POINT_GROUP, load_pack_registry
from verityspec.profiles import PROFILES, profile_issues
from verityspec.readiness import evaluate_readiness
from verityspec.validation import validate_workspace
from verityspec.workspace import load_workspace


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_FIXTURE = ROOT / "tests" / "fixtures" / "generator_maturity"
GENERATOR_GOLDEN = ROOT / "tests" / "golden" / "generator_maturity"
SECURITY_REPORT_GOLDEN = ROOT / "tests" / "golden" / "security_report" / "security_report.json"
SECURITY_REPORT_MARKDOWN_GOLDEN = (
    ROOT / "tests" / "golden" / "security_report" / "security_report.md"
)
OBSERVABILITY_GOLDEN = ROOT / "tests" / "golden" / "observability"
ACCESSIBILITY_REPORT_GOLDEN = (
    ROOT / "tests" / "golden" / "accessibility_report" / "accessibility_report.json"
)
COMPLIANCE_MATRIX_GOLDEN = (
    ROOT / "tests" / "golden" / "compliance_matrix" / "compliance_matrix.json"
)
DEPLOYMENT_GOLDEN = ROOT / "tests" / "golden" / "deployment" / "deployment_report.json"
COVERAGE_DASHBOARD_GOLDEN = (
    ROOT / "tests" / "golden" / "coverage_dashboard" / "coverage_dashboard.json"
)
COVERAGE_DASHBOARD_MARKDOWN_GOLDEN = (
    ROOT / "tests" / "golden" / "coverage_dashboard" / "coverage_dashboard.md"
)
DECISION_INDEX_GOLDEN = ROOT / "tests" / "golden" / "decision_index" / "decision_index.json"
DECISION_INDEX_MARKDOWN_GOLDEN = (
    ROOT / "tests" / "golden" / "decision_index" / "decision_index.md"
)
COVERAGE_FIXTURE = ROOT / "tests" / "fixtures" / "cross_pack_coverage"
CUSTOM_PACK_WORKSPACE = ROOT / "tests" / "fixtures" / "custom_pack_workspace"
CUSTOM_PACK = ROOT / "tests" / "fixtures" / "custom_pack"
PACK_CAPABILITY_INDEX_GOLDEN = (
    ROOT / "tests" / "golden" / "pack_capability_index" / "pack_capability_index.json"
)
ISSUE_CODE_CATALOG_GOLDEN = (
    ROOT / "tests" / "golden" / "issue_code_catalog" / "issue_code_catalog.json"
)
ISSUE_CODE_CATALOG_MARKDOWN_GOLDEN = (
    ROOT / "tests" / "golden" / "issue_code_catalog" / "issue_code_catalog.md"
)
AGENT_CONTEXT_MARKDOWN_GOLDEN = (
    ROOT / "tests" / "golden" / "agent_context" / "agent_context.md"
)
PRODUCT_IMPACT_BASELINE = ROOT / "tests" / "fixtures" / "product_impact" / "baseline"
PRODUCT_IMPACT_CURRENT = ROOT / "tests" / "fixtures" / "product_impact" / "current"
PRODUCT_IMPACT_GOLDEN = ROOT / "tests" / "golden" / "product_impact" / "product_impact.json"
LIFECYCLE_READINESS_EXAMPLE = ROOT / "examples" / "lifecycle-readiness"
LIFECYCLE_READINESS_GOLDEN = (
    ROOT / "tests" / "golden" / "lifecycle_readiness" / "lifecycle_readiness_report.json"
)
WORKSPACE_DEPENDENCY_FIXTURES = ROOT / "tests" / "fixtures" / "workspace_dependencies"
FIXED_GENERATED_AT = "2026-01-02T03:04:05Z"


class FakeEntryPoint:
    def __init__(self, name: str, pack_path: Path) -> None:
        self.name = name
        self._pack_path = pack_path

    def load(self):
        return lambda: self._pack_path


class BrokenEntryPoint:
    def __init__(self, name: str) -> None:
        self.name = name
        self.value = "broken.module:pack_path"

    def load(self):
        raise RuntimeError("entry point exploded")


class FakeEntryPoints(list):
    def select(self, **params):
        group = params.get("group")
        if group == PACK_ENTRY_POINT_GROUP:
            return list(self)
        return []


def normalize_security_report_for_golden(report: dict) -> dict:
    normalized = dict(report)
    normalized["generatedAt"] = "<generatedAt>"
    normalized["verityVersion"] = "<verityVersion>"
    normalized["workspacePath"] = "<workspacePath>"
    return normalized


def normalize_security_report_for_markdown_golden(report: dict) -> dict:
    normalized = normalize_security_report_for_golden(report)
    return normalized


def normalize_observability_report_for_golden(report: dict) -> dict:
    normalized = dict(report)
    normalized["generatedAt"] = "<generatedAt>"
    normalized["verityVersion"] = "<verityVersion>"
    normalized["workspacePath"] = "<workspacePath>"
    return normalized


def normalize_accessibility_report_for_golden(report: dict) -> dict:
    normalized = dict(report)
    normalized["generatedAt"] = "<generatedAt>"
    normalized["verityVersion"] = "<verityVersion>"
    normalized["workspacePath"] = "<workspacePath>"
    return normalized


def normalize_compliance_matrix_for_golden(report: dict) -> dict:
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


def normalize_lifecycle_readiness_report_for_golden(report: dict) -> dict:
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


def normalize_coverage_dashboard_for_markdown_golden(report: dict) -> dict:
    normalized = normalize_coverage_dashboard_for_golden(report)
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


def normalize_issue_code_catalog_for_golden(report: dict) -> dict:
    normalized = dict(report)
    normalized["generatedAt"] = "<generatedAt>"
    normalized["verityVersion"] = "<verityVersion>"
    return normalized


def normalize_issue_code_catalog_for_markdown_golden(report: dict) -> dict:
    return normalize_issue_code_catalog_for_golden(report)


def normalize_agent_context_for_markdown_golden(report: dict) -> dict:
    normalized = dict(report)
    workspace_path = report["workspacePath"]
    normalized["generatedAt"] = "<generatedAt>"
    normalized["verityVersion"] = "<verityVersion>"
    normalized["workspacePath"] = "<workspacePath>"
    normalized["verificationCommands"] = [
        command.replace(workspace_path, "<workspacePath>")
        for command in report["verificationCommands"]
    ]
    return normalized


def normalize_decision_index_for_golden(report: dict) -> dict:
    normalized = dict(report)
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

    def test_installed_pack_discovery_loads_entry_point_pack_without_pack_paths(self) -> None:
        entry_points = FakeEntryPoints([FakeEntryPoint("verity.pack.features", CUSTOM_PACK)])
        with tempfile.TemporaryDirectory() as tmp, patch(
            "verityspec.packs.metadata.entry_points",
            return_value=entry_points,
        ):
            root = Path(tmp)
            records = root / "records"
            records.mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "installed.pack.workspace",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.features"],
                        "packPaths": [],
                        "records": ["records/*.json"],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (records / "product.json").write_text(
                json.dumps(
                    {
                        "id": "product.flags",
                        "kind": "product",
                        "name": "Feature Flag Product",
                        "description": "A product fixture that loads an installed pack.",
                        "status": "ready",
                        "owner": "platform",
                        "version": "0.1.0",
                        "references": [{"type": "configures", "target": "feature.checkout"}],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (records / "feature.checkout.json").write_text(
                json.dumps(
                    {
                        "id": "feature.checkout",
                        "kind": "feature.flag",
                        "name": "Checkout Feature",
                        "description": "Controls access to the checkout flow.",
                        "status": "ready",
                        "owner": "growth",
                        "key": "checkout.enabled",
                        "enabled": True,
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids, workspace.pack_paths, workspace.base_path)

        self.assertEqual("installed", registry.packs["verity.pack.features"].source)
        self.assertEqual([], validate_workspace(workspace, registry, strict=True))
        self.assertEqual([], evaluate_readiness(workspace, registry, strict=True))

    def test_installed_pack_list_and_validate_include_installed_source(self) -> None:
        entry_points = FakeEntryPoints([FakeEntryPoint("verity.pack.features", CUSTOM_PACK)])
        with patch("verityspec.packs.metadata.entry_points", return_value=entry_points):
            summaries = list_pack_summaries()
            issues = validate_packs("verity.pack.features")

        installed = [summary for summary in summaries if summary["id"] == "verity.pack.features"]
        self.assertEqual(1, len(installed))
        self.assertEqual("installed", installed[0]["source"])
        self.assertEqual([], issues)

    def test_local_pack_path_takes_precedence_over_installed_pack(self) -> None:
        entry_points = FakeEntryPoints([FakeEntryPoint("verity.pack.features", CUSTOM_PACK)])
        with patch("verityspec.packs.metadata.entry_points", return_value=entry_points):
            summaries = list_pack_summaries([CUSTOM_PACK])

        features = [summary for summary in summaries if summary["id"] == "verity.pack.features"]
        self.assertEqual(1, len(features))
        self.assertEqual("external", features[0]["source"])

    def test_installed_pack_entry_point_name_must_match_manifest_id(self) -> None:
        entry_points = FakeEntryPoints([FakeEntryPoint("verity.pack.wrong", CUSTOM_PACK)])
        with patch("verityspec.packs.metadata.entry_points", return_value=entry_points):
            with self.assertRaisesRegex(ValueError, "must match manifest id"):
                list_pack_summaries()

    def test_pack_discovery_diagnostics_reports_clean_state(self) -> None:
        with patch("verityspec.packs.metadata.entry_points", return_value=FakeEntryPoints()):
            report, issues = diagnose_pack_discovery()

        self.assertTrue(report["passed"])
        self.assertEqual([], issues)
        self.assertEqual("verityspec.packs", report["entryPointGroup"])
        self.assertGreater(report["summary"]["builtInPackCount"], 0)
        self.assertEqual(0, report["summary"]["installedEntryPointCount"])

    def test_pack_discovery_diagnostics_reports_entry_point_load_failures(self) -> None:
        entry_points = FakeEntryPoints([BrokenEntryPoint("verity.pack.broken")])
        with patch("verityspec.packs.metadata.entry_points", return_value=entry_points):
            report, issues = diagnose_pack_discovery()

        self.assertFalse(report["passed"])
        self.assertEqual(["pack.installed.entry_point_load_failed"], [issue.code for issue in issues])
        self.assertEqual("error", report["installedEntryPoints"][0]["status"])

    def test_pack_discovery_diagnostics_reports_duplicate_installed_pack_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first_pack = Path(tmp) / "features-one"
            second_pack = Path(tmp) / "features-two"
            shutil.copytree(CUSTOM_PACK, first_pack)
            shutil.copytree(CUSTOM_PACK, second_pack)
            entry_points = FakeEntryPoints(
                [
                    FakeEntryPoint("verity.pack.features", first_pack),
                    FakeEntryPoint("verity.pack.features", second_pack),
                ]
            )
            with patch("verityspec.packs.metadata.entry_points", return_value=entry_points):
                report, issues = diagnose_pack_discovery()

        self.assertFalse(report["passed"])
        self.assertIn("pack.installed.duplicate_id", [issue.code for issue in issues])
        self.assertEqual(2, report["summary"]["installedEntryPointCount"])

    def test_pack_discovery_diagnostics_reports_builtin_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack_path = Path(tmp) / "core-collision"
            shutil.copytree(CUSTOM_PACK, pack_path)
            manifest_path = pack_path / "pack.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["id"] = "verity.core"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            entry_points = FakeEntryPoints([FakeEntryPoint("verity.core", pack_path)])
            with patch("verityspec.packs.metadata.entry_points", return_value=entry_points):
                report, issues = diagnose_pack_discovery()

        self.assertFalse(report["passed"])
        self.assertIn("pack.installed.builtin_collision", [issue.code for issue in issues])
        self.assertEqual("error", report["installedEntryPoints"][0]["status"])

    def test_pack_discovery_diagnostics_reports_external_override_behavior(self) -> None:
        entry_points = FakeEntryPoints([FakeEntryPoint("verity.pack.features", CUSTOM_PACK)])
        with patch("verityspec.packs.metadata.entry_points", return_value=entry_points):
            report, issues = diagnose_pack_discovery([CUSTOM_PACK])

        self.assertTrue(report["passed"])
        self.assertEqual(["pack.external.overrides_installed"], [issue.code for issue in issues])
        self.assertEqual("warning", report["externalPacks"][0]["status"])
        self.assertEqual(1, report["summary"]["overrideCount"])
        self.assertEqual("verity.pack.features", report["overrides"][0]["packId"])

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

    def test_local_workspace_dependency_references_exported_records(self) -> None:
        workspace = load_workspace(WORKSPACE_DEPENDENCY_FIXTURES / "consumer")
        registry = load_pack_registry(workspace.pack_ids, workspace.pack_paths, workspace.base_path)

        self.assertEqual([], validate_workspace(workspace, registry, strict=True))
        self.assertEqual([], evaluate_readiness(workspace, registry, strict=True))

    def test_dependency_aware_graph_includes_exported_dependency_records(self) -> None:
        workspace = load_workspace(WORKSPACE_DEPENDENCY_FIXTURES / "consumer")

        graph = build_graph(workspace)

        dependency_nodes = {
            node["id"]: node
            for node in graph["nodes"]
            if node.get("workspaceRole") == "dependency"
        }
        self.assertIn("sharedUnity::unity.package.save_system", dependency_nodes)
        self.assertEqual(
            "studio.library.shared_unity_runtime",
            dependency_nodes["sharedUnity::unity.package.save_system"]["dependencyWorkspace"],
        )
        self.assertEqual(
            [
                {
                    "id": "studio.library.shared_unity_runtime",
                    "alias": "sharedUnity",
                    "source": "../shared-unity-runtime",
                    "version": "1.2.0",
                    "exportedRecords": ["unity.package.save_system"],
                }
            ],
            graph["dependencies"],
        )
        self.assertIn(
            {
                "source": "unity.project.dream_extraction",
                "target": "sharedUnity::unity.package.save_system",
                "relationship": "usesPackage",
                "field": "references[0].target",
            },
            graph["edges"],
        )

    def test_workspace_dependency_reference_failures_have_stable_codes(self) -> None:
        expected_codes = {
            "private-reference": "dependency.reference.not_exported",
            "missing-record": "dependency.reference.missing",
            "unknown-alias": "dependency.alias.unknown",
            "missing-source": "dependency.source.missing",
            "id-mismatch": "dependency.id.mismatch",
        }

        for fixture, expected_code in expected_codes.items():
            with self.subTest(fixture=fixture):
                workspace = load_workspace(WORKSPACE_DEPENDENCY_FIXTURES / fixture)
                registry = load_pack_registry(workspace.pack_ids, workspace.pack_paths, workspace.base_path)

                issues = validate_workspace(workspace, registry, strict=True)

                self.assertEqual([expected_code], [issue.code for issue in issues])

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
        self.assertEqual(
            {
                "criticalUnverified": [],
                "staleEvidence": [],
                "missingVerificationDates": [],
            },
            report["summary"]["releaseGaps"],
        )
        control = report["controls"][0]
        self.assertEqual("security.control.account_access", control["id"])
        self.assertTrue(control["verified"])
        self.assertEqual(
            ["api.accounts.get", "schema.account"],
            [target["id"] for target in control["targets"]],
        )

    def test_security_report_distinguishes_stale_and_missing_verification_dates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stale_root = Path(tmp) / "stale"
            stale_root.mkdir()
            stale_date = (date.today() - timedelta(days=31)).isoformat()
            write_security_freshness_workspace(stale_root, stale_date, cadence_days=30)

            missing_root = Path(tmp) / "missing"
            missing_root.mkdir()
            write_security_freshness_workspace(missing_root, None, cadence_days=30)

            stale_report = generate_security_report(load_workspace(stale_root))
            missing_report = generate_security_report(load_workspace(missing_root))

        self.assertEqual(
            ["security.control.session_review"],
            stale_report["summary"]["releaseGaps"]["staleEvidence"],
        )
        self.assertEqual([], stale_report["summary"]["releaseGaps"]["missingVerificationDates"])
        self.assertEqual([], missing_report["summary"]["releaseGaps"]["staleEvidence"])
        self.assertEqual(
            ["security.control.session_review"],
            missing_report["summary"]["releaseGaps"]["missingVerificationDates"],
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

    def test_roadmap_report_markdown_summarizes_release_governance(self) -> None:
        report = generate_roadmap_report(ROOT, generated_at=FIXED_GENERATED_AT)
        markdown = generate_roadmap_report_markdown(report)

        self.assertTrue(markdown.startswith("# VeritySpec Roadmap Report\n"))
        self.assertIn(f"- Generated: `{FIXED_GENERATED_AT}`", markdown)
        self.assertIn("## Summary", markdown)
        self.assertIn("| Next roadmap points | 20 |", markdown)
        self.assertIn("## Recent Milestones", markdown)
        self.assertIn("## Recent Sprint Rows", markdown)
        self.assertIn("## Next 20 Roadmap Points", markdown)
        self.assertIn("1. Add downstream CI profile artifact guidance", markdown)
        self.assertIn(
            "20. Add golden-fixture refresh automation dry-run implementation",
            markdown,
        )

    def test_roadmap_report_treats_focused_milestone_as_active(self) -> None:
        roadmap = """# Roadmap

## v0.1.0

The `v0.1.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 1 | Complete | First sprint |

## v0.2.0

The `v0.2.0` milestone is focused on active work.

| Sprint | Status | Focus |
|---:|---|---|
| 2 | In Progress | Active sprint |

## Next 20 Roadmap Points

1. Add the next thing.
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ROADMAP.md"
            path.write_text(roadmap, encoding="utf-8")
            report = generate_roadmap_report(path, generated_at=FIXED_GENERATED_AT)

        self.assertEqual("v0.1.0", report["latestReleasedMilestone"])
        self.assertEqual(["v0.2.0"], report["activeMilestones"])
        self.assertEqual(1, report["summary"]["activeMilestones"])

    def test_report_generators_accept_explicit_generated_at(self) -> None:
        security_workspace = load_workspace(ROOT / "examples" / "security")
        observability_workspace = load_workspace(ROOT / "examples" / "observability")
        deployment_workspace = load_workspace(ROOT / "examples" / "deployment")
        lifecycle_workspace = load_workspace(LIFECYCLE_READINESS_EXAMPLE)
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
            generate_issue_code_catalog(generated_at=FIXED_GENERATED_AT)["generatedAt"],
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
            generate_lifecycle_readiness_report(
                lifecycle_workspace,
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
        self.assertEqual(
            FIXED_GENERATED_AT,
            generate_agent_context_report(
                load_workspace(ROOT / "examples" / "product-delivery"),
                "agent-context.exporter.implementation_bundle",
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

    def test_security_report_markdown_matches_golden_file(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "security")
        expected = SECURITY_REPORT_MARKDOWN_GOLDEN.read_text(encoding="utf-8")

        report = generate_security_report(workspace, generated_at=FIXED_GENERATED_AT)
        markdown = generate_security_report_markdown(
            normalize_security_report_for_markdown_golden(report)
        )

        self.assertTrue(markdown.startswith("# VeritySpec Security Report\n"))
        self.assertIn("## Summary", markdown)
        self.assertIn("## Coverage", markdown)
        self.assertIn("## Risk Levels", markdown)
        self.assertIn("## Release Gaps", markdown)
        self.assertIn("## Security Controls", markdown)
        self.assertIn("does not make legal, compliance", markdown)
        self.assertEqual(expected, markdown)

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

    def test_accessibility_report_matches_golden_file(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "accessibility")
        expected = json.loads(ACCESSIBILITY_REPORT_GOLDEN.read_text(encoding="utf-8"))

        report = generate_accessibility_report(workspace)

        datetime.fromisoformat(report["generatedAt"])
        self.assertEqual(str(ROOT / "examples" / "accessibility"), report["workspacePath"])
        self.assertIsInstance(report["verityVersion"], str)
        self.assertEqual(expected, normalize_accessibility_report_for_golden(report))

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

    def test_compliance_matrix_matches_golden_file(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "compliance")
        expected = json.loads(COMPLIANCE_MATRIX_GOLDEN.read_text(encoding="utf-8"))

        matrix = generate_compliance_matrix(workspace)

        datetime.fromisoformat(matrix["generatedAt"])
        self.assertEqual(str(ROOT / "examples" / "compliance"), matrix["workspacePath"])
        self.assertIsInstance(matrix["verityVersion"], str)
        self.assertEqual(expected, normalize_compliance_matrix_for_golden(matrix))

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
                "productionWithoutSecurityControls": [],
                "productionWithoutObservability": [],
                "productionWithoutComplianceMapping": [],
                "productionWithoutReleaseEvidence": [],
                "missingOwners": [],
            },
            report["summary"]["releaseGaps"],
        )
        self.assertEqual("deployment.target.checkout_production", report["targets"][0]["id"])
        self.assertEqual(
            ["security.control.checkout_access"],
            [item["id"] for item in report["targets"][0]["securityControls"]],
        )
        self.assertEqual(
            ["observability.dashboard.checkout_delivery"],
            [item["id"] for item in report["targets"][0]["observabilityDashboards"]],
        )
        self.assertEqual(
            ["compliance.mapping.checkout_delivery"],
            [item["id"] for item in report["targets"][0]["complianceMappings"]],
        )
        self.assertEqual(
            [
                "evidence.ci-run.checkout_release",
                "evidence.qa.checkout_release",
                "evidence.artifact.checkout_release_manifest",
            ],
            [item["id"] for item in report["targets"][0]["releaseEvidence"]],
        )
        self.assertEqual("success", report["targets"][0]["releaseEvidence"][0]["evidenceStatus"])
        self.assertEqual(
            "deployment.runtime.checkout_api",
            report["targets"][0]["runtime"]["id"],
        )

    def test_coverage_dashboard_summarizes_cross_pack_surfaces(self) -> None:
        workspace = load_workspace(COVERAGE_FIXTURE)

        report = generate_coverage_dashboard(workspace)

        self.assertEqual("coverage_dashboard", report["type"])
        self.assertEqual(127, report["recordCount"])
        self.assertEqual(1, report["productCount"])
        self.assertEqual(21, report["summary"]["trackedSurfaces"])
        self.assertEqual(21, report["summary"]["loadedSurfacePacks"])
        self.assertEqual(21, report["summary"]["coveredSurfaces"])
        self.assertEqual(100.0, report["summary"]["coveragePercent"])
        self.assertEqual(
            {
                "accessibility": 1,
                "api": 1,
                "cli": 1,
                "compliance": 1,
                "content": 4,
                "deployment": 2,
                "evidence": 10,
                "economy": 5,
                "events": 1,
                "game-assets": 4,
                "game-core": 4,
                "gameplay": 4,
                "godot": 14,
                "liveops": 9,
                "mobile": 12,
                "observability": 4,
                "product-delivery": 17,
                "progression": 5,
                "security": 1,
                "unity": 12,
                "unreal": 13,
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
        self.assertEqual("verity.pack.content", surfaces["content"]["packId"])
        self.assertEqual("verity.pack.economy", surfaces["economy"]["packId"])
        self.assertEqual("verity.pack.evidence", surfaces["evidence"]["packId"])
        self.assertEqual("verity.pack.game-assets", surfaces["game-assets"]["packId"])
        self.assertEqual("verity.pack.game-core", surfaces["game-core"]["packId"])
        self.assertEqual("verity.pack.gameplay", surfaces["gameplay"]["packId"])
        self.assertEqual("verity.pack.godot", surfaces["godot"]["packId"])
        self.assertEqual("verity.pack.liveops", surfaces["liveops"]["packId"])
        self.assertEqual("verity.pack.mobile", surfaces["mobile"]["packId"])
        self.assertEqual("verity.pack.product-delivery", surfaces["product-delivery"]["packId"])
        self.assertEqual("verity.pack.progression", surfaces["progression"]["packId"])
        self.assertEqual("verity.pack.unity", surfaces["unity"]["packId"])
        self.assertEqual("verity.pack.unreal", surfaces["unreal"]["packId"])
        self.assertEqual(["api.coverage.status"], [record["id"] for record in surfaces["api"]["records"]])
        self.assertEqual(
            [
                "game.loop.coverage_status",
                "game.mode.coverage_coop",
                "game.product.coverage_adventure",
                "game.prototype-scope.coverage_slice",
            ],
            [record["id"] for record in surfaces["game-core"]["records"]],
        )
        self.assertEqual(
            ["deployment.runtime.coverage_api", "deployment.target.coverage_production"],
            [record["id"] for record in surfaces["deployment"]["records"]],
        )
        self.assertEqual(
            [
                "game.concept-art.coverage_zone",
                "game.gdd-source.coverage_pitch",
                "game.identity-image.coverage_key_art",
                "game.visual-identity.coverage_style",
            ],
            [record["id"] for record in surfaces["game-assets"]["records"]],
        )
        self.assertEqual(
            [
                "game.ability.coverage_dash",
                "game.encounter.coverage_portal",
                "game.mechanic.coverage_shards",
                "game.rule.coverage_collapse",
            ],
            [record["id"] for record in surfaces["gameplay"]["records"]],
        )
        self.assertEqual(
            [
                "game.content-item.coverage_shard",
                "game.content-manifest.coverage_slice",
                "game.level.coverage_zone",
                "game.loot-table.coverage_rewards",
            ],
            [record["id"] for record in surfaces["content"]["records"]],
        )
        self.assertEqual(
            [
                "economy.currency.coverage_shard",
                "economy.offer.coverage_cache",
                "economy.reward.coverage_extract",
                "economy.sink.coverage_upgrade",
                "economy.source.coverage_extract",
            ],
            [record["id"] for record in surfaces["economy"]["records"]],
        )
        self.assertEqual(
            [
                "progression.gate.coverage_currency",
                "progression.level.coverage_1",
                "progression.track.coverage_mastery",
                "progression.unlock.coverage_dash",
                "progression.xp-model.coverage_session",
            ],
            [record["id"] for record in surfaces["progression"]["records"]],
        )
        self.assertEqual(
            [
                "agent-context.exporter.coverage_agent_context",
                "archive.policy.coverage_archive",
                "commercial.posture.coverage_private_alpha",
                "decision.record.coverage_truth_layer",
                "decommission.policy.coverage_sunset",
                "editor.surface.coverage_dashboard",
                "evidence.requirement.coverage_ci",
                "generator.capability.coverage_schema_bundle",
                "maintenance.policy.coverage_active",
                "operations.model.coverage_maintained",
                "product.scope.coverage_delivery",
                "project-management.model.coverage_github",
                "readiness.profile.coverage_private_alpha",
                "release.process.coverage_release",
                "scanner.capability.coverage_contract_scan",
                "support.policy.coverage_support",
                "validation.runner.coverage_ci",
            ],
            [record["id"] for record in surfaces["product-delivery"]["records"]],
        )
        self.assertEqual(
            [
                "mobile.app-release.coverage_soft_launch",
                "mobile.apple-privacy-details.coverage_apple",
                "mobile.att-consent.coverage_att",
                "mobile.compatibility-matrix.coverage_devices",
                "mobile.entitlement.coverage_remove_ads",
                "mobile.google-play-data-safety.coverage_google",
                "mobile.launch-candidate.coverage_candidate",
                "mobile.monetization-posture.coverage_monetization",
                "mobile.privacy-policy.coverage_policy",
                "mobile.sdk-inventory.coverage_sdks",
                "mobile.soft-launch.coverage_market",
                "mobile.store-listing.coverage_listing",
            ],
            [record["id"] for record in surfaces["mobile"]["records"]],
        )
        self.assertEqual(
            [
                "liveops.analytics-taxonomy.coverage_events",
                "liveops.archive-handling.coverage_archive",
                "liveops.config.coverage_live",
                "liveops.data-deletion-policy.coverage_deletion",
                "liveops.decommission-plan.coverage_sunset",
                "liveops.remote-config.coverage_bounds",
                "liveops.rollback-plan.coverage_rollback",
                "liveops.save-migration-policy.coverage_save_v2",
                "liveops.support-category.coverage_support",
            ],
            [record["id"] for record in surfaces["liveops"]["records"]],
        )
        self.assertEqual(
            [
                "evidence.artifact.coverage_manifest",
                "evidence.build.coverage_wheel",
                "evidence.certification-checklist.coverage_mobile",
                "evidence.ci-run.coverage_ci",
                "evidence.playtest.coverage_progression",
                "evidence.qa.coverage_release",
                "evidence.review.coverage_decision",
                "evidence.screenshot.coverage_dashboard",
                "evidence.test.coverage_contracts",
                "evidence.video.coverage_walkthrough",
            ],
            [record["id"] for record in surfaces["evidence"]["records"]],
        )
        self.assertEqual(
            [
                "godot.addon.coverage_tools",
                "godot.agent-context-exporter.coverage_context",
                "godot.autoload.coverage_registry",
                "godot.export-preset.coverage_pc",
                "godot.input-action.coverage_interact",
                "godot.node-contract.coverage_avatar",
                "godot.project.coverage_adventure",
                "godot.readiness-dashboard.coverage_prototype",
                "godot.resource.coverage_shard_icon",
                "godot.scanner.coverage_contracts",
                "godot.scene.coverage_zone",
                "godot.script.coverage_controller",
                "godot.shared-library.coverage_runtime",
                "godot.validation-runner.coverage_contracts",
            ],
            [record["id"] for record in surfaces["godot"]["records"]],
        )
        self.assertEqual(
            [
                "unity.agent-context-exporter.coverage_context",
                "unity.asmdef.coverage_runtime",
                "unity.build-target.coverage_pc",
                "unity.package-dependency.coverage_input",
                "unity.package.coverage_input",
                "unity.prefab.coverage_avatar",
                "unity.project.coverage_adventure",
                "unity.readiness-dashboard.coverage_prototype",
                "unity.scanner.coverage_contracts",
                "unity.scene.coverage_zone",
                "unity.shared-library.coverage_runtime",
                "unity.validation-runner.coverage_contracts",
            ],
            [record["id"] for record in surfaces["unity"]["records"]],
        )
        self.assertEqual(
            [
                "unreal.agent-context-exporter.coverage_context",
                "unreal.blueprint.coverage_avatar",
                "unreal.data-asset.coverage_shard",
                "unreal.gameplay-tag.coverage_shard",
                "unreal.input-action.coverage_interact",
                "unreal.map.coverage_zone",
                "unreal.module.coverage_runtime",
                "unreal.plugin.coverage_tools",
                "unreal.project.coverage_adventure",
                "unreal.readiness-dashboard.coverage_prototype",
                "unreal.scanner.coverage_contracts",
                "unreal.target.coverage_pc",
                "unreal.validation-runner.coverage_contracts",
            ],
            [record["id"] for record in surfaces["unreal"]["records"]],
        )
        self.assertEqual([], report["products"][0]["missingSurfaces"])

    def test_mobile_and_liveops_project_reference_rules_keep_engine_parity(self) -> None:
        registry = load_pack_registry(
            [
                "verity.pack.mobile",
                "verity.pack.liveops",
            ]
        )
        rules = {
            (rule.source_kind, rule.relationship, rule.target_kind)
            for rule in registry.reference_rules
        }

        for engine_kind in ["unity.project", "godot.project", "unreal.project"]:
            with self.subTest(engine_kind=engine_kind):
                self.assertIn(
                    (engine_kind, "targetsMobileRelease", "mobile.app-release"),
                    rules,
                )
                self.assertIn(
                    (engine_kind, "usesLiveOpsConfig", "liveops.config"),
                    rules,
                )

    def test_evidence_reference_rules_keep_engine_traceability_parity(self) -> None:
        registry = load_pack_registry(
            [
                "verity.pack.evidence",
                "verity.pack.unity",
                "verity.pack.godot",
                "verity.pack.unreal",
            ]
        )
        rules = {
            (rule.source_kind, rule.relationship, rule.target_kind)
            for rule in registry.reference_rules
        }

        for engine_kind in [
            "unity.project",
            "unity.scene",
            "godot.project",
            "godot.scene",
            "unreal.project",
            "unreal.map",
        ]:
            with self.subTest(engine_kind=engine_kind):
                self.assertIn(("evidence.test", "proves", engine_kind), rules)

        for build_kind in [
            "unity.build-target",
            "godot.export-preset",
            "unreal.target",
        ]:
            with self.subTest(build_kind=build_kind):
                self.assertIn(("evidence.test", "proves", build_kind), rules)
                self.assertIn(("evidence.build", "proves", build_kind), rules)

        runtime_links = [
            ("unity.validation-runner", "unity.build-target"),
            ("godot.validation-runner", "godot.export-preset"),
            ("unreal.validation-runner", "unreal.target"),
        ]
        for runner_kind, runtime_kind in runtime_links:
            with self.subTest(runner_kind=runner_kind, runtime_kind=runtime_kind):
                self.assertIn((runner_kind, "producesEvidence", "evidence.test"), rules)
                self.assertIn((runner_kind, "validatesRuntime", runtime_kind), rules)

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

    def test_issue_code_catalog_summarizes_explain_metadata(self) -> None:
        report = generate_issue_code_catalog()

        self.assertEqual("issue_code_catalog", report["type"])
        self.assertEqual("verity explain", report["source"])
        self.assertEqual(len(ISSUE_EXPLANATIONS), report["summary"]["issueCodeCount"])
        self.assertIn("reference", report["summary"]["categories"])
        self.assertIn("error", report["summary"]["severities"])
        issue_codes = {entry["code"]: entry for entry in report["issueCodes"]}
        self.assertEqual(set(ISSUE_EXPLANATIONS), set(issue_codes))
        self.assertEqual("reference", issue_codes["reference.missing"]["category"])
        self.assertEqual("Missing reference target", issue_codes["reference.missing"]["title"])
        self.assertEqual(
            ISSUE_EXPLANATIONS["reference.missing"]["resolution"],
            issue_codes["reference.missing"]["resolution"],
        )

    def test_issue_code_catalog_matches_golden_file(self) -> None:
        expected = json.loads(ISSUE_CODE_CATALOG_GOLDEN.read_text(encoding="utf-8"))

        report = generate_issue_code_catalog()

        datetime.fromisoformat(report["generatedAt"])
        self.assertIsInstance(report["verityVersion"], str)
        self.assertEqual(expected, normalize_issue_code_catalog_for_golden(report))

    def test_issue_code_catalog_markdown_matches_golden_file(self) -> None:
        expected = ISSUE_CODE_CATALOG_MARKDOWN_GOLDEN.read_text(encoding="utf-8")

        report = generate_issue_code_catalog(generated_at=FIXED_GENERATED_AT)
        markdown = generate_issue_code_catalog_markdown(
            normalize_issue_code_catalog_for_markdown_golden(report)
        )

        self.assertTrue(markdown.startswith("# VeritySpec Issue Code Catalog\n"))
        self.assertIn("## Summary", markdown)
        self.assertIn("## Severities", markdown)
        self.assertIn("## Categories", markdown)
        self.assertIn("## Issue Codes", markdown)
        self.assertIn(
            "| reference.missing | reference | error | Missing reference target |",
            markdown,
        )
        self.assertIn("JSON output remains the machine-readable contract", markdown)
        self.assertEqual(expected, markdown)

    def test_coverage_dashboard_matches_golden_file(self) -> None:
        workspace = load_workspace(COVERAGE_FIXTURE)
        expected = json.loads(COVERAGE_DASHBOARD_GOLDEN.read_text(encoding="utf-8"))

        report = generate_coverage_dashboard(workspace)

        datetime.fromisoformat(report["generatedAt"])
        self.assertEqual(str(COVERAGE_FIXTURE), report["workspacePath"])
        self.assertIsInstance(report["verityVersion"], str)
        self.assertEqual(expected, normalize_coverage_dashboard_for_golden(report))

    def test_coverage_dashboard_markdown_matches_golden_file(self) -> None:
        workspace = load_workspace(COVERAGE_FIXTURE)
        expected = COVERAGE_DASHBOARD_MARKDOWN_GOLDEN.read_text(encoding="utf-8")

        report = generate_coverage_dashboard(workspace, generated_at=FIXED_GENERATED_AT)
        markdown = generate_coverage_dashboard_markdown(
            normalize_coverage_dashboard_for_markdown_golden(report)
        )

        self.assertTrue(markdown.startswith("# VeritySpec Coverage Dashboard\n"))
        self.assertIn("## Summary", markdown)
        self.assertIn("## Release Gaps", markdown)
        self.assertIn("## Surface Coverage", markdown)
        self.assertIn("## Product Surface References", markdown)
        self.assertIn("does not make legal, commercial", markdown)
        self.assertEqual(expected, markdown)

    def test_decision_index_summarizes_product_delivery_decisions(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "product-delivery")

        report = generate_decision_index(workspace, generated_at=FIXED_GENERATED_AT)

        self.assertEqual("decision_index", report["type"])
        self.assertEqual(FIXED_GENERATED_AT, report["generatedAt"])
        self.assertEqual(1, report["decisionCount"])
        self.assertEqual(1, report["summary"]["acceptedDecisionCount"])
        self.assertEqual({"accepted": 1}, report["summary"]["byDecisionStatus"])
        self.assertEqual({"operations": 1}, report["summary"]["byDecisionType"])
        self.assertEqual([], report["summary"]["indexGaps"]["acceptedWithoutDecidedAt"])
        self.assertEqual([], report["summary"]["indexGaps"]["orphanedDecisions"])
        self.assertEqual("decision.record.github_manages_workflow", report["decisions"][0]["id"])
        self.assertEqual(1, report["decisions"][0]["graphLinkCount"])
        self.assertIn(
            {
                "source": "project-management.model.github_native",
                "target": "decision.record.github_manages_workflow",
                "relationship": "recordsDecision",
                "field": "references[0].target",
            },
            report["graphLinks"],
        )

    def test_decision_index_matches_golden_file(self) -> None:
        expected = json.loads(DECISION_INDEX_GOLDEN.read_text(encoding="utf-8"))
        workspace = load_workspace(ROOT / "examples" / "product-delivery")

        report = generate_decision_index(workspace, generated_at=FIXED_GENERATED_AT)

        self.assertEqual(expected, normalize_decision_index_for_golden(report))

    def test_decision_index_markdown_matches_golden_file(self) -> None:
        expected = DECISION_INDEX_MARKDOWN_GOLDEN.read_text(encoding="utf-8")
        workspace = load_workspace(ROOT / "examples" / "product-delivery")

        report = generate_decision_index(workspace, generated_at=FIXED_GENERATED_AT)
        markdown = generate_decision_index_markdown(
            normalize_decision_index_for_golden(report)
        )

        self.assertTrue(markdown.startswith("# VeritySpec Decision Index\n"))
        self.assertIn("## Index Gaps", markdown)
        self.assertIn("decision.record.github_manages_workflow", markdown)
        self.assertIn("does not approve decisions", markdown)
        self.assertEqual(expected, markdown)

    def test_decision_index_generator_is_advertised_by_product_delivery_pack(self) -> None:
        registry = load_pack_registry(["verity.pack.product-delivery"])
        pack = registry.packs["verity.pack.product-delivery"]
        generator = next(
            item
            for item in pack.generator_metadata
            if item.get("id") == "decision-index"
        )

        self.assertIn("decision-index", pack.generators)
        self.assertEqual(["json", "markdown"], generator["outputFormats"])
        self.assertEqual(["decision.record"], generator["recordKinds"])

    def test_agent_context_report_summarizes_target_and_graph_records(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "product-delivery")

        report = generate_agent_context_report(
            workspace,
            "agent-context.exporter.implementation_bundle",
            generated_at=FIXED_GENERATED_AT,
        )

        self.assertEqual("agent_context", report["type"])
        self.assertEqual(FIXED_GENERATED_AT, report["generatedAt"])
        self.assertEqual("agent-context.exporter.implementation_bundle", report["target"]["id"])
        self.assertEqual("agent-context.exporter", report["target"]["kind"])
        self.assertEqual("markdown", report["target"]["exporterType"])
        record_ids = {record["id"] for record in report["records"]}
        for record_id in [
            "product.scope.engine_toolkit_delivery",
            "release.process.tagged_alpha",
            "readiness.profile.private_alpha",
            "evidence.requirement.local_ci",
            "validation.runner.local_ci",
            "decision.record.github_manages_workflow",
        ]:
            with self.subTest(record_id=record_id):
                self.assertIn(record_id, record_ids)

        self.assertEqual(report["summary"]["recordCount"], len(report["records"]))
        self.assertEqual(report["summary"]["graphEdgeCount"], len(report["graphEdges"]))
        self.assertIn(
            {
                "source": "agent-context.exporter.implementation_bundle",
                "target": "product.scope.engine_toolkit_delivery",
                "relationship": "describesScope",
                "field": "references[0].target",
            },
            report["graphEdges"],
        )
        self.assertIn("build/agent-context.md", report["generatedArtifacts"])
        self.assertTrue(any("AGENTS.md" in boundary for boundary in report["safetyBoundaries"]))
        self.assertTrue(
            any(
                "verity generate agent-context" in command
                and "--record agent-context.exporter.implementation_bundle" in command
                for command in report["verificationCommands"]
            )
        )

    def test_agent_context_report_accepts_engine_exporter_targets(self) -> None:
        workspace = load_workspace(COVERAGE_FIXTURE)

        for target_id, expected_kind in [
            ("unity.agent-context-exporter.coverage_context", "unity.agent-context-exporter"),
            ("godot.agent-context-exporter.coverage_context", "godot.agent-context-exporter"),
            ("unreal.agent-context-exporter.coverage_context", "unreal.agent-context-exporter"),
        ]:
            with self.subTest(target_id=target_id):
                report = generate_agent_context_report(
                    workspace,
                    target_id,
                    generated_at=FIXED_GENERATED_AT,
                )
                self.assertEqual(expected_kind, report["target"]["kind"])
                self.assertGreaterEqual(report["summary"]["recordCount"], 1)

    def test_agent_context_generators_are_advertised_by_product_and_engine_packs(self) -> None:
        registry = load_pack_registry(
            [
                "verity.pack.product-delivery",
                "verity.pack.unity",
                "verity.pack.godot",
                "verity.pack.unreal",
            ]
        )
        expectations = {
            "verity.pack.product-delivery": "agent-context.exporter",
            "verity.pack.unity": "unity.agent-context-exporter",
            "verity.pack.godot": "godot.agent-context-exporter",
            "verity.pack.unreal": "unreal.agent-context-exporter",
        }

        for pack_id, target_kind in expectations.items():
            with self.subTest(pack_id=pack_id):
                pack = registry.packs[pack_id]
                generator = next(
                    item
                    for item in pack.generator_metadata
                    if item.get("id") == "agent-context"
                )
                self.assertIn("agent-context", pack.generators)
                self.assertEqual(["markdown"], generator["outputFormats"])
                self.assertEqual([target_kind], generator["recordKinds"])

    def test_agent_context_markdown_matches_golden_file(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "product-delivery")
        expected = AGENT_CONTEXT_MARKDOWN_GOLDEN.read_text(encoding="utf-8")

        report = generate_agent_context_report(
            workspace,
            "agent-context.exporter.implementation_bundle",
            generated_at=FIXED_GENERATED_AT,
        )
        markdown = generate_agent_context_markdown(
            normalize_agent_context_for_markdown_golden(report)
        )

        self.assertTrue(markdown.startswith("# VeritySpec Agent Context\n"))
        self.assertIn("## Target Exporter", markdown)
        self.assertIn("## Verification Commands", markdown)
        self.assertIn("AGENTS.md remains the canonical repository entry point", markdown)
        self.assertEqual(expected, markdown)

    def test_agent_context_report_rejects_unknown_target(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "product-delivery")

        with self.assertRaisesRegex(ValueError, "target record not found"):
            generate_agent_context_report(
                workspace,
                "agent-context.exporter.missing",
                generated_at=FIXED_GENERATED_AT,
            )

    def test_agent_context_report_rejects_unsupported_target_kind(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "product-delivery")

        with self.assertRaisesRegex(ValueError, "target must be one of"):
            generate_agent_context_report(
                workspace,
                "product.scope.engine_toolkit_delivery",
                generated_at=FIXED_GENERATED_AT,
            )

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

    def test_lifecycle_readiness_report_summarizes_complete_stages(self) -> None:
        workspace = load_workspace(LIFECYCLE_READINESS_EXAMPLE)

        report = generate_lifecycle_readiness_report(workspace, generated_at=FIXED_GENERATED_AT)

        self.assertEqual("lifecycle_readiness_report", report["type"])
        self.assertEqual(3, report["summary"]["trackedSurfaces"])
        self.assertEqual(3, report["summary"]["loadedLifecyclePacks"])
        self.assertEqual(10, report["summary"]["completeStages"])
        self.assertEqual(0, report["summary"]["stagesWithGaps"])
        self.assertEqual(0, report["summary"]["gapCount"])
        self.assertIn("does not assert commercial", report["claimBoundaries"][1])
        self.assertEqual(
            ["productDelivery", "mobile", "liveOps"],
            [surface["id"] for surface in report["surfaces"]],
        )
        self.assertEqual(
            "implementation-ready",
            report["stages"][0]["id"],
        )

    def test_lifecycle_readiness_report_summarizes_missing_lifecycle_kinds(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "product-delivery")

        report = generate_lifecycle_readiness_report(workspace, generated_at=FIXED_GENERATED_AT)

        self.assertEqual("gaps", report["stages"][1]["coverageStatus"])
        self.assertGreater(report["summary"]["gapCount"], 0)
        self.assertIn("mobile.app-release", report["stages"][1]["missingKinds"])
        self.assertEqual(
            {
                "stageId": "soft-launch",
                "reason": "missing-kind",
                "kind": "mobile.app-release",
                "message": "Soft Launch has no mobile.app-release record.",
            },
            report["gaps"][0],
        )

    def test_lifecycle_readiness_report_matches_golden_file(self) -> None:
        workspace = load_workspace(LIFECYCLE_READINESS_EXAMPLE)
        expected = json.loads(LIFECYCLE_READINESS_GOLDEN.read_text(encoding="utf-8"))

        report = generate_lifecycle_readiness_report(workspace)

        datetime.fromisoformat(report["generatedAt"])
        self.assertEqual(str(LIFECYCLE_READINESS_EXAMPLE), report["workspacePath"])
        self.assertIsInstance(report["verityVersion"], str)
        self.assertEqual(expected, normalize_lifecycle_readiness_report_for_golden(report))

    def test_deployment_readiness_requires_production_evidence_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "test.deployment.evidence.links",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.deployment"],
                        "packPaths": [],
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
                        "description": "Runtime for deployment evidence link checks.",
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
                        "description": "Production target missing evidence links.",
                        "status": "ready",
                        "owner": "platform",
                        "environment": "production",
                        "provider": "aws",
                        "platform": "kubernetes",
                        "runtimeRef": "deployment.runtime.api",
                        "securityControlRefs": [],
                        "observabilityDashboardRefs": [],
                        "complianceMappingRefs": [],
                        "releaseEvidenceRefs": [],
                        "regions": ["us-east-1"],
                        "healthCheckUrl": "https://example.com/healthz",
                        "releasePolicy": {
                            "strategy": "rolling",
                            "approvalRequired": True,
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
        self.assertEqual("deployment.target.production", issues[0].record_id)

    def test_deployment_release_evidence_reference_must_resolve(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "test.deployment.missing.evidence",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.deployment", "verity.pack.evidence"],
                        "packPaths": [],
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
                        "description": "Runtime for missing release evidence checks.",
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
                        "description": "Production target with an unresolved release evidence reference.",
                        "status": "ready",
                        "owner": "platform",
                        "environment": "production",
                        "provider": "aws",
                        "platform": "kubernetes",
                        "runtimeRef": "deployment.runtime.api",
                        "releaseEvidenceRefs": ["evidence.ci-run.missing"],
                        "regions": ["us-east-1"],
                        "healthCheckUrl": "https://example.com/healthz",
                        "releasePolicy": {
                            "strategy": "rolling",
                            "approvalRequired": True,
                            "owner": "release-management",
                        },
                        "rollbackPlan": "docs/rollback.md",
                        "references": [
                            {
                                "type": "releaseEvidence",
                                "target": "evidence.ci-run.missing",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = validate_workspace(workspace, registry)

        self.assertIn("reference.missing", [issue.code for issue in issues])

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

    def test_game_core_readiness_requires_product_contract_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "game-core-gaps",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.game-core"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "game-product.json").write_text(
                json.dumps(
                    {
                        "id": "game.product.missing_links",
                        "kind": "game.product",
                        "name": "Missing Links",
                        "description": "Game product missing graph links.",
                        "status": "ready",
                        "owner": "game-design",
                        "pitch": "A small fixture game.",
                        "playerFantasy": "Players prove readiness gaps.",
                        "targetAudience": "Maintainers.",
                        "targetPlatforms": ["pc"],
                        "references": [],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertIn("readiness.min_items", [issue.code for issue in issues])
        self.assertIn("game.product.missing_links", [issue.record_id for issue in issues])

    def test_game_assets_readiness_requires_visual_identity_asset_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "game-assets-gaps",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.game-core", "verity.pack.game-assets"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "visual-identity.json").write_text(
                json.dumps(
                    {
                        "id": "game.visual-identity.missing_assets",
                        "kind": "game.visual-identity",
                        "name": "Missing Assets",
                        "description": "Visual identity missing linked asset records.",
                        "status": "ready",
                        "owner": "art-direction",
                        "tone": "Readable.",
                        "artDirection": "Small fixture.",
                        "styleKeywords": ["readable"],
                        "references": [],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertIn("readiness.min_items", [issue.code for issue in issues])
        self.assertIn("game.visual-identity.missing_assets", [issue.record_id for issue in issues])

    def test_gameplay_readiness_requires_mechanic_handoff_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "gameplay-gaps",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.gameplay"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "mechanic.json").write_text(
                json.dumps(
                    {
                        "id": "game.mechanic.missing_handoff",
                        "kind": "game.mechanic",
                        "name": "Missing Handoff",
                        "description": "Gameplay mechanic missing implementation handoff details.",
                        "status": "ready",
                        "owner": "game-design",
                        "mechanicType": "resource",
                        "summary": "A mechanic without enough handoff detail.",
                        "inputs": [],
                        "outputs": [],
                        "references": [],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertIn("readiness.min_items", [issue.code for issue in issues])
        self.assertIn("game.mechanic.missing_handoff", [issue.record_id for issue in issues])

    def test_content_readiness_requires_manifest_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "content-gaps",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.content"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "manifest.json").write_text(
                json.dumps(
                    {
                        "id": "game.content-manifest.missing_links",
                        "kind": "game.content-manifest",
                        "name": "Missing Links",
                        "description": "Content manifest missing content and graph links.",
                        "status": "ready",
                        "owner": "production",
                        "manifestType": "vertical-slice",
                        "scope": "Small fixture scope.",
                        "contentVersion": "0.1.0",
                        "contentRefs": [],
                        "references": [],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertIn("readiness.min_items", [issue.code for issue in issues])
        self.assertIn("game.content-manifest.missing_links", [issue.record_id for issue in issues])

    def test_economy_readiness_requires_offer_reward_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "economy-gaps",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.economy"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "offer.json").write_text(
                json.dumps(
                    {
                        "id": "economy.offer.missing_links",
                        "kind": "economy.offer",
                        "name": "Missing Links",
                        "description": "Economy offer missing reward and graph links.",
                        "status": "ready",
                        "owner": "economy-design",
                        "offerType": "prototype",
                        "priceCurrencyRef": "economy.currency.test",
                        "priceAmount": 0,
                        "rewardRefs": [],
                        "availability": {
                            "state": "prototype",
                        },
                        "references": [],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertIn("readiness.min_items", [issue.code for issue in issues])
        self.assertIn("economy.offer.missing_links", [issue.record_id for issue in issues])

    def test_unity_readiness_requires_project_contract_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "unity-gaps",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.unity"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "project.json").write_text(
                json.dumps(
                    {
                        "id": "unity.project.missing_links",
                        "kind": "unity.project",
                        "name": "Missing Links",
                        "description": "Unity project missing package, scene, and build-target references.",
                        "status": "ready",
                        "owner": "unity-engineering",
                        "unityVersion": "2022.3 LTS",
                        "projectPath": "unity/MissingLinks",
                        "renderPipeline": "urp",
                        "scriptingBackend": "il2cpp",
                        "targetPlatforms": ["pc"],
                        "references": [],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertIn("readiness.min_items", [issue.code for issue in issues])
        self.assertIn("unity.project.missing_links", [issue.record_id for issue in issues])

    def test_unity_readiness_requires_validation_runner_scanner_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "unity-tooling-gaps",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.unity"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "runner.json").write_text(
                json.dumps(
                    {
                        "id": "unity.validation-runner.missing_scanners",
                        "kind": "unity.validation-runner",
                        "name": "Missing Scanner Links",
                        "description": "Unity validation runner missing scanner and graph links.",
                        "status": "ready",
                        "owner": "unity-engineering",
                        "runnerType": "ci",
                        "command": "unity -batchmode -executeMethod Validate.Run",
                        "scannerRefs": [],
                        "references": [
                            {
                                "type": "runsScanner",
                                "target": "unity.scanner.missing",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertIn(
            "readiness.validation_runner.scanner_refs_required",
            [issue.code for issue in issues],
        )
        self.assertIn("unity.validation-runner.missing_scanners", [issue.record_id for issue in issues])

    def test_godot_readiness_requires_validation_runner_scanner_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "godot-tooling-gaps",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.godot"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "runner.json").write_text(
                json.dumps(
                    {
                        "id": "godot.validation-runner.missing_scanners",
                        "kind": "godot.validation-runner",
                        "name": "Missing Scanner Links",
                        "description": "Godot validation runner missing scanner and graph links.",
                        "status": "ready",
                        "owner": "godot-engineering",
                        "runnerType": "ci",
                        "command": "godot --headless --script addons/contracts/run_validation.gd",
                        "scannerRefs": [],
                        "references": [
                            {
                                "type": "runsScanner",
                                "target": "godot.scanner.missing",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertIn(
            "readiness.validation_runner.scanner_refs_required",
            [issue.code for issue in issues],
        )
        self.assertIn("godot.validation-runner.missing_scanners", [issue.record_id for issue in issues])

    def test_unreal_readiness_requires_validation_runner_scanner_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "unreal-tooling-gaps",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.unreal"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "runner.json").write_text(
                json.dumps(
                    {
                        "id": "unreal.validation-runner.missing_scanners",
                        "kind": "unreal.validation-runner",
                        "name": "Missing Scanner Links",
                        "description": "Unreal validation runner missing scanner and graph links.",
                        "status": "ready",
                        "owner": "unreal-engineering",
                        "runnerType": "ci",
                        "command": "UnrealEditor-Cmd.exe Project.uproject -run=Contracts",
                        "scannerRefs": [],
                        "references": [
                            {
                                "type": "runsScanner",
                                "target": "unreal.scanner.missing",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertIn(
            "readiness.validation_runner.scanner_refs_required",
            [issue.code for issue in issues],
        )
        self.assertIn("unreal.validation-runner.missing_scanners", [issue.record_id for issue in issues])

    def test_engine_device_smoke_validation_runners_do_not_require_scanner_refs(self) -> None:
        cases = [
            (
                "unity",
                "verity.pack.unity",
                "unity.validation-runner",
                "unity.build-target.runtime",
            ),
            (
                "godot",
                "verity.pack.godot",
                "godot.validation-runner",
                "godot.export-preset.runtime",
            ),
            (
                "unreal",
                "verity.pack.unreal",
                "unreal.validation-runner",
                "unreal.target.runtime",
            ),
        ]
        for engine, pack_id, kind, target in cases:
            with self.subTest(engine=engine):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "records").mkdir()
                    (root / "verityspec.json").write_text(
                        json.dumps(
                            {
                                "workspace": f"{engine}-device-smoke",
                                "specVersion": "v0.2.0",
                                "packs": ["verity.core", pack_id],
                                "records": ["records/*.json"],
                            }
                        ),
                        encoding="utf-8",
                    )
                    records = [
                        {
                            "id": f"{kind}.without_scanner_refs",
                            "kind": kind,
                            "name": "Device Smoke Runner Without Scanner Refs",
                            "description": "Device-smoke runner that validates a built runtime artifact directly.",
                            "status": "ready",
                            "owner": f"{engine}-engineering",
                            "runnerType": "device-smoke",
                            "command": "tools/run_device_smoke.sh",
                            "references": [
                                {
                                    "type": "validatesRuntime",
                                    "target": target,
                                }
                            ],
                        },
                        {
                            "id": f"{kind}.empty_scanner_refs",
                            "kind": kind,
                            "name": "Device Smoke Runner With Empty Scanner Refs",
                            "description": "Device-smoke runner that explicitly declares no scanner records.",
                            "status": "ready",
                            "owner": f"{engine}-engineering",
                            "runnerType": "device-smoke",
                            "command": "tools/run_device_smoke.sh",
                            "scannerRefs": [],
                            "references": [
                                {
                                    "type": "validatesRuntime",
                                    "target": target,
                                }
                            ],
                        },
                    ]
                    (root / "records" / "runners.json").write_text(
                        json.dumps({"records": records}),
                        encoding="utf-8",
                    )

                    workspace = load_workspace(root)
                    registry = load_pack_registry(workspace.pack_ids)
                    validation_issues = validate_workspace(workspace, registry)
                    readiness_issues = evaluate_readiness(workspace, registry, strict=True)

                self.assertNotIn("schema.validation", [issue.code for issue in validation_issues])
                self.assertNotIn(
                    "readiness.validation_runner.scanner_refs_required",
                    [issue.code for issue in readiness_issues],
                )

    def test_product_delivery_readiness_requires_validation_runner_scanner_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "product-delivery-gaps",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.product-delivery"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "runner.json").write_text(
                json.dumps(
                    {
                        "id": "validation.runner.missing_scanners",
                        "kind": "validation.runner",
                        "name": "Missing Scanner Refs",
                        "description": "Product-delivery validation runner missing scanner references.",
                        "status": "ready",
                        "owner": "tooling",
                        "runnerType": "ci",
                        "command": "verity validate",
                        "scannerRefs": [],
                        "references": [
                            {
                                "type": "runsScanner",
                                "target": "scanner.capability.missing",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertIn("readiness.required", [issue.code for issue in issues])
        self.assertIn("validation.runner.missing_scanners", [issue.record_id for issue in issues])

    def test_mobile_readiness_requires_app_release_contract_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "mobile-gaps",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.mobile"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "release.json").write_text(
                json.dumps(
                    {
                        "id": "mobile.app-release.missing_links",
                        "kind": "mobile.app-release",
                        "name": "Missing Links",
                        "description": "Mobile app release missing store, privacy, SDK, launch, and compatibility links.",
                        "status": "ready",
                        "owner": "mobile-release",
                        "releaseStage": "soft-launch",
                        "releaseTrack": "testflight",
                        "platformTargets": ["ios"],
                        "versionName": "0.5.0",
                        "references": [],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertIn("readiness.min_items", [issue.code for issue in issues])
        self.assertIn("mobile.app-release.missing_links", [issue.record_id for issue in issues])

    def test_liveops_readiness_requires_config_contract_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "liveops-gaps",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.liveops"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "config.json").write_text(
                json.dumps(
                    {
                        "id": "liveops.config.missing_links",
                        "kind": "liveops.config",
                        "name": "Missing Links",
                        "description": "LiveOps config missing remote config, rollback, analytics, support, and lifecycle links.",
                        "status": "ready",
                        "owner": "liveops",
                        "configType": "remote-config",
                        "environment": "production",
                        "ownerTeam": "liveops",
                        "references": [],
                    }
                ),
                encoding="utf-8",
            )

            workspace = load_workspace(root)
            registry = load_pack_registry(workspace.pack_ids)
            issues = evaluate_readiness(workspace, registry, strict=True)

        self.assertIn("readiness.min_items", [issue.code for issue in issues])
        self.assertIn("liveops.config.missing_links", [issue.record_id for issue in issues])


if __name__ == "__main__":
    unittest.main()
