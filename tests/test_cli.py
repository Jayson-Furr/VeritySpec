from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from verityspec import __version__


ROOT = Path(__file__).resolve().parents[1]
CUSTOM_PACK = "tests/fixtures/custom_pack"
CUSTOM_PACK_WORKSPACE = "tests/fixtures/custom_pack_workspace"
UNITY_EXTENSION_MIRROR = "tests/fixtures/official_extension_mirrors/verityspec-pack-unity/pack"
MIGRATION_FIXTURES = ROOT / "tests" / "fixtures" / "migration"
SECURITY_REPORT_GOLDEN = ROOT / "tests" / "golden" / "security_report" / "security_report.json"
OBSERVABILITY_GOLDEN = ROOT / "tests" / "golden" / "observability"
ACCESSIBILITY_REPORT_GOLDEN = (
    ROOT / "tests" / "golden" / "accessibility_report" / "accessibility_report.json"
)
COMPLIANCE_MATRIX_GOLDEN = (
    ROOT / "tests" / "golden" / "compliance_matrix" / "compliance_matrix.json"
)
DEPLOYMENT_GOLDEN = ROOT / "tests" / "golden" / "deployment" / "deployment_report.json"
EVIDENCE_REPORT_GOLDEN = ROOT / "tests" / "golden" / "evidence_report" / "evidence_report.json"
LIFECYCLE_READINESS_GOLDEN = (
    ROOT / "tests" / "golden" / "lifecycle_readiness" / "lifecycle_readiness_report.json"
)
COVERAGE_DASHBOARD_GOLDEN = (
    ROOT / "tests" / "golden" / "coverage_dashboard" / "coverage_dashboard.json"
)
DECISION_INDEX_GOLDEN = ROOT / "tests" / "golden" / "decision_index" / "decision_index.json"
COVERAGE_FIXTURE = "tests/fixtures/cross_pack_coverage"
PACK_CAPABILITY_INDEX_GOLDEN = (
    ROOT / "tests" / "golden" / "pack_capability_index" / "pack_capability_index.json"
)
PRODUCT_IMPACT_BASELINE = "tests/fixtures/product_impact/baseline"
PRODUCT_IMPACT_CURRENT = "tests/fixtures/product_impact/current"
PRODUCT_IMPACT_GOLDEN = ROOT / "tests" / "golden" / "product_impact" / "product_impact.json"
LIFECYCLE_READINESS_EXAMPLE = "examples/lifecycle-readiness"
FIXED_GENERATED_AT = "2026-01-02T03:04:05Z"
DEFAULT_BUILTIN_PACKS = [
    "verity.core",
    "verity.pack.api",
    "verity.pack.cli",
    "verity.pack.events",
]


def verity_command(*args: str) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-m", "verityspec", *args],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def snapshot_files(path: Path) -> dict[str, str]:
    return {
        str(item.relative_to(path)): item.read_text(encoding="utf-8")
        for item in sorted(path.rglob("*"))
        if item.is_file()
    }


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True)


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


def normalize_evidence_report_for_golden(report: dict) -> dict:
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


def normalize_decision_index_for_golden(report: dict) -> dict:
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


