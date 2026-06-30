# Branching Strategy

VeritySpec keeps `main` releasable. Sprint and feature work happens on branches
and merges back only after verification.

Starting with the first sprint after `v0.38.0`, plan sprint branches as
cohesive bundles of related work sized up to roughly one week of development effort.
Avoid splitting tightly related work into many tiny sprint branches when it can
be implemented, verified, reviewed, and released as one clean bundle.

## Branch Types

- `main`: stable release branch. Tags and GitHub releases are cut from `main`.
- `sprint/<number>-<topic>`: sprint implementation branch, such as
  `sprint/13-openapi-parameters`.
- `feature/<topic>`: focused feature branch outside a numbered sprint.
- `fix/<topic>`: narrow bug fix branch.
- `docs/<topic>`: documentation-only branch when not part of a sprint branch.
- `release/<version>`: optional release-preparation branch for larger releases.

## Rules

- Start new implementation work from the latest `origin/main`.
- Do not commit sprint or feature work directly to `main`.
- Keep branch names lowercase and descriptive.
- Keep commits scoped and tied to the current issue when possible.
- Run local checks before pushing a branch.
- Push the branch and use GitHub Actions as the normal verification gate.
- If GitHub Actions is unavailable because of billing, credits, quota, runner
  availability, or another platform issue, run the equivalent local checks and
  document that CI was unavailable for external reasons.
- Merge back to `main` only after checks pass or the local-verification fallback
  has been explicitly recorded.
- After merging, verify `main` and keep `ROADMAP.md`, `CHANGELOG.md`, and
  `README.md` aligned with the completed work.

## AI Agent Requirements

AI agents must determine the correct branch before editing files. If work starts
on `main` by mistake, create the proper branch before committing.

At each commit boundary, agents must refresh context by re-reading `AGENTS.md`,
checking `git status`, and checking the latest commit.

AI agents must not create tags, GitHub releases, or PyPI publishes unless the
user explicitly asks for that release action.
