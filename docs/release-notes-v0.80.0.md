# VeritySpec v0.80.0 Release Notes

VeritySpec v0.80.0 adds golden-fixture refresh automation planning before any
fixture rewrite command ships.

## Highlights

- Added `docs/golden-fixture-refresh-automation-plan.md` to define the safety
  contract for future fixture refresh automation.
- Defined the planned `golden_fixture_refresh_plan` JSON shape with dry-run
  mode, generator allowlists, generated outputs, fixture comparisons,
  placeholder preservation, diff summaries, approval gates, blocked rewrites,
  and claim boundaries.
- Documented the future `verity fixtures refresh --dry-run` command shape
  without adding runtime behavior in this release.
- Anchored the plan to the fixture refresh guide, generator contracts,
  release-integrity checks, release-review workflow, and golden tests.
- Listed planned fixture families for basic dry runs, placeholder preservation,
  blocked rewrites, and explicit allowlists.
- Preserved the boundary that fixture refresh automation reviews generated
  output drift and does not prove commercial, legal, privacy-law, marketplace,
  platform-certification, app-store, pricing-approval, support-SLA,
  security-certification, or production-readiness guarantees.
- Linked the plan from README and the fixture refresh guide.
- Added documentation tests and rotated the Next 20 roadmap queue after
  converting golden-fixture refresh automation planning into Sprint 157.

## Install

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.80.0"
```

PyPI trusted publishing remains prepared but not enabled for this release.

## Verification

Local release verification included:

```bash
PYTHONPATH=src python3 -m unittest tests.test_golden_fixture_refresh_automation_plan_doc tests.test_fixture_refresh_doc -v
PYTHONPATH=src python3 -m unittest tests.test_verityspec -k roadmap_report -v
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m verityspec pack validate
PYTHONPATH=src python3 -m verityspec validate examples/basic
PYTHONPATH=src python3 -m verityspec lint examples/basic --strict
PYTHONPATH=src python3 -m verityspec readiness examples/basic --strict
PYTHONPATH=src python3 -m verityspec generate roadmap-report . --format markdown --out build/roadmap-report.md
git diff --check
python -m build
python -m twine check dist/*
```

The release branch also smoke-tested the built wheel before tagging.
