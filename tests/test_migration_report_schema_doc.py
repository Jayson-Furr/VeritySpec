from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "migration-report-schema.md"
SCHEMA = ROOT / "docs" / "schemas" / "migration-report.schema.json"
MIGRATION_FIXTURES = ROOT / "tests" / "fixtures" / "migration"


def verity_command(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [sys.executable, "-m", "verityspec", *args],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def load_schema_validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


class MigrationReportSchemaDocTests(unittest.TestCase):
    def test_schema_doc_is_publicly_linked(self) -> None:
        sources = [
            ROOT / "README.md",
            ROOT / "docs" / "ci.md",
            ROOT / "docs" / "versioning-and-migrations.md",
            ROOT / "docs" / "workspace-format.md",
        ]

        for source in sources:
            with self.subTest(source=source.relative_to(ROOT)):
                text = source.read_text(encoding="utf-8")
                self.assertIn("migration-report-schema.md", text)

    def test_schema_doc_defines_report_contract(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "docs/schemas/migration-report.schema.json",
            "verityspec_migration_report",
            "verityspec_migration_capabilities",
            "PrismSpec importer reports are also separate",
            "workspaceFormat",
            "manualFollowUp",
            "blocked",
            "changeCount",
            "The schema is additive.",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_schema_validates_current_migration_reports(self) -> None:
        validator = load_schema_validator()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            legacy = tmp_root / "legacy_workspace"
            future = tmp_root / "future_workspace"
            report_out = tmp_root / "reports" / "migration-report.json"
            shutil.copytree(MIGRATION_FIXTURES / "legacy_workspace", legacy)
            shutil.copytree(ROOT / "examples" / "basic", future)
            future_config = json.loads((future / "verityspec.json").read_text(encoding="utf-8"))
            future_config["specVersion"] = "v99.0.0"
            (future / "verityspec.json").write_text(json.dumps(future_config, indent=2) + "\n", encoding="utf-8")

            cases = [
                (verity_command("migrate", str(legacy), "--dry-run", "--format", "json"), 0),
                (verity_command("migrate", str(legacy), "--format", "json", "--report-out", str(report_out)), 0),
                (verity_command("migrate", str(ROOT / "examples" / "basic"), "--to", "v0.1.0", "--format", "json"), 1),
                (verity_command("migrate", str(future), "--format", "json"), 1),
                (
                    verity_command(
                        "migrate",
                        str(ROOT / "examples" / "basic"),
                        "--to",
                        "v99.0.0",
                        "--format",
                        "json",
                    ),
                    1,
                ),
            ]

            for result, expected_returncode in cases:
                with self.subTest(stdout=result.stdout, stderr=result.stderr):
                    self.assertEqual(expected_returncode, result.returncode, result.stderr)
                    validator.validate(json.loads(result.stdout))

            self.assertTrue(report_out.exists())
            validator.validate(json.loads(report_out.read_text(encoding="utf-8")))

    def test_schema_requires_stable_report_identity(self) -> None:
        validator = load_schema_validator()
        invalid_report = {
            "type": "unexpected",
            "source": "/tmp/workspace",
            "targetVersion": "v0.2.0",
            "dryRun": True,
            "changed": False,
            "blocked": False,
            "migrationPath": [],
            "impactSummary": {
                "workspaceFormat": [],
                "records": [],
                "packs": [],
                "generators": [],
            },
            "availableTargets": [],
            "changes": [],
            "changeCount": 0,
            "filesWritten": [],
            "manualFollowUp": [],
            "fromVersionKey": "v0.2.0",
        }

        errors = list(validator.iter_errors(invalid_report))
        self.assertTrue(any(error.path == ("type",) or list(error.path) == ["type"] for error in errors))


if __name__ == "__main__":
    unittest.main()
