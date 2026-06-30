# VeritySpec v0.26.0 Release Notes

VeritySpec v0.26.0 adds product-surface pack boundary guidance for future GUI,
desktop, mobile, and game packs before their first schemas are introduced.

## Highlights

- Added a public design note for future GUI, desktop, mobile, and game pack
  boundaries.
- Clarified what belongs in product-surface packs versus cross-cutting packs
  such as security, accessibility, observability, compliance, release,
  evidence, deployment, dependency, and portfolio packs.
- Documented first-schema gates that future product-surface packs should meet
  before adding schemas.
- Linked the boundary guidance from README and pack documentation.
- Added documentation contract tests that keep the boundary note discoverable
  and preserve its core commitments.
- Updated README, changelog, roadmap, downstream workflow pins, PyPI fallback
  docs, release checklist, and release bookkeeping for `v0.26.0`.

## Compatibility

- Package version: `0.26.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.26.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
