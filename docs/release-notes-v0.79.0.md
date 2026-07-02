# VeritySpec v0.79.0 Release Notes

VeritySpec v0.79.0 adds portfolio report JSON contract planning for a future
aggregate portfolio-report generator.

## Highlights

- Added `docs/portfolio-report-json-contract-plan.md` to define the planned
  `portfolio_report` JSON shape before runtime behavior ships.
- Anchored the plan to existing portfolio validation, product-impact,
  evidence-report, lifecycle-readiness, and agent-context boundaries.
- Defined planned report sections for portfolio identity, workspace inventory,
  validation, lint, readiness, graph status, relationships, impact warnings,
  evidence gaps, generated-artifact refresh needs, agent-context refresh needs,
  follow-up recommendations, and claim boundaries.
- Documented planned fixture families for basic, engine-portfolio,
  evidence-gap, and agent-context-refresh portfolio scenarios.
- Preserved the boundary that portfolio reporting summarizes declared
  product-contract posture and does not prove commercial, legal, privacy-law,
  marketplace, platform-certification, app-store, store-review,
  pricing-approval, support-SLA, security-certification, or
  production-readiness guarantees.
- Linked the plan from README and the portfolio validation foundation.
- Added documentation tests and rotated the Next 20 roadmap queue after
  converting portfolio report JSON contract planning into Sprint 156.

## Install

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.79.0"
```

PyPI trusted publishing remains prepared but not enabled for this release.

## Verification

Local release verification included:

```bash
PYTHONPATH=src python3 -m unittest tests.test_portfolio_report_json_contract_plan_doc tests.test_portfolio_validation_doc tests.test_lifecycle_fixture_plan_doc -v
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
