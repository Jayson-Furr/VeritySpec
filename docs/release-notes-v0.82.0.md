# VeritySpec v0.82.0 Release Notes

VeritySpec v0.82.0 adds Markdown output for deployment reports so release and
operations reviewers can inspect deployment targets, runtimes, release gaps,
release policies, linked controls, observability dashboards, compliance
mappings, and release evidence without opening JSON.

## Highlights

- Added `--format markdown` support for `verity generate deployment-report`.
- Preserved the existing JSON deployment-report output as the default
  machine-readable contract for CI and downstream tooling.
- Added a stable Markdown deployment report with workspace metadata, summary
  counts, environment/provider/platform breakdowns, runtime type counts,
  release gaps, deployment target detail, runtime detail, release policy
  summaries, and linked release evidence.
- Updated `verity.pack.deployment` generator metadata to advertise JSON and
  Markdown output.
- Added CLI, library, golden-fixture, empty-section, pack-metadata, CI smoke,
  fixture-refresh, release-checklist, README, changelog, and roadmap coverage.
- Preserved the boundary that Markdown reports summarize declared VeritySpec
  deployment records and linked evidence; they do not prove external legal,
  commercial, privacy-law, marketplace, app-store, platform-certification,
  pricing-approval, support-SLA, or production-readiness approval.

## Install

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.82.0"
```

PyPI trusted publishing remains prepared but not enabled for this release.

## Verification

Local release verification included:

```bash
PYTHONPATH=src python3 -m unittest tests.test_cli.VerityCliTests.test_deployment_report_generator_writes_report tests.test_cli.VerityCliTests.test_deployment_report_generator_writes_markdown_report tests.test_cli.VerityCliTests.test_deployment_report_generator_matches_golden_file tests.test_cli.VerityCliTests.test_markdown_format_is_limited_to_supported_report_artifacts tests.test_verityspec.VeritySpecTests.test_deployment_report_generator_is_advertised_by_deployment_pack tests.test_verityspec.VeritySpecTests.test_deployment_report_markdown_matches_golden_file tests.test_verityspec.VeritySpecTests.test_deployment_report_markdown_handles_empty_sections tests.test_verityspec.VeritySpecTests.test_roadmap_report_markdown_summarizes_release_governance -v
PYTHONPATH=src python3 -m unittest tests.test_fixture_refresh_doc tests.test_readme_commands tests.test_downstream_ci_profile_artifacts_doc -v
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m verityspec pack validate
PYTHONPATH=src python3 -m verityspec validate examples/basic
PYTHONPATH=src python3 -m verityspec lint examples/basic --strict
PYTHONPATH=src python3 -m verityspec readiness examples/basic --strict
PYTHONPATH=src python3 -m verityspec validate examples/deployment
PYTHONPATH=src python3 -m verityspec lint examples/deployment --strict
PYTHONPATH=src python3 -m verityspec readiness examples/deployment --strict
PYTHONPATH=src python3 -m verityspec generate deployment-report examples/deployment --format markdown --out build/deployment-report.md
git diff --check
python -m build
python -m twine check dist/*
```

The release branch also smoke-tested the built wheel before tagging.
