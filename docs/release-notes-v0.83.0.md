# VeritySpec v0.83.0 Release Notes

VeritySpec v0.83.0 adds Markdown output for evidence reports so implementation
and release reviewers can inspect evidence coverage, release gaps, subject
links, artifact URIs, references, and per-evidence status without opening JSON.

## Highlights

- Added `--format markdown` support for `verity generate evidence-report`.
- Preserved the existing JSON evidence-report output as the default
  machine-readable contract for CI and downstream tooling.
- Added a stable Markdown evidence report with workspace metadata, summary
  counts, kind, lifecycle status, evidence status, owner breakdowns, release
  gaps, subject resolution, URI fields, and reference detail.
- Updated `verity.pack.evidence` generator metadata to advertise JSON and
  Markdown output.
- Added CLI, library, golden-fixture, empty-section, pack-metadata, CI smoke,
  fixture-refresh, release-checklist, README, changelog, and roadmap coverage.
- Preserved the boundary that Markdown reports summarize declared VeritySpec
  evidence records and linked subjects; they do not prove external legal,
  commercial, privacy-law, marketplace, app-store, platform-certification,
  pricing-approval, support-SLA, or production-readiness approval.

## Install

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.83.0"
```

PyPI trusted publishing remains prepared but not enabled for this release.

## Verification

Local release verification included:

```bash
PYTHONPATH=src python3 -m unittest tests.test_cli.VerityCliTests.test_evidence_report_generator_writes_report tests.test_cli.VerityCliTests.test_evidence_report_generator_writes_markdown_report tests.test_cli.VerityCliTests.test_evidence_report_generator_matches_golden_file tests.test_cli.VerityCliTests.test_markdown_format_is_limited_to_supported_report_artifacts tests.test_verityspec.VeritySpecTests.test_evidence_report_matches_golden_file tests.test_verityspec.VeritySpecTests.test_evidence_report_markdown_matches_golden_file tests.test_verityspec.VeritySpecTests.test_evidence_report_markdown_handles_empty_sections tests.test_verityspec.VeritySpecTests.test_evidence_report_generator_is_advertised_by_evidence_pack tests.test_verityspec.VeritySpecTests.test_roadmap_report_markdown_summarizes_release_governance tests.test_fixture_refresh_doc tests.test_readme_commands -v
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m verityspec pack validate
PYTHONPATH=src python3 -m verityspec validate examples/basic
PYTHONPATH=src python3 -m verityspec lint examples/basic --strict
PYTHONPATH=src python3 -m verityspec readiness examples/basic --strict
PYTHONPATH=src python3 -m verityspec validate examples/evidence
PYTHONPATH=src python3 -m verityspec lint examples/evidence --strict
PYTHONPATH=src python3 -m verityspec readiness examples/evidence --strict
PYTHONPATH=src python3 -m verityspec generate evidence-report examples/evidence --format markdown --out build/evidence-report.md
git diff --check
python -m build
python -m twine check dist/*
```

The release branch also smoke-tested the built wheel before tagging.
