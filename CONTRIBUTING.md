# Contributing to VeritySpec

VeritySpec grows through small, executable product-contract increments. Public
contributions should preserve the core direction:

- Keep the core kernel small.
- Add product-surface concepts through packs.
- Prefer validated examples, tests, readiness gates, and generators over broad
  static schema catalogs.
- Keep README, changelog, roadmap, docs, examples, and tests aligned with
  behavior changes.

## Contribution Flow

1. Open an issue before large work. Use the pack proposal or schema change
   template when the change affects product-contract vocabulary.
2. Keep the proposal concrete: describe the product problem, affected record
   kinds, reference relationships, readiness behavior, examples, and expected
   generated outputs.
3. Work on a branch that follows `docs/branching.md`.
4. Add tests and executable examples for behavior changes.
5. Run local checks before opening a pull request.
6. Include the commands you ran in the pull request verification section.

Small typo fixes and narrow documentation corrections can go straight to a pull
request. New packs, new record kinds, breaking schema changes, generator
changes, and readiness policy changes should start with an issue.

Maintainers should review public external pack proposals with the
[External pack maintainer review checklist](docs/external-pack-review-checklist.md).

## Proposing a New Pack

Use the `Pack proposal` issue template for new packs.

A pack proposal should define:

- Product surface and user problem.
- Pack ID, such as `verity.pack.game-core`.
- Initial record kinds and why each belongs in the pack.
- Required record envelope fields and pack-specific required fields.
- Reference rules introduced by the pack.
- Readiness gates or conditional readiness rules.
- Generator, report, or useful artifact planned for the pack.
- Example workspace or fixture that proves the pack is executable.
- Compatibility expectations and likely future expansion boundaries.

Every accepted pack should include:

- A valid `pack.json` manifest.
- Strict JSON Schemas for each record kind.
- Tests for validation, linting, readiness, and generators where relevant.
- At least one executable example or fixture.
- Documentation in the closest pack doc.
- README and roadmap updates when the change is public-facing.

Do not add a large family of skeletal schemas without executable behavior.
The maintainer checklist defines the acceptance gates for identity, contract,
executability, documentation, compatibility, and PR review.

## Proposing a Schema Change

Use the `Schema change` issue template for new record fields, required-field
changes, enum changes, reference-shape changes, and schema removals.

A schema change proposal should define:

- Affected pack ID and record kind.
- Whether the change is additive, behavioral, deprecated, or breaking.
- Migration impact for existing workspaces.
- Validation, lint, readiness, graph, generator, and documentation impact.
- Example records before and after the change.
- Tests and fixtures that will prove the new contract.

Prefer additive schema changes. Breaking changes need a migration story,
release-note coverage, and compatibility tests when the workspace format or
existing examples are affected.

## Local Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools
pip install -e .
```

## Local Checks

Use the standard checks from `AGENTS.md` before opening a pull request:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m verityspec pack validate
PYTHONPATH=src python3 -m verityspec validate examples/basic
PYTHONPATH=src python3 -m verityspec lint examples/basic --strict
PYTHONPATH=src python3 -m verityspec readiness examples/basic --strict
git diff --check
```

For pack, generator, migration, or release changes, also run the relevant
checks listed in `AGENTS.md`, `docs/ci.md`, and `docs/release-checklist.md`.

## Pull Request Expectations

Pull requests should include:

- Summary of the product-contract behavior changed.
- Issue or milestone link when applicable.
- Local verification commands and results.
- README, changelog, roadmap, docs, examples, and test updates when relevant.
- Notes about compatibility, migration, deprecation, or breaking behavior.

If GitHub Actions is unavailable because of billing, credits, quota, runner
availability, or another platform reason, run equivalent local checks and
record that in the pull request.
