# VeritySpec v0.81.0 Release Notes

VeritySpec v0.81.0 adds downstream CI profile artifact guidance so adopting
repositories can preserve the machine-readable evidence behind release,
regulated, public API, and internal-tool product-contract checks.

## Highlights

- Added `docs/downstream-ci-profile-artifacts.md` for preserving profile
  artifact bundles without changing reusable workflow or CLI behavior.
- Defined common artifact bundle contents for validation, lint, readiness,
  doctor, graph, and validation-report outputs.
- Added profile-specific report guidance for release, regulated, public API,
  and internal-tool workflows.
- Included a GitHub Actions `upload-artifact` example with stable artifact
  names, run-attempt metadata, retention guidance, and `if: always()`.
- Documented redaction, path, retention, and privacy boundaries for downstream
  CI artifacts.
- Recorded local verification fallback guidance for GitHub Actions billing,
  credit, quota, runner, or platform outages.
- Linked the guidance from README, downstream CI docs, and product-contract
  profile docs.
- Added documentation tests and rotated the Next 20 roadmap queue after
  converting downstream CI profile artifact guidance into Sprint 158.

## Install

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.81.0"
```

PyPI trusted publishing remains prepared but not enabled for this release.

## Verification

Local release verification included:

```bash
PYTHONPATH=src python3 -m unittest tests.test_downstream_ci_profile_artifacts_doc tests.test_downstream_templates -v
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
