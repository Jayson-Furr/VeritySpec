# VeritySpec v0.32.0 Release Notes

VeritySpec v0.32.0 adds a pack capability index report for reviewing the
schemas, readiness gates, reference rules, and generator metadata loaded from
built-in and external packs.

## Highlights

- Added `verity generate pack-capability-index`.
- Summarized loaded pack IDs, local `packPaths`, built-in pack count, external
  pack count, schema count, readiness gate count, conditional readiness rule
  count, reference rule count, and generator declaration count.
- Added per-pack details for source type, path, schemas, readiness gates,
  reference rules, and normalized generator metadata.
- Added a deduplicated generator capability index across packs.
- Added core pack generator metadata for `pack-capability-index`.
- Added external-pack coverage for both workspace `packPaths` and CLI
  `--pack-path`.
- Added committed golden output for the pack capability index JSON contract.
- Updated README, generator docs, pack docs, CI docs, release checklist,
  changelog, roadmap, workflow smoke checks, and AI-agent command guidance.

## Compatibility

- Package version: `0.32.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace schema or workspace format behavior changed in this release.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.32.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
