# VeritySpec v0.9.0 Release Notes

VeritySpec v0.9.0 adds the first compliance product surface and makes
compliance mappings reportable through an executable matrix generator.

## Highlights

- Added built-in `verity.pack.compliance`.
- Added strict `compliance.mapping` records for framework requirement mappings.
- Kept compliance records evidence-oriented by requiring `attestation: false`
  and avoiding legal, regulatory, audit, or certification claims.
- Added compliance readiness gates, reviewed-mapping policy, and reference
  rules.
- Added executable `examples/compliance` that connects compliance mappings to
  security, accessibility, and observability evidence.
- Added `verity generate compliance-matrix` for mapping, framework,
  requirement, verification, evidence, target, and release-gap summaries.
- Kept the next-20 roadmap planning backlog populated after completing the
  compliance work.

## Compatibility

- Package version: `0.9.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.9.0"
verity --version
```

PyPI publishing remains prepared but requires PyPI-side trusted publishing
setup before enabling `publish_pypi=true`.
