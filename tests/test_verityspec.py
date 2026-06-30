from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from verityspec.generators import generate_openapi
from verityspec.envelope import RECORD_ENVELOPE_REQUIRED
from verityspec.packs import load_pack_registry
from verityspec.readiness import evaluate_readiness
from verityspec.validation import validate_workspace
from verityspec.workspace import load_workspace


ROOT = Path(__file__).resolve().parents[1]


class VeritySpecTests(unittest.TestCase):
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

        self.assertTrue(any(issue.code == "reference.missing" for issue in issues))

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

        self.assertTrue(any(issue.code == "readiness.required" for issue in issues))

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


if __name__ == "__main__":
    unittest.main()
