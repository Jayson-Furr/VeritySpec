from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "cli-command-modules.md"


class CliCommandModuleDocTests(unittest.TestCase):
    def test_cli_command_module_design_note_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        adr_doc = (ROOT / "docs" / "architecture-decision-records.md").read_text(encoding="utf-8")
        branching = (ROOT / "docs" / "branching.md").read_text(encoding="utf-8")

        self.assertIn("docs/cli-command-modules.md", readme)
        self.assertIn("cli-command-modules.md", adr_doc)
        self.assertIn("cli-command-modules.md", branching)

    def test_cli_command_module_design_note_defines_module_boundaries(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "No runtime command movement is introduced by this design note.",
            "verityspec.commands",
            "register_all",
            "commands.common",
            "Command Registration Contract",
            "Shared Helpers",
            "Suggested Migration Phases",
            "Compatibility Guardrails",
            "Test Expectations",
            "First Implementation Gate",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_cli_command_module_design_note_preserves_non_goals(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "move command implementations",
            "change public command names, arguments, output formats, or exit codes",
            "introduce a new CLI framework",
            "add dependency, portfolio, lifecycle, or agent-context commands",
            "detach specialized packs from the core package",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_cli_command_module_design_note_names_compatibility_surfaces(self) -> None:
        text = DOC.read_text(encoding="utf-8")

        for phrase in [
            "verity --version",
            "current exit-code meanings",
            "text and JSON output contracts",
            "stable issue-code payloads",
            "GitHub Actions annotation behavior",
            "README command smoke-test coverage",
            "downstream workflow examples",
            "release-integrity surfaces",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
