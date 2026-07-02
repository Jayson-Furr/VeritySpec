# VeritySpec v0.70.0 Release Notes

VeritySpec v0.70.0 adds Markdown output for security reports so release
reviewers can inspect security-control coverage and release gaps without
opening JSON, while preserving the existing machine-readable security-report
contract.

## Highlights

- Added `verity generate security-report --format markdown`.
- Preserved the existing JSON `security-report` output as the CI and
  downstream tooling contract.
- Rendered security report metadata, summary counts, coverage counts, risk
  counts, release gaps, per-control verification details, and target records
  in stable Markdown.
- Kept stale evidence, missing verification dates, and critical unverified
  controls visible in the Markdown release-gap table.
- Added committed Markdown golden fixture coverage for the security report.
- Added CLI and library tests for security-report Markdown generation.
- Updated `verity.pack.security` generator metadata to advertise JSON and
  Markdown output formats.
- Updated README, generator docs, security-pack docs, CI guidance, release
  checklist, fixture-refresh docs, workflow generator checks, and agent command
  references.
- Added canonical AI-agent feedback-loop guidance for filing VeritySpec issues
  when agents discover reusable bugs, gaps, or workflow friction.
- Added clean-on-main open-issue sweep guidance so agents scan and attempt
  small unblocked issues before starting unrelated roadmap expansion.
- Rotated the next-20 roadmap queue after converting security-report Markdown
  output into sprint 147.

The Markdown report is a derived internal release-review artifact. It does not
make legal, compliance, privacy-law, security-certification, penetration-test,
marketplace, app-store, platform-certification, pricing-approval, support-SLA,
or production-readiness claims.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.70.0"
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
verity validate examples/security
verity lint examples/security --strict
verity readiness examples/security --strict
verity generate security-report examples/security --out build/security-report.json
verity generate security-report examples/security --format markdown --out build/security-report.md
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release. After the tag
workflow completes, use the post-tag release verification checklist to record
release asset hashes, skipped PyPI state, downloaded wheel smoke results,
public GitHub tag install results, closed issue and milestone evidence, and
agent context refresh evidence.