class VerityCliTests(unittest.TestCase):
    def test_version_command(self) -> None:
        result = verity_command("--version")

        self.assertEqual(0, result.returncode)
        self.assertIn(f"verity {__version__}", result.stdout)

    def test_validate_json_output(self) -> None:
        result = verity_command("validate", "examples/basic", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual("validate", payload["command"])
        self.assertEqual({"errors": 0, "warnings": 0, "issues": 0}, payload["summary"])
        self.assertEqual([], payload["issues"])

    def test_readiness_json_output(self) -> None:
        result = verity_command("readiness", "examples/basic", "--strict", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual("readiness", payload["command"])

    def test_validate_release_profile_json_output(self) -> None:
        result = verity_command("validate", "examples/basic", "--profile", "release", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual("release", payload["profile"]["id"])
        self.assertTrue(payload["profile"]["effectiveStrict"])
        self.assertEqual("error", payload["profile"]["effectiveFailOn"])

    def test_regulated_profile_requires_governance_packs(self) -> None:
        result = verity_command("validate", "examples/basic", "--profile", "regulated", "--format", "json")

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        issue_codes = [issue["code"] for issue in payload["issues"]]
        self.assertEqual("regulated", payload["profile"]["id"])
        self.assertEqual(3, issue_codes.count("profile.required_pack"))
        for pack_id in [
            "verity.pack.security",
            "verity.pack.accessibility",
            "verity.pack.compliance",
        ]:
            with self.subTest(pack_id=pack_id):
                self.assertIn(pack_id, canonical_json(payload["issues"]))

    def test_public_api_profile_requires_api_scope(self) -> None:
        result = verity_command("validate", "examples/cli-tool", "--profile", "public-api", "--format", "json")

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        issue_codes = {issue["code"] for issue in payload["issues"]}
        self.assertEqual("public-api", payload["profile"]["id"])
        self.assertIn("profile.required_pack", issue_codes)
        self.assertIn("profile.required_record_kind", issue_codes)

    def test_internal_tool_profile_keeps_warnings_advisory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "internal-tool",
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
                        "id": "product.internal_tool",
                        "kind": "product",
                        "name": "Internal Tool",
                        "description": "A small internal tool contract.",
                        "status": "ready",
                        "owner": "platform",
                        "version": "0.1.0",
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "schema.json").write_text(
                json.dumps(
                    {
                        "id": "schema.unused",
                        "kind": "schema.object",
                        "name": "Unused Schema",
                        "description": "Unused by design.",
                        "status": "ready",
                        "owner": "platform",
                        "jsonSchema": {"type": "object", "properties": {}},
                    }
                ),
                encoding="utf-8",
            )

            result = verity_command("validate", str(root), "--profile", "internal-tool", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual("internal-tool", payload["profile"]["id"])
        self.assertFalse(payload["profile"]["effectiveStrict"])
        self.assertEqual(1, payload["summary"]["warnings"])

    def test_doctor_json_output(self) -> None:
        result = verity_command("doctor", "examples/basic", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual("doctor", payload["command"])
        self.assertEqual(8, payload["records"])

    def test_doctor_profile_json_output(self) -> None:
        result = verity_command("doctor", "examples/basic", "--profile", "public-api", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual("doctor", payload["command"])
        self.assertEqual("public-api", payload["profile"]["id"])

    def test_doctor_report_out_writes_json_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "reports" / "doctor-report.json"
            result = verity_command(
                "doctor",
                "examples/basic",
                "--report-out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertIn("Doctor passed.", result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual("doctor", payload["command"])
        self.assertEqual(8, payload["records"])
        self.assertEqual({"errors": 0, "warnings": 0, "issues": 0}, payload["summary"])

    def test_doctor_report_out_preserves_json_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "doctor-report.json"
            result = verity_command(
                "doctor",
                "examples/basic",
                "--format",
                "json",
                "--report-out",
                str(out_path),
            )

            stdout_payload = json.loads(result.stdout)
            file_payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertEqual(stdout_payload, file_payload)
        self.assertTrue(file_payload["passed"])

    def test_explain_issue_code_json_output(self) -> None:
        result = verity_command("explain", "reference.missing", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("reference.missing", payload["code"])
        self.assertEqual("Missing reference target", payload["title"])

    def test_issue_code_catalog_generator_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "issue-code-catalog.json"
            result = verity_command(
                "generate",
                "issue-code-catalog",
                "--generated-at",
                FIXED_GENERATED_AT,
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertIn("Generated issue-code-catalog", result.stdout)
        self.assertEqual("issue_code_catalog", payload["type"])
        self.assertEqual(FIXED_GENERATED_AT, payload["generatedAt"])
        self.assertGreater(payload["summary"]["issueCodeCount"], 0)
        self.assertIn("reference.missing", {item["code"] for item in payload["issueCodes"]})

    def test_issue_code_catalog_generator_writes_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "issue-code-catalog.md"
            result = verity_command(
                "generate",
                "issue-code-catalog",
                "--format",
                "markdown",
                "--generated-at",
                FIXED_GENERATED_AT,
                "--out",
                str(out_path),
            )

            text = out_path.read_text(encoding="utf-8")

        self.assertEqual(0, result.returncode)
        self.assertIn("Generated issue-code-catalog", result.stdout)
        self.assertTrue(text.startswith("# VeritySpec Issue Code Catalog\n"))
        self.assertIn(f"- Generated: `{FIXED_GENERATED_AT}`", text)
        self.assertIn("## Summary", text)
        self.assertIn("## Issue Codes", text)
        self.assertIn(
            "| reference.missing | reference | error | Missing reference target |",
            text,
        )

    def test_issue_code_catalog_matches_explain_metadata_for_sampled_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "issue-code-catalog.json"
            catalog_result = verity_command(
                "generate",
                "issue-code-catalog",
                "--out",
                str(out_path),
            )
            explain_result = verity_command("explain", "reference.missing", "--format", "json")

            catalog = json.loads(out_path.read_text(encoding="utf-8"))
            explanation = json.loads(explain_result.stdout)

        self.assertEqual(0, catalog_result.returncode)
        self.assertEqual(0, explain_result.returncode)
        catalog_entry = {
            item["code"]: item for item in catalog["issueCodes"]
        }["reference.missing"]
        self.assertEqual(explanation["code"], catalog_entry["code"])
        self.assertEqual(explanation["title"], catalog_entry["title"])
        self.assertEqual(explanation["severity"], catalog_entry["severity"])
        self.assertEqual(explanation["description"], catalog_entry["description"])
        self.assertEqual(explanation["resolution"], catalog_entry["resolution"])

    def test_issue_code_catalog_rejects_workspace_path(self) -> None:
        result = verity_command("generate", "issue-code-catalog", "examples/basic")

        self.assertEqual(2, result.returncode)
        self.assertIn("does not accept workspace paths", result.stderr)

    def test_workspace_generators_require_workspace_path(self) -> None:
        result = verity_command("generate", "openapi", "--out", "build/openapi-missing.json")

        self.assertEqual(2, result.returncode)
        self.assertIn("requires a workspace path", result.stderr)

    def test_explain_security_issue_code_json_output(self) -> None:
        result = verity_command(
            "explain",
            "security.control.critical_unverified",
            "--format",
            "json",
        )

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("security.control.critical_unverified", payload["code"])
        self.assertEqual("Critical security control not verified", payload["title"])

    def test_explain_security_stale_evidence_issue_code_json_output(self) -> None:
        result = verity_command(
            "explain",
            "security.control.evidence_stale",
            "--format",
            "json",
        )

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("security.control.evidence_stale", payload["code"])
        self.assertEqual("Security verification evidence stale", payload["title"])

    def test_explain_profile_issue_code_json_output(self) -> None:
        result = verity_command("explain", "profile.required_pack", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("profile.required_pack", payload["code"])
        self.assertEqual("error", payload["severity"])

    def test_explain_accessibility_issue_code_json_output(self) -> None:
        result = verity_command(
            "explain",
            "accessibility.claim.critical_unverified",
            "--format",
            "json",
        )

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("accessibility.claim.critical_unverified", payload["code"])
        self.assertEqual("Critical accessibility claim not verified", payload["title"])

    def test_explain_compliance_issue_code_json_output(self) -> None:
        result = verity_command(
            "explain",
            "compliance.mapping.reviewed_unverified",
            "--format",
            "json",
        )

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("compliance.mapping.reviewed_unverified", payload["code"])
        self.assertEqual("Reviewed compliance mapping not verified", payload["title"])

    def test_graph_focus_json_output(self) -> None:
        result = verity_command("graph", "examples/basic", "--focus", "api.users.create", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        node_ids = {node["id"] for node in payload["nodes"]}
        self.assertIn("api.users.create", node_ids)
        self.assertIn("schema.create_user_request", node_ids)
        self.assertIn("event.user.created", node_ids)

    def test_graph_cycles_json_output(self) -> None:
        result = verity_command("graph", "tests/fixtures/broken_semantics", "--cycles", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["cycles"])

    def test_graph_includes_local_workspace_dependency_metadata(self) -> None:
        result = verity_command(
            "graph",
            "tests/fixtures/workspace_dependencies/consumer",
            "--format",
            "json",
        )

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        dependency_nodes = {
            node["id"]: node
            for node in payload["nodes"]
            if node.get("workspaceRole") == "dependency"
        }
        self.assertIn("sharedUnity::unity.package.save_system", dependency_nodes)
        self.assertEqual(
            "sharedUnity",
            dependency_nodes["sharedUnity::unity.package.save_system"]["dependencyAlias"],
        )
        self.assertEqual(
            ["unity.package.save_system"],
            payload["dependencies"][0]["exportedRecords"],
        )

    def test_validate_dependency_private_reference_json_output(self) -> None:
        result = verity_command(
            "validate",
            "tests/fixtures/workspace_dependencies/private-reference",
            "--format",
            "json",
        )

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["passed"])
        self.assertEqual(
            ["dependency.reference.not_exported"],
            [issue["code"] for issue in payload["issues"]],
        )

    def test_lint_strict_json_output(self) -> None:
        result = verity_command("lint", "examples/basic", "--strict", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])

    def test_validation_failure_exit_code(self) -> None:
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

            result = verity_command("validate", str(root), "--format", "json")

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["passed"])
        self.assertEqual(1, payload["summary"]["errors"])
        self.assertEqual("reference.missing", payload["issues"][0]["code"])
        self.assertTrue(
            payload["issues"][0]["location"].endswith("records/product.json:references[0].target")
        )
        self.assertIn("locationDetails", payload["issues"][0])
        location_details = payload["issues"][0]["locationDetails"]
        self.assertTrue(location_details["path"].endswith("records/product.json"))
        self.assertEqual("references[0].target", location_details["fieldPath"])
        self.assertEqual(["references", 0, "target"], location_details["fieldParts"])
        self.assertEqual("/references/0/target", location_details["jsonPointer"])

    def test_validation_github_annotations_preserve_json_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "annotation-validation",
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
                        "id": "product.annotation_validation",
                        "kind": "product",
                        "name": "Annotation Validation",
                        "description": "A workspace with a missing reference.",
                        "status": "ready",
                        "owner": "platform",
                        "version": "0.1.0",
                        "references": [{"type": "uses", "target": "schema.missing"}],
                    }
                ),
                encoding="utf-8",
            )

            result = verity_command(
                "validate",
                str(root),
                "--format",
                "json",
                "--github-annotations",
            )

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["passed"])
        self.assertNotIn("::error", result.stdout)
        self.assertIn("::error ", result.stderr)
        self.assertIn("title=reference.missing", result.stderr)
        self.assertIn("file=", result.stderr)
        self.assertIn("records/product.json", result.stderr)
        self.assertIn("product.annotation_validation", result.stderr)

    def test_readiness_github_annotations_preserve_json_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "annotation-readiness",
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
                        "id": "product.annotation_readiness",
                        "kind": "product",
                        "name": "Annotation Readiness",
                        "status": "ready",
                        "owner": "platform",
                        "version": "0.1.0",
                    }
                ),
                encoding="utf-8",
            )

            result = verity_command(
                "readiness",
                str(root),
                "--strict",
                "--format",
                "json",
                "--github-annotations",
            )

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["passed"])
        self.assertNotIn("::error", result.stdout)
        self.assertIn("::error ", result.stderr)
        self.assertIn("title=readiness.required", result.stderr)
        self.assertIn("description", result.stderr)

    def test_fail_on_warning_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "warning-only",
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
                        "id": "product.warning_only",
                        "kind": "product",
                        "name": "Warning Only",
                        "description": "A workspace with a warning but no validation error.",
                        "status": "ready",
                        "owner": "platform",
                        "version": "0.1.0",
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "schema.json").write_text(
                json.dumps(
                    {
                        "id": "schema.unused",
                        "kind": "schema.object",
                        "name": "Unused Schema",
                        "description": "Unused by design.",
                        "status": "ready",
                        "owner": "platform",
                        "jsonSchema": {"type": "object", "properties": {}},
                    }
                ),
                encoding="utf-8",
            )

            default_result = verity_command("validate", str(root), "--format", "json")
            fail_on_warning_result = verity_command(
                "validate", str(root), "--format", "json", "--fail-on", "warning"
            )

        self.assertEqual(0, default_result.returncode)
        self.assertEqual(1, fail_on_warning_result.returncode)

    def test_usage_error_exit_code(self) -> None:
        result = verity_command("unknown-command")

        self.assertEqual(2, result.returncode)
        self.assertIn("invalid choice", result.stderr)

    def test_future_workspace_version_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "future",
                        "specVersion": "v99.0.0",
                        "packs": ["verity.core"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "product.json").write_text(
                json.dumps(
                    {
                        "id": "product.future",
                        "kind": "product",
                        "name": "Future Product",
                        "status": "ready",
                        "owner": "platform",
                        "version": "1.0.0",
                    }
                ),
                encoding="utf-8",
            )

            result = verity_command("validate", str(root), "--format", "json")

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(any(issue["code"] == "workspace.version.future" for issue in payload["issues"]))

    def test_v0_2_workspace_requires_explicit_pack_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "missing-pack-paths",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "product.json").write_text(
                json.dumps(
                    {
                        "id": "product.missing_pack_paths",
                        "kind": "product",
                        "name": "Missing Pack Paths",
                        "status": "ready",
                        "owner": "platform",
                        "version": "1.0.0",
                    }
                ),
                encoding="utf-8",
            )

            result = verity_command("validate", str(root), "--format", "json")

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(any(issue["code"] == "workspace.packPaths.missing" for issue in payload["issues"]))

    def test_migrate_list_json_output(self) -> None:
        result = verity_command("migrate", "--list", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("verityspec_migration_capabilities", payload["type"])
        self.assertEqual("v0.2.0", payload["currentVersion"])
        self.assertIn("v0.1.0", {version["id"] for version in payload["supportedVersions"]})
        self.assertIn("v0.2.0", {version["id"] for version in payload["supportedVersions"]})
        self.assertEqual(
            ["legacy-to-v0.1.0", "v0.1.0-to-v0.2.0"],
            [step["id"] for step in payload["steps"]],
        )
        steps_by_id = {step["id"]: step for step in payload["steps"]}
        self.assertIn(
            "Renames legacy workspace version fields to specVersion.",
            steps_by_id["legacy-to-v0.1.0"]["impacts"]["workspaceFormat"],
        )
        self.assertIn(
            "Renames known legacy record type fields to kind.",
            steps_by_id["legacy-to-v0.1.0"]["impacts"]["records"],
        )
        self.assertIn(
            "Makes local external pack paths explicit with packPaths.",
            steps_by_id["v0.1.0-to-v0.2.0"]["impacts"]["packs"],
        )
        self.assertIn(
            "External pack-provided generator availability becomes tied to explicit packPaths.",
            steps_by_id["v0.1.0-to-v0.2.0"]["impacts"]["generators"],
        )

    def test_migrate_list_text_output_includes_impacts(self) -> None:
        result = verity_command("migrate", "--list")

        self.assertEqual(0, result.returncode)
        self.assertIn("Migration steps:", result.stdout)
        self.assertIn("Impacts:", result.stdout)
        self.assertIn("Workspace format:", result.stdout)
        self.assertIn("Generators:", result.stdout)

    def test_migrate_dry_run_edge_fixtures_report_without_writing(self) -> None:
        cases = [
            {
                "fixture": "legacy_workspace",
                "target": "v0.1.0",
                "path": ["legacy-to-v0.1.0"],
                "impacts": {
                    "workspaceFormat": "Renames legacy workspace version fields to specVersion.",
                    "records": "Renames known legacy record type fields to kind.",
                    "packs": "Adds the default built-in pack set when packs are missing.",
                    "generators": "Generator availability may change when default built-in packs are added.",
                },
                "changes": [
                    ("verityspec.json", "rename", "version -> specVersion", "0.1.0", "v0.1.0"),
                    ("verityspec.json", "remove", "version", "0.1.0", None),
                    ("verityspec.json", "set", "packs", None, DEFAULT_BUILTIN_PACKS),
                    ("records/product.json", "rename", "type -> kind", "product", "product"),
                    ("records/product.json", "remove", "type", "product", None),
                    (
                        "records/product.json",
                        "rename",
                        "displayName -> name",
                        "Legacy Product",
                        "Legacy Product",
                    ),
                    ("records/product.json", "remove", "displayName", "Legacy Product", None),
                    ("records/product.json", "normalize", "status", "approved", "ready"),
                    ("records/product.json", "set", "owner", None, "unknown"),
                    ("records/product.json", "set", "version", None, "0.1.0"),
                ],
            },
            {
                "fixture": "v0_1_0_workspace",
                "target": "v0.2.0",
                "path": ["v0.1.0-to-v0.2.0"],
                "impacts": {
                    "workspaceFormat": "Upgrades specVersion to v0.2.0.",
                    "packs": "Makes local external pack paths explicit with packPaths.",
                    "generators": "External pack-provided generator availability becomes tied to explicit packPaths.",
                },
                "changes": [
                    ("verityspec.json", "upgrade", "specVersion", "v0.1.0", "v0.2.0"),
                    ("verityspec.json", "set", "packPaths", None, []),
                ],
            },
            {
                "fixture": "legacy_workspace",
                "target": "v0.2.0",
                "path": ["legacy-to-v0.1.0", "v0.1.0-to-v0.2.0"],
                "impacts": {
                    "workspaceFormat": "Adds explicit packPaths when absent or repairs invalid packPaths values.",
                    "records": "Renames displayName to name.",
                    "packs": "Makes local external pack paths explicit with packPaths.",
                    "generators": "External pack-provided generator availability becomes tied to explicit packPaths.",
                },
                "changes": [
                    ("verityspec.json", "rename", "version -> specVersion", "0.1.0", "v0.1.0"),
                    ("verityspec.json", "remove", "version", "0.1.0", None),
                    ("verityspec.json", "set", "packs", None, DEFAULT_BUILTIN_PACKS),
                    ("verityspec.json", "upgrade", "specVersion", "v0.1.0", "v0.2.0"),
                    ("verityspec.json", "set", "packPaths", None, []),
                ],
            },
        ]
        for case in cases:
            with self.subTest(fixture=case["fixture"], target=case["target"]):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp) / str(case["fixture"])
                    shutil.copytree(MIGRATION_FIXTURES / str(case["fixture"]), root)
                    resolved_root = root.resolve()
                    before = snapshot_files(root)

                    result = verity_command(
                        "migrate",
                        str(root),
                        "--to",
                        str(case["target"]),
                        "--dry-run",
                        "--format",
                        "json",
                    )
                    report = json.loads(result.stdout)
                    after = snapshot_files(root)

                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(before, after)
                self.assertTrue(report["changed"])
                self.assertEqual(case["target"], report["targetVersion"])
                self.assertEqual(case["path"], [step["id"] for step in report["migrationPath"]])
                self.assertEqual(
                    {"workspaceFormat", "records", "packs", "generators"},
                    set(report["impactSummary"]),
                )
                for category, impact in case["impacts"].items():
                    self.assertIn(impact, report["impactSummary"][category])
                self.assertEqual([], report["filesWritten"])
                self.assertEqual(str(resolved_root), report["source"])

                normalized_changes = {
                    (
                        str(Path(change["path"]).relative_to(resolved_root)),
                        change["action"],
                        change["field"],
                        canonical_json(change["before"]),
                        canonical_json(change["after"]),
                    )
                    for change in report["changes"]
                }
                expected_changes = {
                    (path, action, field, canonical_json(before), canonical_json(after))
                    for path, action, field, before, after in case["changes"]
                }
                self.assertEqual(set(), expected_changes - normalized_changes)

    def test_migrate_rewrites_legacy_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            config_path = root / "verityspec.json"
            record_path = root / "records" / "product.json"
            config_path.write_text(
                json.dumps({"workspace": "legacy", "version": "0.1.0", "records": ["records/*.json"]}),
                encoding="utf-8",
            )
            record_path.write_text(
                json.dumps(
                    {
                        "id": "product.legacy",
                        "type": "product",
                        "displayName": "Legacy Product",
                        "status": "approved",
                    }
                ),
                encoding="utf-8",
            )

            result = verity_command("migrate", str(root), "--format", "json")
            report = json.loads(result.stdout)
            config = json.loads(config_path.read_text(encoding="utf-8"))
            record = json.loads(record_path.read_text(encoding="utf-8"))
            validation = verity_command("validate", str(root), "--format", "json")

        self.assertEqual(0, result.returncode)
        self.assertEqual(0, validation.returncode)
        self.assertGreater(report["changeCount"], 0)
        self.assertEqual("v0.2.0", config["specVersion"])
        self.assertEqual([], config["packPaths"])
        self.assertNotIn("version", config)
        self.assertIn("verity.core", config["packs"])
        self.assertEqual("product", record["kind"])
        self.assertEqual("Legacy Product", record["name"])
        self.assertEqual("ready", record["status"])
        self.assertEqual("unknown", record["owner"])
        self.assertEqual("0.1.0", record["version"])
        self.assertNotIn("type", record)
        self.assertNotIn("displayName", record)

    def test_migrate_can_target_v0_1_0_explicitly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            config_path = root / "verityspec.json"
            config_path.write_text(
                json.dumps({"workspace": "legacy", "version": "0.1.0", "records": ["records/*.json"]}),
                encoding="utf-8",
            )
            (root / "records" / "product.json").write_text(
                json.dumps(
                    {
                        "id": "product.legacy",
                        "type": "product",
                        "displayName": "Legacy Product",
                        "status": "approved",
                    }
                ),
                encoding="utf-8",
            )

            result = verity_command("migrate", str(root), "--to", "v0.1.0", "--format", "json")
            report = json.loads(result.stdout)
            config = json.loads(config_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertEqual("v0.1.0", config["specVersion"])
        self.assertNotIn("packPaths", config)
        self.assertEqual(["legacy-to-v0.1.0"], [step["id"] for step in report["migrationPath"]])

    def test_migrate_repairs_v0_2_0_pack_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            config_path = root / "verityspec.json"
            config_path.write_text(
                json.dumps(
                    {
                        "workspace": "current",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "product.json").write_text(
                json.dumps(
                    {
                        "id": "product.current",
                        "kind": "product",
                        "name": "Current Product",
                        "status": "ready",
                        "owner": "platform",
                        "version": "1.0.0",
                    }
                ),
                encoding="utf-8",
            )

            result = verity_command("migrate", str(root), "--format", "json")
            report = json.loads(result.stdout)
            config = json.loads(config_path.read_text(encoding="utf-8"))
            validation = verity_command("validate", str(root), "--format", "json")

        self.assertEqual(0, result.returncode)
        self.assertEqual(0, validation.returncode)
        self.assertEqual([], config["packPaths"])
        self.assertEqual([], report["migrationPath"])
        self.assertTrue(report["changed"])
        self.assertIn(
            "Workspace manifest fields are rewritten or repaired.",
            report["impactSummary"]["workspaceFormat"],
        )
        self.assertIn(
            "Resolved pack configuration is rewritten or repaired.",
            report["impactSummary"]["packs"],
        )
        self.assertIn(
            "Generator availability may change when resolved packs or pack paths change.",
            report["impactSummary"]["generators"],
        )

    def test_init_templates_create_executable_workspaces(self) -> None:
        expected_packs = {
            "basic": ["verity.core", "verity.pack.api", "verity.pack.cli", "verity.pack.events"],
            "api": ["verity.core", "verity.pack.api"],
            "cli": ["verity.core", "verity.pack.cli"],
            "events": ["verity.core", "verity.pack.events"],
            "security": ["verity.core", "verity.pack.api", "verity.pack.security"],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for template, packs in expected_packs.items():
                with self.subTest(template=template):
                    workspace_path = root / template
                    init_result = verity_command(
                        "init",
                        str(workspace_path),
                        "--template",
                        template,
                        "--name",
                        f"starter_{template}",
                        "--owner",
                        "platform",
                    )
                    config = json.loads((workspace_path / "verityspec.json").read_text(encoding="utf-8"))
                    validate_result = verity_command("validate", str(workspace_path), "--format", "json")
                    lint_result = verity_command("lint", str(workspace_path), "--strict", "--format", "json")
                    readiness_result = verity_command(
                        "readiness",
                        str(workspace_path),
                        "--strict",
                        "--format",
                        "json",
                    )

                    self.assertEqual(0, init_result.returncode)
                    self.assertEqual(packs, config["packs"])
                    self.assertEqual([], config["packPaths"])
                    self.assertEqual(0, validate_result.returncode)
                    self.assertEqual(0, lint_result.returncode)
                    self.assertEqual(0, readiness_result.returncode)
                    self.assertTrue(json.loads(validate_result.stdout)["passed"])
                    self.assertTrue(json.loads(lint_result.stdout)["passed"])
                    self.assertTrue(json.loads(readiness_result.stdout)["passed"])

    def test_init_refuses_existing_json_records_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace_path = Path(tmp) / "existing"
            records_path = workspace_path / "records"
            records_path.mkdir(parents=True)
            (records_path / "existing.json").write_text("{}", encoding="utf-8")

            result = verity_command("init", str(workspace_path), "--template", "api")

        self.assertEqual(2, result.returncode)
        self.assertIn("Record directory already contains JSON records", result.stderr)

    def test_pack_list_json_output(self) -> None:
        result = verity_command("pack", "list", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        pack_ids = {pack["id"] for pack in payload["packs"]}
        self.assertIn("verity.core", pack_ids)
        self.assertIn("verity.pack.api", pack_ids)
        self.assertIn("verity.pack.accessibility", pack_ids)
        self.assertIn("verity.pack.compliance", pack_ids)
        self.assertIn("verity.pack.content", pack_ids)
        self.assertIn("verity.pack.economy", pack_ids)
        self.assertIn("verity.pack.evidence", pack_ids)
        self.assertIn("verity.pack.game-assets", pack_ids)
        self.assertIn("verity.pack.game-core", pack_ids)
        self.assertIn("verity.pack.gameplay", pack_ids)
        self.assertIn("verity.pack.godot", pack_ids)
        self.assertIn("verity.pack.liveops", pack_ids)
        self.assertIn("verity.pack.mobile", pack_ids)
        self.assertIn("verity.pack.observability", pack_ids)
        self.assertIn("verity.pack.product-delivery", pack_ids)
        self.assertIn("verity.pack.progression", pack_ids)
        self.assertIn("verity.pack.security", pack_ids)
        self.assertIn("verity.pack.unity", pack_ids)
        self.assertIn("verity.pack.unreal", pack_ids)
        api_pack = next(pack for pack in payload["packs"] if pack["id"] == "verity.pack.api")
        self.assertEqual(["openapi"], api_pack["generators"])
        self.assertEqual(
            {
                "id": "openapi",
                "name": "OpenAPI",
                "description": "Emit an OpenAPI document from API endpoint and schema records.",
                "artifactType": "api-description",
                "outputFormats": ["json"],
                "recordKinds": ["api.endpoint"],
            },
            api_pack["generatorMetadata"][0],
        )

    def test_pack_validate_json_output(self) -> None:
        result = verity_command("pack", "validate", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual("pack.validate", payload["command"])

    def test_pack_validate_unknown_pack_fails(self) -> None:
        result = verity_command("pack", "validate", "verity.pack.missing", "--format", "json")

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["passed"])
        self.assertEqual("pack.unknown", payload["issues"][0]["code"])

    def test_pack_doctor_json_output(self) -> None:
        result = verity_command("pack", "doctor", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual("pack.doctor", payload["command"])
        self.assertEqual("verityspec.packs", payload["entryPointGroup"])
        self.assertGreater(payload["summary"]["builtInPackCount"], 0)
        self.assertEqual([], payload["issues"])

    def test_pack_doctor_text_output(self) -> None:
        result = verity_command("pack", "doctor")

        self.assertEqual(0, result.returncode)
        self.assertIn("Pack diagnostics passed.", result.stdout)
        self.assertIn("Entry point group: verityspec.packs", result.stdout)

    def test_pack_doctor_reports_external_builtin_collision_without_internal_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack_path = Path(tmp) / "core-collision"
            shutil.copytree(ROOT / CUSTOM_PACK, pack_path)
            manifest_path = pack_path / "pack.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["id"] = "verity.core"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            result = verity_command(
                "pack",
                "doctor",
                "--path",
                str(pack_path),
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode)
        self.assertEqual("", result.stderr)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["passed"])
        self.assertEqual("pack.external.builtin_collision", payload["issues"][0]["code"])

    def test_pack_compare_official_extension_mirror_json_output(self) -> None:
        result = verity_command(
            "pack",
            "compare",
            "verity.pack.unity",
            "--mirror",
            UNITY_EXTENSION_MIRROR,
            "--format",
            "json",
        )

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual("pack.compare", payload["command"])
        self.assertEqual("verity.pack.unity", payload["packId"])
        self.assertEqual("built-in", payload["source"]["source"])
        self.assertEqual("mirror", payload["mirror"]["source"])
        self.assertEqual([], payload["differences"])
        self.assertGreater(payload["summary"]["schemas"], 0)
        self.assertGreater(payload["summary"]["readinessGates"], 0)
        self.assertGreater(payload["summary"]["referenceRules"], 0)
        self.assertGreater(payload["summary"]["generators"], 0)

    def test_pack_compare_reports_mirror_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mirror_path = Path(tmp) / "unity-mirror"
            shutil.copytree(ROOT / UNITY_EXTENSION_MIRROR, mirror_path)
            manifest_path = mirror_path / "pack.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["generators"] = []
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            result = verity_command(
                "pack",
                "compare",
                "verity.pack.unity",
                "--mirror",
                str(mirror_path),
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["passed"])
        self.assertEqual("pack.mirror.surface_mismatch", payload["issues"][0]["code"])
        self.assertTrue(
            any(difference["surface"] == "generatorMetadata" for difference in payload["differences"])
        )

    def test_pack_compare_reports_invalid_mirror_path(self) -> None:
        result = verity_command(
            "pack",
            "compare",
            "verity.pack.unity",
            "--mirror",
            "tests/fixtures/official_extension_mirrors/missing-pack",
            "--format",
            "json",
        )

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["passed"])
        self.assertEqual("pack.mirror.invalid", payload["issues"][0]["code"])

    def test_pack_compare_reports_mirror_id_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mirror_path = Path(tmp) / "unity-mirror"
            shutil.copytree(ROOT / UNITY_EXTENSION_MIRROR, mirror_path)
            manifest_path = mirror_path / "pack.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["id"] = "verity.pack.unity-renamed"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            result = verity_command(
                "pack",
                "compare",
                "verity.pack.unity",
                "--mirror",
                str(mirror_path),
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["passed"])
        self.assertEqual("pack.mirror.id_mismatch", payload["issues"][0]["code"])

    def test_pack_compare_text_output(self) -> None:
        result = verity_command(
            "pack",
            "compare",
            "verity.pack.unity",
            "--mirror",
            UNITY_EXTENSION_MIRROR,
        )

        self.assertEqual(0, result.returncode)
        self.assertIn("Pack mirror comparison passed.", result.stdout)
        self.assertIn("Pack: verity.pack.unity", result.stdout)

    def test_pack_init_creates_valid_external_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack_path = Path(tmp) / "features"
            init_result = verity_command(
                "pack",
                "init",
                "verity.pack.features",
                "--out",
                str(pack_path),
                "--kind",
                "feature.flag",
                "--name",
                "Feature Pack",
            )
            manifest = json.loads((pack_path / "pack.json").read_text(encoding="utf-8"))
            schema = json.loads((pack_path / "schemas" / "feature-flag.schema.json").read_text(encoding="utf-8"))
            validate_result = verity_command(
                "pack",
                "validate",
                "verity.pack.features",
                "--path",
                str(pack_path),
                "--format",
                "json",
            )
            list_result = verity_command("pack", "list", "--path", str(pack_path), "--format", "json")

        self.assertEqual(0, init_result.returncode)
        self.assertEqual("verity.pack.features", manifest["id"])
        self.assertEqual("feature.flag", manifest["schemas"][0]["kind"])
        self.assertEqual("schemas/feature-flag.schema.json", manifest["schemas"][0]["path"])
        self.assertEqual(
            [
                {
                    "sourceKind": "product",
                    "relationship": "uses",
                    "targetKind": "feature.flag",
                }
            ],
            manifest["referenceRules"],
        )
        self.assertEqual("schema-bundle", manifest["generators"][0]["id"])
        self.assertEqual("schema-bundle", manifest["generators"][0]["artifactType"])
        self.assertEqual(["feature.flag"], manifest["generators"][0]["recordKinds"])
        self.assertEqual("feature.flag", schema["properties"]["kind"]["const"])
        self.assertEqual(0, validate_result.returncode)
        self.assertTrue(json.loads(validate_result.stdout)["passed"])
        pack_ids = {pack["id"] for pack in json.loads(list_result.stdout)["packs"]}
        self.assertIn("verity.pack.features", pack_ids)

    def test_pack_init_scaffold_supports_sample_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack_path = root / "packs" / "features"
            workspace_path = root / "workspace"
            records_path = workspace_path / "records"
            records_path.mkdir(parents=True)
            bundle_path = root / "schema-bundle.json"

            init_result = verity_command(
                "pack",
                "init",
                "verity.pack.features",
                "--out",
                str(pack_path),
                "--kind",
                "feature.flag",
                "--name",
                "Feature Pack",
            )
            (workspace_path / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "pack.scaffold.sample",
                        "specVersion": "v0.2.0",
                        "packs": ["verity.core", "verity.pack.features"],
                        "packPaths": ["../packs/features"],
                        "records": ["records/*.json"],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (records_path / "product.json").write_text(
                json.dumps(
                    {
                        "id": "product.flags",
                        "kind": "product",
                        "name": "Feature Flag Product",
                        "description": "A product fixture using a generated external pack.",
                        "status": "ready",
                        "owner": "platform",
                        "version": "0.1.0",
                        "references": [{"type": "uses", "target": "feature.checkout"}],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (records_path / "feature.checkout.json").write_text(
                json.dumps(
                    {
                        "id": "feature.checkout",
                        "kind": "feature.flag",
                        "name": "Checkout Feature",
                        "description": "Controls access to the checkout flow.",
                        "status": "ready",
                        "owner": "growth",
                        "references": [],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            pack_validate_result = verity_command(
                "pack",
                "validate",
                "verity.pack.features",
                "--path",
                str(pack_path),
                "--format",
                "json",
            )
            validate_result = verity_command("validate", str(workspace_path), "--format", "json")
            lint_result = verity_command("lint", str(workspace_path), "--strict", "--format", "json")
            readiness_result = verity_command(
                "readiness",
                str(workspace_path),
                "--strict",
                "--format",
                "json",
            )
            generate_result = verity_command(
                "generate",
                "schema-bundle",
                str(workspace_path),
                "--out",
                str(bundle_path),
            )
            bundle = json.loads(bundle_path.read_text(encoding="utf-8"))

        self.assertEqual(0, init_result.returncode)
        self.assertEqual(0, pack_validate_result.returncode)
        self.assertEqual(0, validate_result.returncode)
        self.assertEqual(0, lint_result.returncode)
        self.assertEqual(0, readiness_result.returncode)
        self.assertEqual(0, generate_result.returncode)
        self.assertTrue(json.loads(pack_validate_result.stdout)["passed"])
        self.assertTrue(json.loads(validate_result.stdout)["passed"])
        self.assertTrue(json.loads(lint_result.stdout)["passed"])
        self.assertTrue(json.loads(readiness_result.stdout)["passed"])
        self.assertIn("feature.flag", bundle["schemas"])

    def test_pack_validate_unknown_generator_metadata_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack_path = Path(tmp) / "features"
            shutil.copytree(ROOT / CUSTOM_PACK, pack_path)
            manifest_path = pack_path / "pack.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["generators"] = [
                {
                    "id": "unknown-report",
                    "name": "Unknown Report",
                    "description": "A deliberately unsupported generator fixture.",
                    "artifactType": "report",
                    "outputFormats": ["json"],
                    "recordKinds": ["feature.flag"],
                }
            ]
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            result = verity_command(
                "pack",
                "validate",
                "verity.pack.features",
                "--path",
                str(pack_path),
                "--format",
                "json",
            )

        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["passed"])
        self.assertTrue(any(issue["code"] == "pack.generator.unknown" for issue in payload["issues"]))

    def test_external_pack_workspace_from_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle_path = Path(tmp) / "schema-bundle.json"
            validate_result = verity_command("validate", CUSTOM_PACK_WORKSPACE, "--format", "json")
            lint_result = verity_command("lint", CUSTOM_PACK_WORKSPACE, "--strict", "--format", "json")
            readiness_result = verity_command("readiness", CUSTOM_PACK_WORKSPACE, "--strict", "--format", "json")
            generate_result = verity_command(
                "generate",
                "schema-bundle",
                CUSTOM_PACK_WORKSPACE,
                "--out",
                str(bundle_path),
            )
            bundle = json.loads(bundle_path.read_text(encoding="utf-8"))

        self.assertEqual(0, validate_result.returncode)
        self.assertEqual(0, lint_result.returncode)
        self.assertEqual(0, readiness_result.returncode)
        self.assertEqual(0, generate_result.returncode)
        self.assertIn("feature.flag", bundle["schemas"])

    def test_external_pack_cli_path_for_workspace_and_pack_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "records").mkdir()
            (root / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "external.cli.path",
                        "specVersion": "v0.1.0",
                        "packs": ["verity.core", "verity.pack.features"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "product.json").write_text(
                json.dumps(
                    {
                        "id": "product.flags",
                        "kind": "product",
                        "name": "Feature Flag Product",
                        "description": "A product fixture that loads an external pack.",
                        "status": "ready",
                        "owner": "platform",
                        "version": "0.1.0",
                        "references": [{"type": "configures", "target": "feature.checkout"}],
                    }
                ),
                encoding="utf-8",
            )
            (root / "records" / "feature.checkout.json").write_text(
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
                ),
                encoding="utf-8",
            )

            validate_result = verity_command(
                "validate",
                str(root),
                "--pack-path",
                CUSTOM_PACK,
                "--format",
                "json",
            )
            pack_list_result = verity_command("pack", "list", "--path", CUSTOM_PACK, "--format", "json")
            pack_validate_result = verity_command(
                "pack",
                "validate",
                "verity.pack.features",
                "--path",
                CUSTOM_PACK,
                "--format",
                "json",
            )
            pack_index_path = root / "pack-capability-index.json"
            pack_index_result = verity_command(
                "generate",
                "pack-capability-index",
                str(root),
                "--pack-path",
                CUSTOM_PACK,
                "--out",
                str(pack_index_path),
            )
            pack_index_payload = json.loads(pack_index_path.read_text(encoding="utf-8"))

        self.assertEqual(0, validate_result.returncode)
        self.assertEqual(0, pack_list_result.returncode)
        self.assertEqual(0, pack_validate_result.returncode)
        self.assertEqual(0, pack_index_result.returncode)
        pack_payload = json.loads(pack_list_result.stdout)
        pack_ids = {pack["id"] for pack in pack_payload["packs"]}
        self.assertIn("verity.pack.features", pack_ids)
        custom_pack = next(pack for pack in pack_payload["packs"] if pack["id"] == "verity.pack.features")
        self.assertEqual(["schema-bundle"], custom_pack["generators"])
        self.assertEqual([{"id": "schema-bundle"}], custom_pack["generatorMetadata"])
        self.assertEqual("pack_capability_index", pack_index_payload["type"])
        self.assertEqual(1, pack_index_payload["summary"]["externalPackCount"])
        self.assertIn("feature.flag", pack_index_payload["summary"]["recordKinds"])

    def test_validation_report_generator_writes_report_for_broken_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "validation-report.json"
            result = verity_command(
                "generate",
                "validation-report",
                "tests/fixtures/broken_semantics",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(1, result.returncode)
        self.assertFalse(payload["passed"])
        self.assertGreater(payload["summary"]["errors"], 0)
        self.assertTrue(any(issue["code"] == "reference.disallowed" for issue in payload["issues"]))
        disallowed = next(issue for issue in payload["issues"] if issue["code"] == "reference.disallowed")
        self.assertIn("locationDetails", disallowed)
        self.assertTrue(disallowed["locationDetails"]["path"].endswith("records/product.json"))
        self.assertEqual("references[0].target", disallowed["locationDetails"]["fieldPath"])
        self.assertEqual(["references", 0, "target"], disallowed["locationDetails"]["fieldParts"])
        self.assertEqual("/references/0/target", disallowed["locationDetails"]["jsonPointer"])

    def test_security_report_generator_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "security-report.json"
            result = verity_command(
                "generate",
                "security-report",
                "examples/security",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertEqual("security_report", payload["type"])
        self.assertEqual(1, payload["controlCount"])
        self.assertEqual({"verified": 1}, payload["summary"]["byCoverage"])
        self.assertEqual(
            {
                "criticalUnverified": [],
                "staleEvidence": [],
                "missingVerificationDates": [],
            },
            payload["summary"]["releaseGaps"],
        )
        self.assertEqual("security.control.account_access", payload["controls"][0]["id"])

    def test_security_report_generator_writes_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "security-report.md"
            result = verity_command(
                "generate",
                "security-report",
                "examples/security",
                "--format",
                "markdown",
                "--out",
                str(out_path),
            )

            text = out_path.read_text(encoding="utf-8")

        self.assertEqual(0, result.returncode)
        self.assertIn("Generated security-report", result.stdout)
        self.assertTrue(text.startswith("# VeritySpec Security Report\n"))
        self.assertIn("## Summary", text)
        self.assertIn("| Security controls | 1 |", text)
        self.assertIn("## Release Gaps", text)
        self.assertIn("| Stale evidence | 0 | none |", text)
        self.assertIn("## Security Controls", text)
        self.assertIn("does not make legal, compliance", text)

    def test_generate_report_accepts_explicit_generated_at(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "security-report.json"
            result = verity_command(
                "generate",
                "security-report",
                "examples/security",
                "--generated-at",
                FIXED_GENERATED_AT,
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertEqual(FIXED_GENERATED_AT, payload["generatedAt"])

    def test_generate_report_rejects_invalid_generated_at(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "security-report.json"
            result = verity_command(
                "generate",
                "security-report",
                "examples/security",
                "--generated-at",
                "not-a-datetime",
                "--out",
                str(out_path),
            )

        self.assertEqual(2, result.returncode)
        self.assertIn("--generated-at must be an ISO 8601 datetime.", result.stderr)
        self.assertFalse(out_path.exists())

    def test_security_report_generator_matches_golden_file(self) -> None:
        expected = json.loads(SECURITY_REPORT_GOLDEN.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "security-report.json"
            result = verity_command(
                "generate",
                "security-report",
                "examples/security",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        datetime.fromisoformat(payload["generatedAt"])
        self.assertEqual(str(ROOT / "examples" / "security"), payload["workspacePath"])
        self.assertIsInstance(payload["verityVersion"], str)
        self.assertEqual(expected, normalize_security_report_for_golden(payload))

    def test_observability_report_generator_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "observability-report.json"
            result = verity_command(
                "generate",
                "observability-report",
                "examples/observability",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertEqual("observability_report", payload["type"])
        self.assertEqual(4, payload["signalCount"])
        self.assertEqual(1, payload["summary"]["telemetry"])
        self.assertEqual(1, payload["summary"]["metrics"])
        self.assertEqual(1, payload["summary"]["dashboards"])
        self.assertEqual(1, payload["summary"]["alerts"])
        self.assertEqual({"checkout-platform": 4}, payload["summary"]["byOwner"])
        self.assertEqual({"critical": 1}, payload["summary"]["alertsBySeverity"])
        self.assertEqual(
            {
                "telemetryWithoutMetrics": [],
                "metricsWithoutTelemetry": [],
                "dashboardsWithoutAlerts": [],
                "alertsWithoutRunbooks": [],
                "missingOwners": [],
            },
            payload["summary"]["releaseGaps"],
        )
        self.assertEqual("observability.metric.checkout_success_rate", payload["metrics"][0]["id"])

    def test_observability_report_generator_matches_golden_file(self) -> None:
        expected = json.loads((OBSERVABILITY_GOLDEN / "observability_report.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "observability-report.json"
            result = verity_command(
                "generate",
                "observability-report",
                "examples/observability",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        datetime.fromisoformat(payload["generatedAt"])
        self.assertEqual(str(ROOT / "examples" / "observability"), payload["workspacePath"])
        self.assertIsInstance(payload["verityVersion"], str)
        self.assertEqual(expected, normalize_observability_report_for_golden(payload))

    def test_observability_schema_bundle_generator_matches_golden_file(self) -> None:
        expected = json.loads((OBSERVABILITY_GOLDEN / "schema_bundle.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "observability-schema-bundle.json"
            result = verity_command(
                "generate",
                "schema-bundle",
                "examples/observability",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertEqual(expected, payload)

    def test_accessibility_report_generator_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "accessibility-report.json"
            result = verity_command(
                "generate",
                "accessibility-report",
                "examples/accessibility",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertEqual("accessibility_report", payload["type"])
        self.assertEqual(1, payload["claimCount"])
        self.assertEqual({"checkout-platform": 1}, payload["summary"]["byOwner"])
        self.assertEqual({"wcag-2.2": 1}, payload["summary"]["byStandard"])
        self.assertEqual({"a": 1}, payload["summary"]["byLevel"])
        self.assertEqual({"high": 1}, payload["summary"]["byImpact"])
        self.assertEqual({"verified": 1}, payload["summary"]["byCoverage"])
        self.assertEqual(
            {
                "criticalUnverified": [],
                "claimsWithoutTargets": [],
                "missingOwners": [],
                "missingVerificationDates": [],
            },
            payload["summary"]["releaseGaps"],
        )
        self.assertEqual("accessibility.claim.checkout_keyboard", payload["claims"][0]["id"])

    def test_accessibility_report_generator_matches_golden_file(self) -> None:
        expected = json.loads(ACCESSIBILITY_REPORT_GOLDEN.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "accessibility-report.json"
            result = verity_command(
                "generate",
                "accessibility-report",
                "examples/accessibility",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        datetime.fromisoformat(payload["generatedAt"])
        self.assertEqual(str(ROOT / "examples" / "accessibility"), payload["workspacePath"])
        self.assertIsInstance(payload["verityVersion"], str)
        self.assertEqual(expected, normalize_accessibility_report_for_golden(payload))

    def test_compliance_matrix_generator_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "compliance-matrix.json"
            result = verity_command(
                "generate",
                "compliance-matrix",
                "examples/compliance",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertEqual("compliance_matrix", payload["type"])
        self.assertEqual(1, payload["mappingCount"])
        self.assertEqual({"internal-access-review": 1}, payload["summary"]["byFramework"])
        self.assertEqual(
            {
                "mappingsWithoutTargets": [],
                "mappingsWithoutEvidence": [],
                "reviewedUnverified": [],
                "missingOwners": [],
                "targetsWithoutOwners": [],
            },
            payload["summary"]["releaseGaps"],
        )
        self.assertEqual("compliance.mapping.checkout_access_review", payload["matrix"][0]["id"])

    def test_compliance_matrix_generator_matches_golden_file(self) -> None:
        expected = json.loads(COMPLIANCE_MATRIX_GOLDEN.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "compliance-matrix.json"
            result = verity_command(
                "generate",
                "compliance-matrix",
                "examples/compliance",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        datetime.fromisoformat(payload["generatedAt"])
        self.assertEqual(str(ROOT / "examples" / "compliance"), payload["workspacePath"])
        self.assertIsInstance(payload["verityVersion"], str)
        self.assertEqual(expected, normalize_compliance_matrix_for_golden(payload))

    def test_deployment_report_generator_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "deployment-report.json"
            result = verity_command(
                "generate",
                "deployment-report",
                "examples/deployment",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertEqual("deployment_report", payload["type"])
        self.assertEqual(1, payload["targetCount"])
        self.assertEqual(1, payload["runtimeCount"])
        self.assertEqual({"production": 1}, payload["summary"]["byEnvironment"])
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
            payload["summary"]["releaseGaps"],
        )
        self.assertEqual("deployment.target.checkout_production", payload["targets"][0]["id"])
        self.assertEqual(
            [
                "evidence.ci-run.checkout_release",
                "evidence.qa.checkout_release",
                "evidence.artifact.checkout_release_manifest",
            ],
            [item["id"] for item in payload["targets"][0]["releaseEvidence"]],
        )

    def test_deployment_report_generator_writes_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "deployment-report.md"
            result = verity_command(
                "generate",
                "deployment-report",
                "examples/deployment",
                "--format",
                "markdown",
                "--out",
                str(out_path),
            )

            text = out_path.read_text(encoding="utf-8")

        self.assertEqual(0, result.returncode)
        self.assertIn("Generated deployment-report", result.stdout)
        self.assertTrue(text.startswith("# VeritySpec Deployment Report\n"))
        self.assertIn("## Summary", text)
        self.assertIn("| Deployment targets | 1 |", text)
        self.assertIn("## Release Gaps", text)
        self.assertIn("| Production without release evidence | 0 | none |", text)
        self.assertIn("## Deployment Targets", text)
        self.assertIn("evidence.ci-run.checkout_release", text)
        self.assertIn("does not make legal, commercial", text)

    def test_deployment_report_generator_matches_golden_file(self) -> None:
        expected = json.loads(DEPLOYMENT_GOLDEN.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "deployment-report.json"
            result = verity_command(
                "generate",
                "deployment-report",
                "examples/deployment",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        datetime.fromisoformat(payload["generatedAt"])
        self.assertEqual(str(ROOT / "examples" / "deployment"), payload["workspacePath"])
        self.assertIsInstance(payload["verityVersion"], str)
        self.assertEqual(expected, normalize_deployment_report_for_golden(payload))

    def test_evidence_report_generator_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "evidence-report.json"
            result = verity_command(
                "generate",
                "evidence-report",
                "examples/evidence",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertEqual("evidence_report", payload["type"])
        self.assertEqual(10, payload["evidenceCount"])
        self.assertEqual(1, payload["summary"]["byKind"]["evidence.ci-run"])
        self.assertEqual({"ready": 10}, payload["summary"]["byStatus"])
        self.assertEqual(
            {
                "missingSubjects": [],
                "missingArtifacts": [],
                "failingEvidence": [],
                "inconclusiveEvidence": [],
            },
            payload["summary"]["releaseGaps"],
        )
        self.assertEqual("evidence.artifact.release_manifest", payload["evidence"][0]["id"])

    def test_evidence_report_generator_matches_golden_file(self) -> None:
        expected = json.loads(EVIDENCE_REPORT_GOLDEN.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "evidence-report.json"
            result = verity_command(
                "generate",
                "evidence-report",
                "examples/evidence",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        datetime.fromisoformat(payload["generatedAt"])
        self.assertEqual(str(ROOT / "examples" / "evidence"), payload["workspacePath"])
        self.assertIsInstance(payload["verityVersion"], str)
        self.assertEqual(expected, normalize_evidence_report_for_golden(payload))

    def test_lifecycle_readiness_report_generator_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "lifecycle-readiness-report.json"
            result = verity_command(
                "generate",
                "lifecycle-readiness-report",
                LIFECYCLE_READINESS_EXAMPLE,
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertEqual("lifecycle_readiness_report", payload["type"])
        self.assertEqual(10, payload["summary"]["completeStages"])
        self.assertEqual(0, payload["summary"]["gapCount"])
        self.assertEqual(
            ["implementation-ready", "soft-launch", "launch-candidate"],
            [stage["id"] for stage in payload["stages"][:3]],
        )
        self.assertIn("does not assert commercial", payload["claimBoundaries"][1])

    def test_lifecycle_readiness_report_generator_matches_golden_file(self) -> None:
        expected = json.loads(LIFECYCLE_READINESS_GOLDEN.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "lifecycle-readiness-report.json"
            result = verity_command(
                "generate",
                "lifecycle-readiness-report",
                LIFECYCLE_READINESS_EXAMPLE,
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        datetime.fromisoformat(payload["generatedAt"])
        self.assertEqual(str(ROOT / LIFECYCLE_READINESS_EXAMPLE), payload["workspacePath"])
        self.assertIsInstance(payload["verityVersion"], str)
        self.assertEqual(expected, normalize_lifecycle_readiness_report_for_golden(payload))

    def test_coverage_dashboard_generator_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "coverage-dashboard.json"
            result = verity_command(
                "generate",
                "coverage-dashboard",
                COVERAGE_FIXTURE,
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertEqual("coverage_dashboard", payload["type"])
        self.assertEqual(127, payload["recordCount"])
        self.assertEqual(21, payload["summary"]["trackedSurfaces"])
        self.assertEqual(21, payload["summary"]["coveredSurfaces"])
        self.assertEqual(100.0, payload["summary"]["coveragePercent"])
        self.assertEqual([], payload["summary"]["releaseGaps"]["missingSurfaceRecords"])
        self.assertEqual("product.coverage_dashboard", payload["products"][0]["id"])

    def test_coverage_dashboard_generator_matches_golden_file(self) -> None:
        expected = json.loads(COVERAGE_DASHBOARD_GOLDEN.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "coverage-dashboard.json"
            result = verity_command(
                "generate",
                "coverage-dashboard",
                COVERAGE_FIXTURE,
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        datetime.fromisoformat(payload["generatedAt"])
        self.assertEqual(str(ROOT / COVERAGE_FIXTURE), payload["workspacePath"])
        self.assertIsInstance(payload["verityVersion"], str)
        self.assertEqual(expected, normalize_coverage_dashboard_for_golden(payload))

    def test_coverage_dashboard_generator_writes_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "coverage-dashboard.md"
            result = verity_command(
                "generate",
                "coverage-dashboard",
                COVERAGE_FIXTURE,
                "--format",
                "markdown",
                "--out",
                str(out_path),
            )

            text = out_path.read_text(encoding="utf-8")

        self.assertEqual(0, result.returncode)
        self.assertIn("Generated coverage-dashboard", result.stdout)
        self.assertTrue(text.startswith("# VeritySpec Coverage Dashboard\n"))
        self.assertIn("## Summary", text)
        self.assertIn("| Coverage percent | 100.0% |", text)
        self.assertIn("## Release Gaps", text)
        self.assertIn("## Surface Coverage", text)
        self.assertIn("## Product Surface References", text)
        self.assertIn("does not make legal, commercial", text)

    def test_decision_index_generator_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "decision-index.json"
            result = verity_command(
                "generate",
                "decision-index",
                "examples/product-delivery",
                "--generated-at",
                FIXED_GENERATED_AT,
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertIn("Generated decision-index", result.stdout)
        self.assertEqual("decision_index", payload["type"])
        self.assertEqual(FIXED_GENERATED_AT, payload["generatedAt"])
        self.assertEqual(1, payload["decisionCount"])
        self.assertEqual({"accepted": 1}, payload["summary"]["byDecisionStatus"])
        self.assertEqual([], payload["summary"]["indexGaps"]["orphanedDecisions"])

    def test_decision_index_generator_matches_golden_file(self) -> None:
        expected = json.loads(DECISION_INDEX_GOLDEN.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "decision-index.json"
            result = verity_command(
                "generate",
                "decision-index",
                "examples/product-delivery",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        datetime.fromisoformat(payload["generatedAt"])
        self.assertEqual(str(ROOT / "examples/product-delivery"), payload["workspacePath"])
        self.assertIsInstance(payload["verityVersion"], str)
        self.assertEqual(expected, normalize_decision_index_for_golden(payload))

    def test_decision_index_generator_writes_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "decision-index.md"
            result = verity_command(
                "generate",
                "decision-index",
                "examples/product-delivery",
                "--format",
                "markdown",
                "--generated-at",
                FIXED_GENERATED_AT,
                "--out",
                str(out_path),
            )

            text = out_path.read_text(encoding="utf-8")

        self.assertEqual(0, result.returncode)
        self.assertIn("Generated decision-index", result.stdout)
        self.assertTrue(text.startswith("# VeritySpec Decision Index\n"))
        self.assertIn(f"- Generated: `{FIXED_GENERATED_AT}`", text)
        self.assertIn("## Index Gaps", text)
        self.assertIn("decision.record.github_manages_workflow", text)
        self.assertIn("does not approve decisions", text)

    def test_decision_index_generator_stops_on_validation_errors(self) -> None:
        result = verity_command(
            "generate",
            "decision-index",
            "tests/fixtures/broken_semantics",
        )

        self.assertEqual(1, result.returncode)
        self.assertIn("reference.disallowed", result.stdout)
        self.assertIn("Generation validation", result.stdout)

    def test_agent_context_generator_writes_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "agent-context.md"
            result = verity_command(
                "generate",
                "agent-context",
                "examples/product-delivery",
                "--record",
                "agent-context.exporter.implementation_bundle",
                "--format",
                "markdown",
                "--generated-at",
                FIXED_GENERATED_AT,
                "--out",
                str(out_path),
            )

            text = out_path.read_text(encoding="utf-8")

        self.assertEqual(0, result.returncode)
        self.assertIn("Generated agent-context", result.stdout)
        self.assertTrue(text.startswith("# VeritySpec Agent Context\n"))
        self.assertIn(f"- Generated: `{FIXED_GENERATED_AT}`", text)
        self.assertIn("agent-context.exporter.implementation_bundle", text)
        self.assertIn("## Verification Commands", text)
        self.assertIn("AGENTS.md remains the canonical repository entry point", text)

    def test_agent_context_generator_requires_record(self) -> None:
        result = verity_command(
            "generate",
            "agent-context",
            "examples/product-delivery",
            "--format",
            "markdown",
        )

        self.assertEqual(2, result.returncode)
        self.assertIn("requires --record TARGET_ID", result.stderr)

    def test_agent_context_generator_rejects_json_format(self) -> None:
        result = verity_command(
            "generate",
            "agent-context",
            "examples/product-delivery",
            "--record",
            "agent-context.exporter.implementation_bundle",
        )

        self.assertEqual(2, result.returncode)
        self.assertIn("supports --format markdown only", result.stderr)

    def test_agent_context_generator_rejects_unknown_record(self) -> None:
        result = verity_command(
            "generate",
            "agent-context",
            "examples/product-delivery",
            "--record",
            "agent-context.exporter.missing",
            "--format",
            "markdown",
        )

        self.assertEqual(2, result.returncode)
        self.assertIn("target record not found", result.stderr)

    def test_agent_context_generator_rejects_unsupported_target_kind(self) -> None:
        result = verity_command(
            "generate",
            "agent-context",
            "examples/product-delivery",
            "--record",
            "product.scope.engine_toolkit_delivery",
            "--format",
            "markdown",
        )

        self.assertEqual(2, result.returncode)
        self.assertIn("target must be one of", result.stderr)

    def test_agent_context_generator_stops_on_validation_errors(self) -> None:
        result = verity_command(
            "generate",
            "agent-context",
            "tests/fixtures/broken_semantics",
            "--record",
            "agent-context.exporter.missing",
            "--format",
            "markdown",
        )

        self.assertEqual(1, result.returncode)
        self.assertIn("reference.disallowed", result.stdout)
        self.assertIn("Generation validation", result.stdout)

    def test_pack_capability_index_generator_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "pack-capability-index.json"
            result = verity_command(
                "generate",
                "pack-capability-index",
                CUSTOM_PACK_WORKSPACE,
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertIn("Generated pack-capability-index", result.stdout)
        self.assertEqual("pack_capability_index", payload["type"])
        self.assertEqual(2, payload["summary"]["packCount"])
        self.assertEqual(1, payload["summary"]["externalPackCount"])
        self.assertIn("feature.flag", payload["summary"]["recordKinds"])
        self.assertIn("pack-capability-index", payload["summary"]["generators"])

    def test_pack_capability_index_generator_matches_golden_file(self) -> None:
        expected = json.loads(PACK_CAPABILITY_INDEX_GOLDEN.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "pack-capability-index.json"
            result = verity_command(
                "generate",
                "pack-capability-index",
                CUSTOM_PACK_WORKSPACE,
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        datetime.fromisoformat(payload["generatedAt"])
        self.assertEqual(str(ROOT / CUSTOM_PACK_WORKSPACE), payload["workspacePath"])
        self.assertIsInstance(payload["verityVersion"], str)
        self.assertEqual(expected, normalize_pack_capability_index_for_golden(payload))

    def test_product_impact_generator_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "product-impact.json"
            result = verity_command(
                "generate",
                "product-impact",
                PRODUCT_IMPACT_BASELINE,
                PRODUCT_IMPACT_CURRENT,
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertIn("Generated product-impact", result.stdout)
        self.assertEqual("product_impact_report", payload["type"])
        self.assertEqual(6, payload["summary"]["changedRecordCount"])
        self.assertEqual(6, payload["summary"]["impactedRecordCount"])
        self.assertEqual(0, payload["summary"]["missingReferenceCount"])
        self.assertEqual("high", payload["summary"]["releaseReview"]["riskLevel"])
        self.assertTrue(payload["validation"]["old"]["passed"])
        self.assertTrue(payload["validation"]["new"]["passed"])

    def test_product_impact_generator_requires_comparison_workspace(self) -> None:
        result = verity_command(
            "generate",
            "product-impact",
            PRODUCT_IMPACT_BASELINE,
        )

        self.assertEqual(2, result.returncode)
        self.assertIn("requires OLD and NEW workspace paths", result.stderr)

    def test_single_workspace_generator_rejects_extra_comparison_workspace(self) -> None:
        result = verity_command(
            "generate",
            "coverage-dashboard",
            COVERAGE_FIXTURE,
            PRODUCT_IMPACT_CURRENT,
        )

        self.assertEqual(2, result.returncode)
        self.assertIn("accepts one workspace path", result.stderr)

    def test_product_impact_generator_matches_golden_file(self) -> None:
        expected = json.loads(PRODUCT_IMPACT_GOLDEN.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "product-impact.json"
            result = verity_command(
                "generate",
                "product-impact",
                PRODUCT_IMPACT_BASELINE,
                PRODUCT_IMPACT_CURRENT,
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        datetime.fromisoformat(payload["generatedAt"])
        self.assertEqual(str(ROOT / PRODUCT_IMPACT_BASELINE), payload["oldWorkspace"]["workspacePath"])
        self.assertEqual(str(ROOT / PRODUCT_IMPACT_CURRENT), payload["newWorkspace"]["workspacePath"])
        self.assertIsInstance(payload["verityVersion"], str)
        self.assertEqual(expected, normalize_product_impact_for_golden(payload))

    def test_explain_deployment_issue_code_json_output(self) -> None:
        result = verity_command(
            "explain",
            "deployment.target.production_release_controls_missing",
            "--format",
            "json",
        )

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual(
            "deployment.target.production_release_controls_missing",
            payload["code"],
        )
        self.assertEqual("Production deployment controls missing", payload["title"])

    def test_roadmap_report_generator_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "roadmap-report.json"
            result = verity_command(
                "generate",
                "roadmap-report",
                ".",
                "--out",
                str(out_path),
            )

            payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertIn("Generated roadmap-report", result.stdout)
        self.assertEqual("roadmap_report", payload["type"])
        self.assertEqual(str(ROOT / "ROADMAP.md"), payload["roadmapPath"])
        self.assertEqual(20, payload["summary"]["nextRoadmapPoints"])
        self.assertEqual(list(range(1, 21)), [point["number"] for point in payload["nextRoadmapPoints"]])

    def test_roadmap_report_generator_writes_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "roadmap-report.md"
            result = verity_command(
                "generate",
                "roadmap-report",
                ".",
                "--format",
                "markdown",
                "--out",
                str(out_path),
            )

            text = out_path.read_text(encoding="utf-8")

        self.assertEqual(0, result.returncode)
        self.assertIn("Generated roadmap-report", result.stdout)
        self.assertTrue(text.startswith("# VeritySpec Roadmap Report\n"))
        self.assertIn("## Summary", text)
        self.assertIn("| Next roadmap points | 20 |", text)
        self.assertIn("## Next 20 Roadmap Points", text)

    def test_markdown_format_is_limited_to_supported_report_artifacts(self) -> None:
        result = verity_command(
            "generate",
            "validation-report",
            "examples/basic",
            "--format",
            "markdown",
        )

        self.assertEqual(2, result.returncode)
        self.assertIn("generate validation-report supports --format json only.", result.stderr)

    def test_prismspec_import_reports_migration_details(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "imported"
            result = verity_command(
                "import",
                "prismspec",
                "tests/fixtures/prismspec_sample",
                "--out",
                str(out_path),
            )
            report = json.loads((out_path / "migration-report.json").read_text(encoding="utf-8"))
            workspace = json.loads((out_path / "verityspec.json").read_text(encoding="utf-8"))
            validation = verity_command("validate", str(out_path), "--format", "json")

        self.assertEqual(0, result.returncode)
        self.assertEqual(0, validation.returncode)
        self.assertEqual("not_wire_compatible", report["compatibility"])
        self.assertGreaterEqual(report["convertedRecordCount"], 5)
        self.assertGreaterEqual(report["skippedRecordCount"], 1)
        self.assertTrue(report["defaultsApplied"])
        self.assertIn("verity.pack.api", workspace["packs"])
        self.assertIn("verity.pack.cli", workspace["packs"])
        self.assertIn("verity.pack.events", workspace["packs"])

    def test_diff_reports_workspace_versions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = root / "old"
            new = root / "new"
            (old / "records").mkdir(parents=True)
            (new / "records").mkdir(parents=True)
            (old / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "old",
                        "specVersion": "v0.1.0",
                        "packs": ["verity.core"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (new / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "new",
                        "specVersion": "v0.1.0",
                        "packs": ["verity.core", "verity.pack.api"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )

            result = verity_command("diff", str(old), str(new), "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("v0.1.0", payload["versions"]["old"])
        self.assertIn("verity.pack.api", payload["packs"]["added"])
        self.assertEqual(1, payload["summary"]["totalChanges"])
        self.assertEqual(0, payload["summary"]["breakingChanges"])
        self.assertEqual({"info": 1, "warning": 0, "error": 0}, payload["summary"]["bySeverity"])
        self.assertEqual("pack.added", payload["changes"][0]["type"])
        self.assertFalse(payload["changes"][0]["breaking"])

    def test_diff_reports_severity_and_breaking_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = root / "old"
            new = root / "new"
            (old / "records").mkdir(parents=True)
            (new / "records").mkdir(parents=True)
            (old / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "old",
                        "specVersion": "v0.1.0",
                        "packs": ["verity.core", "verity.pack.api", "verity.pack.cli"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            (new / "verityspec.json").write_text(
                json.dumps(
                    {
                        "workspace": "new",
                        "specVersion": "v0.1.0",
                        "packs": ["verity.core", "verity.pack.api"],
                        "records": ["records/*.json"],
                    }
                ),
                encoding="utf-8",
            )
            api_record = {
                "id": "api.users.get",
                "kind": "api.endpoint",
                "name": "Get User",
                "status": "ready",
                "owner": "platform",
                "method": "GET",
                "path": "/users/{id}",
                "responses": [
                    {"statusCode": 200, "description": "User found.", "schema": "schema.user"},
                    {"statusCode": 404, "description": "User missing."},
                ],
            }
            schema_record = {
                "id": "schema.user",
                "kind": "schema.object",
                "name": "User",
                "status": "ready",
                "owner": "platform",
                "jsonSchema": {
                    "type": "object",
                    "required": ["id", "email", "status"],
                    "properties": {
                        "id": {"type": "string"},
                        "email": {"type": "string"},
                        "status": {"type": "string", "enum": ["active", "disabled"]},
                    },
                },
            }
            removed_command = {
                "id": "cli.users.get",
                "kind": "cli.command",
                "name": "Get User CLI",
                "status": "ready",
                "owner": "platform",
                "command": "users get",
            }
            changed_api = {
                **api_record,
                "path": "/members/{id}",
                "responses": [
                    {"statusCode": 200, "description": "User found.", "schema": "schema.user"},
                ],
            }
            changed_schema = {
                **schema_record,
                "jsonSchema": {
                    "type": "object",
                    "required": ["id", "status"],
                    "properties": {
                        "id": {"type": "string"},
                        "status": {"type": "string", "enum": ["active"]},
                    },
                },
            }
            (old / "records" / "api.json").write_text(json.dumps(api_record), encoding="utf-8")
            (old / "records" / "schema.json").write_text(json.dumps(schema_record), encoding="utf-8")
            (old / "records" / "cli.json").write_text(json.dumps(removed_command), encoding="utf-8")
            (new / "records" / "api.json").write_text(json.dumps(changed_api), encoding="utf-8")
            (new / "records" / "schema.json").write_text(json.dumps(changed_schema), encoding="utf-8")

            json_result = verity_command("diff", str(old), str(new), "--format", "json")
            text_result = verity_command("diff", str(old), str(new))

        self.assertEqual(0, json_result.returncode)
        payload = json.loads(json_result.stdout)
        self.assertEqual(["cli.users.get"], payload["removed"])
        self.assertEqual(["api.users.get", "schema.user"], payload["changed"])
        self.assertEqual(4, payload["summary"]["totalChanges"])
        self.assertEqual(4, payload["summary"]["breakingChanges"])
        self.assertEqual({"info": 0, "warning": 0, "error": 4}, payload["summary"]["bySeverity"])

        changes_by_type = {change["type"]: change for change in payload["changes"]}
        self.assertTrue(changes_by_type["pack.removed"]["breaking"])
        self.assertEqual("verity.pack.cli", changes_by_type["pack.removed"]["packId"])

        changes_by_record = {
            change["recordId"]: change
            for change in payload["changes"]
            if "recordId" in change
        }
        self.assertTrue(changes_by_record["cli.users.get"]["breaking"])
        self.assertIn("API endpoint path changed", " ".join(changes_by_record["api.users.get"]["reasons"]))
        self.assertIn("API endpoint responses removed", " ".join(changes_by_record["api.users.get"]["reasons"]))
        self.assertIn("jsonSchema.properties removed", " ".join(changes_by_record["schema.user"]["reasons"]))
        self.assertIn("enum removed", " ".join(changes_by_record["schema.user"]["reasons"]))

        self.assertEqual(0, text_result.returncode)
        self.assertIn("Breaking changes: 4", text_result.stdout)
        self.assertIn("[error] record.changed api.users.get", text_result.stdout)
        self.assertIn("[error] record.removed cli.users.get", text_result.stdout)


if __name__ == "__main__":
    unittest.main()
