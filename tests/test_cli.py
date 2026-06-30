from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CUSTOM_PACK = "tests/fixtures/custom_pack"
CUSTOM_PACK_WORKSPACE = "tests/fixtures/custom_pack_workspace"


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


class VerityCliTests(unittest.TestCase):
    def test_version_command(self) -> None:
        result = verity_command("--version")

        self.assertEqual(0, result.returncode)
        self.assertIn("verity 0.9.0", result.stdout)

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

    def test_doctor_json_output(self) -> None:
        result = verity_command("doctor", "examples/basic", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual("doctor", payload["command"])
        self.assertEqual(8, payload["records"])

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

    def test_migrate_dry_run_reports_without_writing(self) -> None:
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

            result = verity_command("migrate", str(root), "--dry-run", "--format", "json")
            report = json.loads(result.stdout)
            config = json.loads(config_path.read_text(encoding="utf-8"))
            record = json.loads(record_path.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode)
        self.assertTrue(report["changed"])
        self.assertEqual("v0.2.0", report["targetVersion"])
        self.assertEqual(
            ["legacy-to-v0.1.0", "v0.1.0-to-v0.2.0"],
            [step["id"] for step in report["migrationPath"]],
        )
        self.assertEqual([], report["filesWritten"])
        self.assertNotIn("specVersion", config)
        self.assertEqual("product", record["type"])

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
        self.assertIn("verity.pack.observability", pack_ids)
        self.assertIn("verity.pack.security", pack_ids)

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
        self.assertEqual("feature.flag", schema["properties"]["kind"]["const"])
        self.assertEqual(0, validate_result.returncode)
        self.assertTrue(json.loads(validate_result.stdout)["passed"])
        pack_ids = {pack["id"] for pack in json.loads(list_result.stdout)["packs"]}
        self.assertIn("verity.pack.features", pack_ids)

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

        self.assertEqual(0, validate_result.returncode)
        self.assertEqual(0, pack_list_result.returncode)
        self.assertEqual(0, pack_validate_result.returncode)
        pack_ids = {pack["id"] for pack in json.loads(pack_list_result.stdout)["packs"]}
        self.assertIn("verity.pack.features", pack_ids)

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
        self.assertEqual("security.control.account_access", payload["controls"][0]["id"])

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


if __name__ == "__main__":
    unittest.main()
