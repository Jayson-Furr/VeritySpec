# AI Agent Entry Point

This is the canonical instruction file for AI agents working in this
repository. Agent-specific files are adapters only; if they conflict with this
file, `AGENTS.md` wins.

This entry point is intended for Codex, GitHub Copilot, Claude, Claude Code,
ChatGPT, Gemini, Unity AI, and other coding agents.

## Organization Entry-Point Baseline

This file follows the organization-wide AI entry-point baseline in
`../organization-patterns/patterns/ai-entry-point-baseline.md`. When updating
this file or sibling repository entry points, preserve the baseline
requirements for paired workspace/repository reads, shell discipline,
organization pattern and glossary consultation, work ledgers, content
opportunity handling, VeritySpec feedback issues, post-commit refresh,
clean-main issue sweeps, user-change preservation, secret protection, and
explicit approval gates for release, deploy, publish, package, and store
submission actions.

If another organization repository lacks this baseline, record or follow a
tracking issue such as `Jason-Furr/organization-patterns#6` unless the current
task explicitly authorizes updating that repository.

All organization AI agents should encounter these requirements through their
active entry points. Do not rely on conversation history, private notes, or
agent-specific adapters to carry the baseline; keep `AGENTS.md` files and
workspace-level entry points aligned with the organization pattern so agents
refreshing context get the same operating rules.

## Project Identity

VeritySpec is an executable product-contract framework. It is not a static
schema catalog.

The core promise is:

> Executable product contracts for humans, tools, and agents.

Treat PrismSpec only as historical input for the importer. Do not expand
VeritySpec by recreating a broad static PrismSpec-style catalog.

## VeritySpec Feedback Loop

When an agent discovers a VeritySpec bug, schema gap, unclear validation result, missing rule, workflow friction, documentation issue, or reusable improvement opportunity while working in this organization, the agent must open an issue in `Jason-Furr/verity-spec` before considering the discovery resolved.

The issue should include the source repository/path, the observed behavior or gap, expected behavior, reproduction or validation command when available, impact/severity, and whether the finding blocks current work. Do not silently work around VeritySpec problems only inside this repository. If GitHub issue creation is unavailable, record the issue candidate in the active work ledger and tell the operator explicitly.

## Architecture Summary

The repository is a Python package with a CLI named `verity`.

Core concepts:

- Workspace: directory with `verityspec.json` and record files.
- Pack: extension unit that contributes schemas, readiness gates, reference
  rules, and generator support. Packs may be bundled, discovered from
  installed Python package entry points, or loaded from explicit local
  `packPaths`.
- Record: product-contract object with shared envelope fields.
- Reference graph: relationships between records.
- Validation issue: stable issue code plus severity, message, and location.
- Readiness gate: pack-declared release-readiness requirement.
- Generator: artifact emitter such as OpenAPI, AsyncAPI, TypeScript, Python
  models, schema bundles, CLI references, and validation reports.
- Migration: explicit rewrite/report process for workspace or PrismSpec inputs.

Keep the kernel small. Add product-surface concepts through packs and tested
fixtures.

## Working Rules

- Keep the repository releasable after every sprint.
- Update tests, examples, docs, CI, and roadmap entries with behavior changes.
- Keep `README.md` aligned with `CHANGELOG.md`, `ROADMAP.md`, release notes,
  install instructions, release badges, version references, and other public
  bookkeeping.
- When the active roadmap is caught up, plan up to the next 20 roadmap points
  for fixing, improving, continuing, and expanding the project. Keep those
  points in `ROADMAP.md` as planning inputs until they are converted into
  GitHub issues and milestones.
- Follow the repository branching strategy in `docs/branching.md`; do feature
  and sprint work on branches, keep `main` releasable, and avoid direct pushes
  to `main` except for explicitly approved release or bookkeeping work.
- After each commit, refresh agent context by re-reading this file and checking
  the latest repository state before continuing work.
- At the entry point, determine whether commands should run under `zsh`,
  `bash`, or PowerShell, then keep command syntax consistent with that shell.
- Prefer small, executable increments over broad speculative architecture.
- Preserve the pack-based architecture: core stays small; product surfaces
  belong in packs.
- Keep engine-specific additions parity-aware: when adding a built-in Unity
  record kind, generator surface, readiness gate, or example capability, add
  equivalent Godot and Unreal coverage in the same related sprint where the
  concept applies. If an equivalent does not apply, document the reason in the
  issue, docs, and tests.
