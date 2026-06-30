## Summary

Describe what changed and why.

## Issue or Milestone

Link the related issue, sprint, or milestone when applicable.

## Compatibility

Note any schema, workspace format, migration, readiness, generator, or
downstream CI impact.

## Verification

- [ ] `PYTHONPATH=src python3 -m unittest discover -s tests -v`
- [ ] `PYTHONPATH=src python3 -m verityspec validate examples/basic`
- [ ] `PYTHONPATH=src python3 -m verityspec lint examples/basic --strict`
- [ ] `PYTHONPATH=src python3 -m verityspec readiness examples/basic --strict`

## Bookkeeping

- [ ] README, changelog, roadmap, docs, and examples are updated when relevant.
- [ ] Pack or schema changes follow `CONTRIBUTING.md`.
