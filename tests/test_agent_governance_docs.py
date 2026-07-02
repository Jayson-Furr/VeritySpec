from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT_CONTEXT_DOC = ROOT / "docs" / "agent-context-generation.md"
ADAPTER_DRIFT_DOC = ROOT / "docs" / "downstream-ai-adapter-drift.md"
ADR_DOC = ROOT / "docs" / "architecture-decision-records.md"
ADR_TEMPLATE = ROOT / "docs" / "adr-template.md"
ADAPTER_FILES = [
    ROOT / "CODEX.md",
    ROOT / "CLAUDE.md",
    ROOT / "GEMINI.md",
    ROOT / "CHATGPT.md",
    ROOT / "UNITY_AI.md",
    ROOT / ".github" / "copilot-instructions.md",
]


class AgentGovernanceDocTests(unittest.TestCase):
    def test_agent_context_design_note_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/agent-context-generation.md", readme)

    def test_agent_context_design_note_defines_bounded_handoff_contract(self) -> None:
        text = AGENT_CONTEXT_DOC.read_text(encoding="utf-8")

        for phrase in [
            "bounded implementation context",
            "workspace as the source of truth",
            "agent-context.exporter",
            "unity.agent-context-exporter",
            "Relevant records",
            "Contract constraints",
            "Readiness gates and evidence requirements",
            "prohibited drift",
            "Determinism",
            "first implementation is a Markdown handoff artifact",
            "AGENTS.md",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_adr_process_and_template_are_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/architecture-decision-records.md", readme)
        self.assertIn("docs/adr-template.md", readme)

    def test_downstream_ai_adapter_drift_guidance_is_publicly_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/downstream-ai-adapter-drift.md", readme)

    def test_downstream_ai_adapter_drift_guidance_preserves_baseline(self) -> None:
        text = ADAPTER_DRIFT_DOC.read_text(encoding="utf-8")

        for phrase in [
            "organization-patterns/patterns/ai-entry-point-baseline.md",
            "AGENTS.md",
            "canonical AI-agent entry point",
            "Adapters should say only where the canonical entry point is.",
            "Drift Checklist",
            "post-commit context refresh",
            "organization-patterns",
            "organization-glossary",
            "release, deploy, publish, package, and store-submission",
            "Adapter files do not contain independent commands",
            "Suggested Adapter Shape",
            "rg -n",
            "does not authorize publishing, deploying, tagging",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_adr_process_defines_review_and_status_contract(self) -> None:
        text = ADR_DOC.read_text(encoding="utf-8")

        for phrase in [
            "Architecture decision records",
            "pack architecture",
            "generator behavior",
            "workspace format compatibility",
            "AI-agent operating rules",
            "Proposed",
            "Accepted",
            "Superseded",
            "Rejected",
            "Verification plan",
            "Rollback or supersession criteria",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_adr_template_preserves_required_sections(self) -> None:
        text = ADR_TEMPLATE.read_text(encoding="utf-8")

        for phrase in [
            "## Context",
            "## Decision",
            "## Rationale",
            "## Alternatives Considered",
            "## Consequences",
            "## Compatibility And Migration",
            "## Verification",
            "## Rollback Or Supersession",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_ai_agent_adapter_files_remain_thin_pointers(self) -> None:
        for path in ADAPTER_FILES:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                non_empty_lines = [line for line in text.splitlines() if line.strip()]

                self.assertLessEqual(len(non_empty_lines), 4)
                self.assertIn("Read `AGENTS.md` first.", text)
                self.assertIn("canonical AI-agent entry point", text)
                self.assertNotIn("pytest", text)
                self.assertNotIn("git push", text)
                self.assertNotIn("verity ", text)

    def test_agent_adapter_policy_names_current_adapters(self) -> None:
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

        for path in ADAPTER_FILES:
            with self.subTest(path=path.name):
                self.assertIn(path.name, text)
        self.assertIn("thin pointers to this file", text)


if __name__ == "__main__":
    unittest.main()