- New packs should include schemas, examples or fixtures, validation coverage,
  readiness gates where relevant, and docs.
- Installed extension packs should use the `verityspec.packs` Python
  entry-point group and must keep the entry-point name aligned with the pack
  manifest `id`.
- Do not remove or detach bundled specialized packs from the core package
  until `docs/specialized-pack-separation.md` gates are implemented, tested,
  documented, and covered by migration and rollback guidance.
- Do not commit secrets, tokens, PyPI credentials, or local environment files.
- Do not publish releases or PyPI packages unless the user explicitly asks.
- Preserve user changes. Do not revert unrelated dirty files.
- Use structured JSON parsing/writing for JSON artifacts.
- Keep documentation command examples executable from a clean checkout.
- If GitHub workflow checks cannot run or fail because of billing, credits,
  quota, runner availability, or another platform issue, verify the equivalent
  checks locally, record that CI was unavailable for external reasons, and
  continue work from the local evidence.
- During clean-on-main stopping points after merges or releases, scan open
  issues and attempt small, unblocked issues before starting unrelated roadmap
  expansion. Leave larger or blocked issues in the issue tracker with clear
  status instead of derailing the current release flow.

## Shell Discipline

At the start of work, determine the command shell before running repository
commands. Use the host OS, current shell, CI workflow shell, and command syntax
requirements to choose one of:

- `zsh`: normal local shell on macOS developer machines.
- `bash`: normal shell for GitHub Actions and portable Unix-like scripts.
- PowerShell: Windows or explicitly PowerShell-based automation.

Maintain that shell discipline until there is a concrete reason to switch. Do
not mix activation commands, environment-variable syntax, path separators, or
control-flow syntax across shells in the same command sequence.

When switching shells:

1. State why the switch is necessary.
2. Rewrite the full command for the new shell.
3. Re-check paths, quoting, virtualenv activation, and environment variables.

Shell-specific examples:

```bash
# zsh/bash
. .venv/bin/activate
PYTHONPATH=src python -m unittest discover -s tests -v
```

```powershell
# PowerShell
. .venv\Scripts\Activate.ps1
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

In GitHub Actions, prefer explicit `shell: bash` for multi-line Unix command
steps. Use PowerShell in workflows only when the job targets Windows or needs
PowerShell-specific behavior.

## Organization Research And Reuse

Before inventing or changing a reusable pattern, practice, term, workflow, schema convention, prompt convention, CI convention, evidence pattern, content model, legal/support workflow, release rule, or agent procedure, agents must consult the canonical organization repositories:

- `../organization-patterns` locally, or `Jason-Furr/organization-patterns` remotely
- `../organization-glossary` locally, or `Jason-Furr/organization-glossary` remotely

If the work produces a reusable pattern or practice, propose a follow-up update to `organization-patterns`. If the work introduces or changes terminology, propose a follow-up update to `organization-glossary`. Do not silently fork organization terms or practices inside this repository.

## Work Ledger And Content Opportunities

Agents must keep track of the active issue, branch, roadmap item, affected records, decisions, and verification while they work. When the work yields material suitable for public explanation, agents must propose an article or devlog candidate instead of directly publishing it.

Article candidates belong in `Jason-Furr/jasonfurr-articles`; devlog candidates belong in `Jason-Furr/jasonfurr-devlog`. The operator may approve, decline, or postpone the content, writing, and submission. Legal or policy content belongs in `Jason-Furr/jasonfurr-legal` and requires explicit approval.

## Required Operating Loop

AI agents must follow the same development, release, and project-management
loop that has been used successfully in this repository:

1. Start by reading this file, checking `git status --short --branch`, checking
   the latest commit, confirming the active shell, and identifying the active
   issue, milestone, branch, and roadmap section.
2. Convert substantive work into a public sprint, release, feature, fix, or
   docs branch with a GitHub issue and milestone before implementation when the
   work is not already tracked.
3. Keep work in small executable increments. Read the relevant files first,
   follow existing patterns, and avoid broad speculative rewrites.
4. Update behavior, tests, examples, docs, README, changelog, roadmap, release
   notes, workflow templates, and public version references together when they
   are part of the same change.
5. Keep the README release badge, latest-release text, install tag, workspace
   package-version text, release-notes link, downstream CI pins, and package
   version aligned during release prep.
6. Run focused checks first when useful, then the standard local checks. For
   release work, also build distributions, run `twine check`, and smoke-test
   the built wheel.
7. Commit only after local verification. After every commit, re-read this file,
   check `git status --short --branch`, and check the latest commit before
   continuing.
8. Push the branch, open a PR with a concise summary and the exact local
   verification performed, then watch GitHub Actions until checks pass or fail.
9. If GitHub Actions is unavailable because of billing, credits, quota, runner
   availability, or another platform reason, run and record equivalent local
   checks in the PR and continue from that evidence.
10. Merge only after checks pass or the local-verification fallback is recorded.
    After merge, verify local `main`, verify the `main` CI run, and confirm the
    issue and milestone state.
11. For authorized releases, use a release-prep branch and PR, merge to `main`,
    tag from `main`, watch the release workflow, verify the GitHub release and
    uploaded artifacts, and then close the milestone.
12. At clean-on-main moments after merge or release verification, scan open
    issues and handle small, unblocked issues when doing so keeps the
    repository releasable and does not interrupt a required release step.
13. When the active roadmap is caught up, keep the next-20 roadmap planning
    section populated with concrete future points for fixing, improving,
    continuing, and expanding the project.

## Standard Local Checks

Use these checks before committing meaningful changes:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools
pip install -e .

python -m unittest discover -s tests -v
verity pack validate
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
git diff --check
```

