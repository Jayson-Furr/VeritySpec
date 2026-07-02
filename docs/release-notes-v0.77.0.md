# VeritySpec v0.77.0 Release Notes

VeritySpec v0.77.0 adds downstream AI-adapter drift-check guidance for sibling
repositories that keep agent-specific adapter files.

## Highlights

- Added [downstream AI adapter drift checks](downstream-ai-adapter-drift.md).
- Anchored downstream adapter guidance to
  `organization-patterns/patterns/ai-entry-point-baseline.md`.
- Documented how Codex, Claude, ChatGPT, Gemini, Unity AI, GitHub Copilot, and
  similar adapter files should remain thin pointers to `AGENTS.md`.
- Added a practical drift checklist for sibling repositories covering paired
  entry-point reads, shell discipline, post-commit refresh,
  `organization-patterns`, `organization-glossary`, clean-main issue sweeps,
  explicit approval gates, and adapter-file boundaries.
- Added optional `rg` review commands for spotting independent commands or
  policy in adapter files.
- Expanded agent-governance documentation tests to cover the new guide and the
  current adapter inventory, including Unity AI and GitHub Copilot.
- Rotated the Next 20 roadmap queue after converting the adapter guidance item
  into Sprint 154.
- Updated README, changelog, roadmap, release checklist surfaces, downstream
  workflow pins, release-integrity fixtures, and release notes.

This release does not change repository operating authority. `AGENTS.md`
remains the canonical repository entry point, the organization pattern remains
the reusable baseline, and adapter files must not define independent branch,
test, release, product, legal, support, publishing, deployment, package, or
store-submission policy.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.77.0"
verity --version
```

PyPI publishing is prepared but not enabled yet. GitHub release installation
remains the canonical public install path for this release.

## Verification

Release verification should include:

```bash
python -m unittest discover -s tests -v
verity pack validate
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity generate roadmap-report . --format markdown --out build/roadmap-report.md
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release. After the tag
workflow completes, use the post-tag release verification checklist to record
release asset hashes, skipped PyPI state, downloaded wheel smoke results,
public GitHub tag install results, closed issue and milestone evidence, and
agent context refresh evidence.
