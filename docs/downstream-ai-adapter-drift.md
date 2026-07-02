# Downstream AI Adapter Drift Checks

Downstream repositories can keep agent-specific adapter files for tools such
as Codex, Claude, Claude Code, ChatGPT, Gemini, GitHub Copilot, Unity AI, and
other coding agents. Those files should stay thin. They point agents to the
canonical repository entry point; they do not define independent repository
policy.

This guidance follows the organization-wide
`organization-patterns/patterns/ai-entry-point-baseline.md` pattern. If this
repository and the organization pattern disagree, treat the organization
pattern plus the active repository `AGENTS.md` as the source of truth and open
a follow-up issue instead of silently copying new policy into adapter files.

## Canonical Rule

Every downstream repository should have:

- A repository-level `AGENTS.md` with the active repository operating rules.
- A workspace-level entry point when the repository lives inside a shared
  workspace that has one.
- Optional agent-specific adapters such as `CODEX.md`, `CLAUDE.md`,
  `CHATGPT.md`, `GEMINI.md`, `UNITY_AI.md`, and
  `.github/copilot-instructions.md`.

Adapters should say only where the canonical entry point is. They should not
include branch strategy, test commands, release rules, shell rules, VeritySpec
commands, GitHub workflow rules, or local product policy. That keeps all AI
agents working from the same instructions after every context refresh.

## Drift Checklist

Use this checklist when reviewing a sibling repository:

- `AGENTS.md` exists and names itself as the canonical AI-agent entry point.
- `AGENTS.md` references the organization AI entry-point baseline.
- `AGENTS.md` requires paired workspace/repository entry-point reads when a
  workspace-level entry point exists.
- `AGENTS.md` requires entry shell discipline for `zsh`, `bash`, or
  PowerShell.
- `AGENTS.md` requires post-commit context refresh.
- `AGENTS.md` requires consulting `organization-patterns` and
  `organization-glossary` before creating reusable practices or durable terms.
- `AGENTS.md` keeps release, deploy, publish, package, and store-submission
  actions behind explicit operator approval.
- Adapter files point back to `AGENTS.md`.
- Adapter files do not contain independent commands, test matrices, release
  instructions, roadmap instructions, or product policy.
- Adapter files do not weaken the canonical entry point.

When a repository lacks the baseline, record or open a follow-up issue for the
appropriate repository. Large organization-wide adapter backfills should be
batched and reviewed through normal issue, branch, PR, and CI flow.

## Suggested Adapter Shape

Use this shape for plain Markdown adapters:

```markdown
# Codex Instructions

Read `AGENTS.md` first. It is the canonical AI-agent entry point for this
repository.
```

Use the same wording for other agents, changing only the heading when needed.
GitHub Copilot can use the same body in `.github/copilot-instructions.md`.

## Review Commands

These commands are optional review aids. They do not replace reading the files.

```bash
rg -n "pytest|git push|git tag|verity |release|deploy|publish|store" CODEX.md CLAUDE.md CHATGPT.md GEMINI.md UNITY_AI.md .github/copilot-instructions.md
rg -n "organization-patterns|organization-glossary|Post-Commit Refresh|Shell Discipline|Agent Adapter Policy" AGENTS.md
```

The first command should usually return no matches for thin adapters. The
second command should confirm that the canonical entry point contains the
baseline operating rules.

## Boundaries

This guidance does not require every downstream repository to use the exact
same `AGENTS.md` text. Each repository still owns its local build, test,
release, and product rules. The shared requirement is that durable operating
rules live in the canonical entry point, while agent-specific files remain
short pointers.

This guidance also does not authorize publishing, deploying, tagging,
submitting store builds, changing legal/support policy, or editing
organization-wide patterns without the normal approval and PR process.
