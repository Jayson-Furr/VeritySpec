from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import unittest

from verityspec.packs import load_pack_registry
from verityspec.readiness import evaluate_readiness
from verityspec.validation import lint_workspace, validate_workspace
from verityspec.versions import SUPPORTED_SPEC_VERSIONS
from verityspec.workspace import load_workspace


ROOT = Path(__file__).resolve().parents[1]
POSITIVE_EXAMPLES = [
    ROOT / "examples" / "basic",
    ROOT / "examples" / "api-service",
    ROOT / "examples" / "cli-tool",
    ROOT / "examples" / "events",
    ROOT / "examples" / "security",
    ROOT / "examples" / "observability",
]
COMPATIBILITY_WORKSPACES = POSITIVE_EXAMPLES + [
    ROOT / "tests" / "fixtures" / "generator_maturity",
]
COMPATIBILITY_SPEC_VERSIONS = sorted(SUPPORTED_SPEC_VERSIONS)


def write_compatibility_config(path: Path, spec_version: str) -> None:
    config_path = path / "verityspec.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["specVersion"] = spec_version
    if spec_version == "v0.2.0":
        config["packPaths"] = config.get("packPaths", [])
    else:
        config.pop("packPaths", None)
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")


class ExampleWorkspaceTests(unittest.TestCase):
    def test_positive_examples_validate_lint_and_pass_readiness(self) -> None:
        for path in POSITIVE_EXAMPLES:
            with self.subTest(path=path):
                workspace = load_workspace(path)
                registry = load_pack_registry(workspace.pack_ids)

                self.assertEqual([], validate_workspace(workspace, registry, strict=True))
                self.assertEqual([], lint_workspace(workspace, registry, strict=True))
                self.assertEqual([], evaluate_readiness(workspace, registry, strict=True))

    def test_positive_fixture_matrix_supports_workspace_versions(self) -> None:
        for source_path in COMPATIBILITY_WORKSPACES:
            for spec_version in COMPATIBILITY_SPEC_VERSIONS:
                with self.subTest(path=source_path, spec_version=spec_version):
                    with tempfile.TemporaryDirectory() as tmp:
                        workspace_path = Path(tmp) / source_path.name
                        shutil.copytree(source_path, workspace_path)
                        write_compatibility_config(workspace_path, spec_version)

                        workspace = load_workspace(workspace_path)
                        registry = load_pack_registry(
                            workspace.pack_ids,
                            workspace.pack_paths,
                            workspace.base_path,
                        )

                        self.assertEqual([], validate_workspace(workspace, registry, strict=True))
                        self.assertEqual([], lint_workspace(workspace, registry, strict=True))
                        self.assertEqual([], evaluate_readiness(workspace, registry, strict=True))

    def test_broken_example_fails_with_expected_issue_codes(self) -> None:
        workspace = load_workspace(ROOT / "examples" / "broken")
        registry = load_pack_registry(workspace.pack_ids)

        issues = validate_workspace(workspace, registry)
        codes = {issue.code for issue in issues}

        self.assertIn("reference.missing", codes)
        self.assertIn("reference.disallowed", codes)


if __name__ == "__main__":
    unittest.main()
