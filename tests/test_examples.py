from __future__ import annotations

from pathlib import Path

import unittest

from verityspec.packs import load_pack_registry
from verityspec.readiness import evaluate_readiness
from verityspec.validation import lint_workspace, validate_workspace
from verityspec.workspace import load_workspace


ROOT = Path(__file__).resolve().parents[1]
POSITIVE_EXAMPLES = [
    ROOT / "examples" / "basic",
    ROOT / "examples" / "api-service",
    ROOT / "examples" / "cli-tool",
    ROOT / "examples" / "events",
]


class ExampleWorkspaceTests(unittest.TestCase):
    def test_positive_examples_validate_lint_and_pass_readiness(self) -> None:
        for path in POSITIVE_EXAMPLES:
            with self.subTest(path=path):
                workspace = load_workspace(path)
                registry = load_pack_registry(workspace.pack_ids)

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