For generator, migration, external-pack, or release work, also run the relevant
CLI smoke checks from `README.md`, `docs/ci.md`, and `docs/release-checklist.md`.

## Common Commands

```bash
verity --version
verity init build/init-api --template api --owner platform --force
verity pack list
verity pack doctor
verity pack compare verity.pack.unity --mirror tests/fixtures/official_extension_mirrors/verityspec-pack-unity/pack
verity pack validate
verity pack init verity.pack.features --out build/packs/features --kind feature.flag --force
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity validate examples/security
verity lint examples/security --strict
verity readiness examples/security --strict
verity validate examples/observability
verity lint examples/observability --strict
verity readiness examples/observability --strict
verity validate examples/accessibility
verity lint examples/accessibility --strict
verity readiness examples/accessibility --strict
verity validate examples/compliance
verity lint examples/compliance --strict
verity readiness examples/compliance --strict
verity validate examples/deployment
verity lint examples/deployment --strict
verity readiness examples/deployment --strict
verity validate examples/game-core
verity lint examples/game-core --strict
verity readiness examples/game-core --strict
verity validate examples/game-assets
verity lint examples/game-assets --strict
verity readiness examples/game-assets --strict
verity validate examples/unity
verity lint examples/unity --strict
verity readiness examples/unity --strict
verity graph examples/unity
verity validate examples/godot
verity lint examples/godot --strict
verity readiness examples/godot --strict
verity graph examples/godot
verity validate examples/unreal
verity lint examples/unreal --strict
verity readiness examples/unreal --strict
verity graph examples/unreal
verity validate examples/gameplay
verity lint examples/gameplay --strict
verity readiness examples/gameplay --strict
verity validate examples/content
verity lint examples/content --strict
verity readiness examples/content --strict
verity validate examples/economy
verity lint examples/economy --strict
verity readiness examples/economy --strict
verity validate examples/progression
verity lint examples/progression --strict
verity readiness examples/progression --strict
verity graph examples/progression
verity validate examples/product-delivery
verity lint examples/product-delivery --strict
verity readiness examples/product-delivery --strict
verity graph examples/product-delivery
verity validate examples/lifecycle-readiness
verity lint examples/lifecycle-readiness --strict
verity readiness examples/lifecycle-readiness --strict
verity graph examples/lifecycle-readiness
verity validate examples/mobile
verity lint examples/mobile --strict
verity readiness examples/mobile --strict
verity graph examples/mobile
verity validate examples/liveops
verity lint examples/liveops --strict
verity readiness examples/liveops --strict
verity graph examples/liveops
verity validate examples/evidence
verity lint examples/evidence --strict
verity readiness examples/evidence --strict
verity graph examples/evidence
verity doctor examples/basic
verity doctor examples/basic --report-out build/doctor-report.json
verity explain reference.missing
verity graph examples/basic
verity diff examples/basic examples/basic --format json
verity migrate --list --format json
verity migrate examples/basic --dry-run --format json
verity generate openapi examples/basic --out build/openapi.json
verity generate asyncapi examples/basic --out build/asyncapi.json
verity generate typescript examples/basic --out build/types.ts
verity generate python-models examples/basic --out build/models.py
verity generate validation-report examples/basic --out build/validation-report.json
verity generate security-report examples/security --out build/security-report.json
verity generate security-report examples/security --format markdown --out build/security-report.md
verity generate observability-report examples/observability --out build/observability-report.json
verity generate accessibility-report examples/accessibility --out build/accessibility-report.json
verity generate compliance-matrix examples/compliance --out build/compliance-matrix.json
verity generate deployment-report examples/deployment --out build/deployment-report.json
verity generate deployment-report examples/deployment --format markdown --out build/deployment-report.md
verity generate schema-bundle examples/game-core --out build/game-core-schema-bundle.json
verity generate schema-bundle examples/game-assets --out build/game-assets-schema-bundle.json
verity generate schema-bundle examples/unity --out build/unity-schema-bundle.json
verity generate schema-bundle examples/godot --out build/godot-schema-bundle.json
verity generate schema-bundle examples/unreal --out build/unreal-schema-bundle.json
verity generate schema-bundle examples/gameplay --out build/gameplay-schema-bundle.json
verity generate schema-bundle examples/content --out build/content-schema-bundle.json
verity generate schema-bundle examples/economy --out build/economy-schema-bundle.json
verity generate schema-bundle examples/progression --out build/progression-schema-bundle.json
verity generate schema-bundle examples/product-delivery --out build/product-delivery-schema-bundle.json
verity generate lifecycle-readiness-report examples/lifecycle-readiness --out build/lifecycle-readiness-report.json
verity generate schema-bundle examples/mobile --out build/mobile-schema-bundle.json
verity generate schema-bundle examples/liveops --out build/liveops-schema-bundle.json
verity generate schema-bundle examples/evidence --out build/evidence-schema-bundle.json
verity generate evidence-report examples/evidence --out build/evidence-report.json
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --out build/coverage-dashboard.json
verity generate pack-capability-index tests/fixtures/custom_pack_workspace --out build/pack-capability-index.json
verity generate product-impact tests/fixtures/product_impact/baseline tests/fixtures/product_impact/current --out build/product-impact.json
verity generate schema-bundle examples/accessibility --out build/accessibility-schema-bundle.json
verity generate schema-bundle examples/compliance --out build/compliance-schema-bundle.json
verity generate schema-bundle examples/deployment --out build/deployment-schema-bundle.json
verity generate decision-index examples/product-delivery --out build/decision-index.json
verity generate decision-index examples/product-delivery --format markdown --out build/decision-index.md
```

