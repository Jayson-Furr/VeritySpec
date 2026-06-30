from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "docs" / "fixtures" / "pack-scaffold"
FIXTURE_PACK = FIXTURE_ROOT / "packs" / "features"
FIXTURE_WORKSPACE = FIXTURE_ROOT / "workspace"
FIXTURE_DOC = ROOT / "docs" / "pack-scaffold-fixtures.md"


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


class PackScaffoldFixtureTests(unittest.TestCase):
    def test_pack_scaffold_fixture_is_documented(self) -> None:
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        readme = (FIXTURE_ROOT / "README.md").read_text(encoding="utf-8")
        doc = FIXTURE_DOC.read_text(encoding="utf-8")

        self.assertIn("docs/pack-scaffold-fixtures.md", root_readme)
        for text in [readme, doc]:
            self.assertIn("docs/fixtures/pack-scaffold", text)
            self.assertIn("verity pack init verity.pack.features", text)
            self.assertIn("verity pack validate verity.pack.features", text)
            self.assertIn("verity validate docs/fixtures/pack-scaffold/workspace", text)
            self.assertIn("verity generate schema-bundle", text)
            self.assertIn("verity generate pack-capability-index", text)

    def test_committed_pack_fixture_matches_generated_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            generated_pack = Path(tmp) / "packs" / "features"
            result = verity_command(
                "pack",
                "init",
                "verity.pack.features",
                "--out",
                str(generated_pack),
                "--kind",
                "feature.flag",
                "--name",
                "Feature Pack",
                "--description",
                "Feature flag records for pack scaffold documentation.",
            )

            generated_manifest = json.loads((generated_pack / "pack.json").read_text(encoding="utf-8"))
            generated_schema = json.loads(
                (generated_pack / "schemas" / "feature-flag.schema.json").read_text(encoding="utf-8")
            )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            generated_manifest,
            json.loads((FIXTURE_PACK / "pack.json").read_text(encoding="utf-8")),
        )
        self.assertEqual(
            generated_schema,
            json.loads((FIXTURE_PACK / "schemas" / "feature-flag.schema.json").read_text(encoding="utf-8")),
        )

    def test_pack_scaffold_workspace_executes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            bundle_path = tmp_root / "pack-scaffold-schema-bundle.json"
            capability_path = tmp_root / "pack-scaffold-capability-index.json"
            pack_validate = verity_command(
                "pack",
                "validate",
                "verity.pack.features",
                "--path",
                str(FIXTURE_PACK),
                "--format",
                "json",
            )
            validate = verity_command("validate", str(FIXTURE_WORKSPACE), "--format", "json")
            lint = verity_command("lint", str(FIXTURE_WORKSPACE), "--strict", "--format", "json")
            readiness = verity_command("readiness", str(FIXTURE_WORKSPACE), "--strict", "--format", "json")
            schema_bundle = verity_command(
                "generate",
                "schema-bundle",
                str(FIXTURE_WORKSPACE),
                "--out",
                str(bundle_path),
            )
            capability_index = verity_command(
                "generate",
                "pack-capability-index",
                str(FIXTURE_WORKSPACE),
                "--out",
                str(capability_path),
            )
            bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
            capability = json.loads(capability_path.read_text(encoding="utf-8"))

        for result in [pack_validate, validate, lint, readiness, schema_bundle, capability_index]:
            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
        self.assertTrue(json.loads(pack_validate.stdout)["passed"])
        self.assertTrue(json.loads(validate.stdout)["passed"])
        self.assertTrue(json.loads(lint.stdout)["passed"])
        self.assertTrue(json.loads(readiness.stdout)["passed"])
        self.assertIn("feature.flag", bundle["schemas"])
        self.assertIn("feature.flag", capability["summary"]["recordKinds"])
        self.assertEqual(1, capability["summary"]["externalPackCount"])


if __name__ == "__main__":
    unittest.main()
