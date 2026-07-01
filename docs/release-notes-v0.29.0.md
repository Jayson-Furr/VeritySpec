# VeritySpec v0.29.0 Release Notes

VeritySpec v0.29.0 adds cross-pack coverage dashboards for product-surface
release review.

## Highlights

- Added `verity generate coverage-dashboard`.
- Added coverage summaries for API, CLI, events, security, accessibility,
  observability, compliance, and deployment records.
- Added product-level surface reference coverage for `exposes`, `ships`,
  `emits`, `securedBy`, `accessibilityCoveredBy`, `observes`,
  `complianceMappedBy`, and `deploysTo`.
- Added release-gap summaries for missing surface records, loaded surface
  packs without records, products without surface references, and
  product-specific missing surface references.
- Added a strict cross-pack fixture that validates every current built-in
  product surface together.
- Added committed golden output for the coverage-dashboard JSON contract.
- Updated CI, release checklist, generator docs, pack docs, README, changelog,
  roadmap, and AI-agent command guidance.

## Compatibility

- Package version: `0.29.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.29.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
