# VeritySpec v0.72.0 Release Notes

VeritySpec v0.72.0 documents the workspace migration-report JSON contract for
CI integrations and release-review tooling.

## Highlights

- Added `docs/schemas/migration-report.schema.json`, a machine-readable JSON
  Schema for reports emitted by `verity migrate --format json` and
  `verity migrate --report-out`.
- Added [Migration Report JSON Schema](migration-report-schema.md), covering
  report identity, stable fields, impact summaries, migration path steps,
  change records, blocked reports, and additive compatibility policy.
- Documented that blocked migration reports return a non-zero CLI exit code
  while still emitting schema-valid JSON.
- Linked the schema from README, CI guidance, workspace-format docs, and
  versioning/migration docs.
- Added executable tests that validate current successful, dry-run,
  report-out, unsupported-target blocked, future-version blocked, and no-path
  blocked migration reports against the schema.
- Rotated the Next 20 roadmap queue after converting migration-report schema
  documentation into Sprint 149.
- Aligned `AGENTS.md` with the organization-wide AI entry-point baseline so
  all agents in VeritySpec preserve the same shell, context-refresh,
  organization-pattern, glossary, work-ledger, and approval-gate discipline.

This release documents the existing workspace migration-report contract. It
does not introduce a new workspace format version, a migration-report generator
command, runtime schema enforcement for users, or a PrismSpec importer report
schema.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.72.0"
verity --version
```

PyPI publishing is prepared but not enabled yet. GitHub release installation
remains the canonical public install path for this release.

## Verification

Release verification should include:

```bash
python -m unittest tests.test_migration_report_schema_doc -v
python -m unittest discover -s tests -v
verity pack validate
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity migrate tests/fixtures/migration/legacy_workspace --dry-run --format json
verity validate examples/unity
verity lint examples/unity --strict
verity readiness examples/unity --strict
verity validate examples/godot
verity lint examples/godot --strict
verity readiness examples/godot --strict
verity validate examples/unreal
verity lint examples/unreal --strict
verity readiness examples/unreal --strict
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release. After the tag
workflow completes, use the post-tag release verification checklist to record
release asset hashes, skipped PyPI state, downloaded wheel smoke results,
public GitHub tag install results, closed issue and milestone evidence, and
agent context refresh evidence.
