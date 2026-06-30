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
        self.assertIn("verity 0.1.0", result.stdout)

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

    def test_explain_issue_code_json_output(self) -> None:
        result = verity_command("explain", "reference.missing", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("reference.missing", payload["code"])
        self.assertEqual("Missing reference target", payload["title"])

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
        self.assertEqual("v0.1.0", config["specVersion"])
        self.assertNotIn("version", config)
        self.assertIn("verity.core", config["packs"])
        self.assertEqual("product", record["kind"])
        self.assertEqual("Legacy Product", record["name"])
        self.assertEqual("ready", record["status"])
        self.assertEqual("unknown", record["owner"])
        self.assertEqual("0.1.0", record["version"])
        self.assertNotIn("type", record)
        self.assertNotIn("displayName", record)

    def test_pack_list_json_output(self) -> None:
        result = verity_command("pack", "list", "--format", "json")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        pack_ids = {pack["id"] for pack in payload["packs"]}
        self.assertIn("verity.core", pack_ids)
        self.assertIn("verity.pack.api", pack_ids)

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
