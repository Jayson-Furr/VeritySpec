# VeritySpec v0.30.0 Release Notes

VeritySpec v0.30.0 adds product-impact reports for release-review graph
analysis across two workspace snapshots.

## Highlights

- Added `verity generate product-impact OLD NEW`.
- Added baseline/current workspace comparison using the existing
  `verity diff` classification model.
- Added changed-record expansion through upstream dependents and downstream
  dependencies in the workspace reference graph.
- Added missing-reference reporting for baseline and current graph edges.
- Added release-review summary fields for changed records, impacted records,
  severity counts, risk level, and review focus.
- Added deterministic baseline/current fixtures and committed golden output
  for the product-impact JSON contract.
- Updated CI, release checklist, generator docs, pack docs, CI docs, README,
  changelog, roadmap, and AI-agent command guidance.

## Compatibility

- Package version: `0.30.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.30.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