External pack checks:

```bash
verity pack validate verity.pack.features --path tests/fixtures/custom_pack
verity pack doctor --path tests/fixtures/custom_pack --format json
verity pack validate verity.pack.features --path docs/fixtures/pack-scaffold/packs/features
verity validate tests/fixtures/custom_pack_workspace
verity lint tests/fixtures/custom_pack_workspace --strict
verity readiness tests/fixtures/custom_pack_workspace --strict
verity validate docs/fixtures/pack-scaffold/workspace
verity lint docs/fixtures/pack-scaffold/workspace --strict
verity readiness docs/fixtures/pack-scaffold/workspace --strict
verity generate schema-bundle docs/fixtures/pack-scaffold/workspace --out build/pack-scaffold-schema-bundle.json
verity generate pack-capability-index docs/fixtures/pack-scaffold/workspace --out build/pack-scaffold-capability-index.json
```

Generator maturity checks:

```bash
verity validate tests/fixtures/generator_maturity
verity generate typescript tests/fixtures/generator_maturity --out build/generator-maturity.ts
verity generate python-models tests/fixtures/generator_maturity --out build/generator-maturity.py
```

## Important Files

- `README.md`: public overview and quick start.
- `ROADMAP.md`: canonical sprint roadmap.
- `CHANGELOG.md`: release-facing change log.
- `src/verityspec/cli.py`: CLI contract and command wiring.
- `src/verityspec/validation.py`: structural and semantic validation.
- `src/verityspec/packs.py`: pack registry and loading.
- `src/verityspec/generators.py`: generated artifacts.
- `docs/security-pack.md`: built-in security pack and security report behavior.
- `docs/accessibility-pack.md`: built-in accessibility pack behavior.
- `docs/compliance-pack.md`: built-in compliance pack behavior.
- `docs/game-core-pack.md`: built-in game-core pack behavior.
- `docs/game-assets-pack.md`: built-in game-assets pack behavior.
- `docs/unity-pack.md`: built-in Unity pack behavior.
- `docs/godot-pack.md`: built-in Godot pack behavior.
- `docs/unreal-pack.md`: built-in Unreal pack behavior.
- `docs/gameplay-pack.md`: built-in gameplay pack behavior.
- `docs/content-pack.md`: built-in content pack behavior.
- `docs/economy-pack.md`: built-in economy pack behavior.
- `docs/progression-pack.md`: built-in progression pack behavior.
- `docs/product-delivery-pack.md`: built-in product-delivery pack behavior.
- `docs/mobile-pack.md`: built-in mobile lifecycle pack behavior.
- `docs/liveops-pack.md`: built-in live operations pack behavior.
- `docs/evidence-pack.md`: built-in evidence pack behavior.
- `tests/`: executable behavior coverage.
- `.github/workflows/ci.yml`: required CI contract.
- `.github/workflows/release.yml`: release automation.
- `.github/workflows/product-contract.yml`: reusable downstream product-contract
  workflow.
