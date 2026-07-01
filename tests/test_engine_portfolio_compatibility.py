from __future__ import annotations

import unittest
from pathlib import Path

from verityspec.graph import build_graph
from verityspec.packs import load_pack_registry
from verityspec.readiness import evaluate_readiness
from verityspec.validation import lint_workspace, validate_workspace
from verityspec.workspace import load_workspace


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "engine_portfolio"
ENGINE_PORTFOLIO_WORKSPACES = [
    FIXTURES / "shared-game-core",
    FIXTURES / "unity-game",
    FIXTURES / "godot-game",
    FIXTURES / "unreal-game",
    FIXTURES / "portfolio",
]


class EnginePortfolioCompatibilityTests(unittest.TestCase):
    def test_engine_portfolio_workspaces_validate_lint_and_pass_readiness(self) -> None:
        for path in ENGINE_PORTFOLIO_WORKSPACES:
            with self.subTest(path=path):
                workspace = load_workspace(path)
                registry = load_pack_registry(
                    workspace.pack_ids,
                    workspace.pack_paths,
                    workspace.base_path,
                )

                self.assertEqual([], validate_workspace(workspace, registry, strict=True))
                self.assertEqual([], lint_workspace(workspace, registry, strict=True))
                self.assertEqual([], evaluate_readiness(workspace, registry, strict=True))

    def test_portfolio_fixture_graph_shows_all_engines_and_shared_game_core(self) -> None:
        workspace = load_workspace(FIXTURES / "portfolio")
        graph = build_graph(workspace)

        node_ids = {node["id"] for node in graph["nodes"]}
        for record_id in [
            "product.engine_portfolio_matrix",
            "product.engine_portfolio_unity_game",
            "product.engine_portfolio_godot_game",
            "product.engine_portfolio_unreal_game",
            "unity.project.engine_portfolio_game",
            "godot.project.engine_portfolio_game",
            "unreal.project.engine_portfolio_game",
            "sharedGame::game.product.engine_portfolio_baseline",
            "sharedGame::game.mode.engine_portfolio_session",
            "sharedGame::game.loop.engine_portfolio_validate_ship",
            "sharedGame::game.prototype-scope.engine_portfolio_engine_slice",
        ]:
            with self.subTest(record_id=record_id):
                self.assertIn(record_id, node_ids)

        self.assertEqual(
            [
                {
                    "id": "studio.shared.game_core",
                    "alias": "sharedGame",
                    "source": "../shared-game-core",
                    "version": "1.0.0",
                    "exportedRecords": [
                        "game.loop.engine_portfolio_validate_ship",
                        "game.mode.engine_portfolio_session",
                        "game.product.engine_portfolio_baseline",
                        "game.prototype-scope.engine_portfolio_engine_slice",
                    ],
                }
            ],
            graph["dependencies"],
        )

    def test_portfolio_fixture_records_dependency_alias_and_engine_edges(self) -> None:
        workspace = load_workspace(FIXTURES / "portfolio")
        graph = build_graph(workspace)
        edges = {
            (edge["source"], edge["relationship"], edge["target"])
            for edge in graph["edges"]
        }

        for edge in [
            (
                "product.engine_portfolio_matrix",
                "describes",
                "sharedGame::game.product.engine_portfolio_baseline",
            ),
            (
                "product.engine_portfolio_matrix",
                "hasUnityProject",
                "unity.project.engine_portfolio_game",
            ),
            (
                "product.engine_portfolio_matrix",
                "hasGodotProject",
                "godot.project.engine_portfolio_game",
            ),
            (
                "product.engine_portfolio_matrix",
                "hasUnrealProject",
                "unreal.project.engine_portfolio_game",
            ),
            (
                "product.engine_portfolio_unity_game",
                "describes",
                "sharedGame::game.product.engine_portfolio_baseline",
            ),
            (
                "product.engine_portfolio_godot_game",
                "describes",
                "sharedGame::game.product.engine_portfolio_baseline",
            ),
            (
                "product.engine_portfolio_unreal_game",
                "describes",
                "sharedGame::game.product.engine_portfolio_baseline",
            ),
        ]:
            with self.subTest(edge=edge):
                self.assertIn(edge, edges)

    def test_engine_portfolio_docs_are_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        portfolio_note = (ROOT / "docs" / "portfolio-validation.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/engine-portfolio-compatibility.md", readme)
        self.assertIn(
            "tests/fixtures/engine_portfolio/portfolio/verityspec.json",
            readme,
        )
        self.assertIn("engine portfolio compatibility fixture", portfolio_note)


if __name__ == "__main__":
    unittest.main()
