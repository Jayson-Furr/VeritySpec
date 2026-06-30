from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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


if __name__ == "__main__":
    unittest.main()
