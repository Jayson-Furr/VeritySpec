# AI Agent Entry Point

This is the canonical instruction file for AI agents working in this
repository. Agent-specific files are adapters only; if they conflict with this
file, `AGENTS.md` wins.

This entry point is intended for Codex, GitHub Copilot, Claude, Claude Code,
ChatGPT, Gemini, Unity AI, and other coding agents.

## Project Identity

VeritySpec is an executable product-contract framework. It is not a static
schema catalog.

The core promise is:

> Executable product contracts for humans, tools, and agents.

Treat PrismSpec only as historical input for the importer. Do not expand
VeritySpec by recreating a broad static PrismSpec-style catalog.

## Architecture Summary

The repository is a Python package with a CLI named `verity`.

Core concepts:

- Workspace: directory with `verityspec.json` and record files.
- Pack: extension unit that contributes schemas, readiness gates, reference
  rules, and generator support.
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
  install instructions, version references, and other public bookkeeping.
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
- New packs should include schemas, examples or fixtures, validation coverage,
  readiness gates where relevant, and docs.
- Do not commit secrets, tokens, PyPI credentials, or local environment files.
- Do not publish releases or PyPI packages unless the user explicitly asks.
- Preserve user changes. Do not revert unrelated dirty files.
- Use structured JSON parsing/writing for JSON artifacts.
- Keep documentation command examples executable from a clean checkout.
- If GitHub workflow checks cannot run or fail because of billing, credits,
  quota, runner availability, or another platform issue, verify the equivalent
  checks locally, record that CI was unavailable for external reasons, and
  continue work from the local evidence.

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
verity pack validate
verity pack init verity.pack.features --out build/packs/features --kind feature.flag --force
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity validate examples/security
verity lint examples/security --strict
verity readiness examples/security --strict
verity doctor examples/basic
verity doctor examples/basic --report-out build/doctor-report.json
verity explain reference.missing
verity graph examples/basic
verity migrate --list --format json
verity migrate examples/basic --dry-run --format json
verity generate openapi examples/basic --out build/openapi.json
verity generate asyncapi examples/basic --out build/asyncapi.json
verity generate typescript examples/basic --out build/types.ts
verity generate python-models examples/basic --out build/models.py
verity generate validation-report examples/basic --out build/validation-report.json
verity generate security-report examples/security --out build/security-report.json
```

External pack checks:

```bash
verity pack validate verity.pack.features --path tests/fixtures/custom_pack
verity validate tests/fixtures/custom_pack_workspace
verity lint tests/fixtures/custom_pack_workspace --strict
verity readiness tests/fixtures/custom_pack_workspace --strict
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
- `tests/`: executable behavior coverage.
- `.github/workflows/ci.yml`: required CI contract.
- `.github/workflows/release.yml`: release automation.
- `.github/workflows/product-contract.yml`: reusable downstream product-contract
  workflow.

## Sprint Discipline

The project is managed in public sprints through GitHub issues and milestones.
Sprint implementation work should happen on `sprint/<number>-<topic>` branches
and merge back to `main` only after local checks and, when available, GitHub
Actions checks pass.

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