- `templates/github-actions/`: maintained downstream workflow templates,
  including direct, reusable, local-pack, and monorepo examples.

## Sprint Discipline

The project is managed in public sprints through GitHub issues and milestones.
Plan sprints as cohesive bundles of related work sized up to roughly two weeks
of development effort instead of many tiny release slices. Sprint
implementation work should happen on
`sprint/<number>-<topic>` branches and merge back to `main` only after local
checks and, when available, GitHub Actions checks pass.

When completing sprint work:

1. Keep `ROADMAP.md` current.
2. Keep the relevant GitHub issue and milestone state current.
3. Add or update tests for every new behavior.
4. Run local checks.
5. Commit on the appropriate sprint or feature branch.
6. Refresh agent context from `AGENTS.md`, `git status`, and the latest commit.
7. Push the branch and verify GitHub Actions passes, or document the local verification if
   GitHub Actions is unavailable for external platform reasons.
8. Merge to `main` using the approved repository flow, then verify `main`.

## Testing Expectations

- CLI behavior belongs in subprocess tests in `tests/test_cli.py`.
- Library behavior belongs in `tests/test_verityspec.py`.
- Example workspace behavior belongs in `tests/test_examples.py`.
- Positive examples should validate, lint, and pass readiness.
- Broken examples should fail with stable issue codes.
- Generator output that should remain stable should use golden fixtures.
- External pack behavior should cover both workspace `packPaths` and CLI
  `--pack-path`.

## Documentation Expectations

Update the closest documentation file with behavior changes:

- CLI usage: `README.md`
- Roadmap/sprints: `ROADMAP.md`
- CI adoption: `docs/ci.md` and `docs/downstream-ci.md`
- Packs: `docs/packs.md`
- Generators: `docs/generators.md`
- Workspace format: `docs/workspace-format.md`
- Branching and merge flow: `docs/branching.md`
- Releases: `CHANGELOG.md`, `docs/release-checklist.md`, release notes docs
- AI-agent guidance: `AGENTS.md`

For public-facing changes, also review `README.md` in the same change. The
README should not lag the changelog, roadmap, release status, install tags,
package version, supported workspace format, or active sprint direction.

## Release Rules

- Version lives in both `pyproject.toml` and `src/verityspec/__init__.py`.
- Release tags use `vMAJOR.MINOR.PATCH`.
- The workspace format version is separate from the package version.
- PyPI trusted publishing requires PyPI-side setup; do not assume it is ready.
- Do not create tags, GitHub releases, or PyPI publishes without explicit user
  direction.

## Agent Adapter Policy

Agent-specific files such as `CLAUDE.md`, `GEMINI.md`, `CODEX.md`,
`CHATGPT.md`, `UNITY_AI.md`, and `.github/copilot-instructions.md` should remain
thin pointers to this file. Do not put independent project instructions in those
files.
