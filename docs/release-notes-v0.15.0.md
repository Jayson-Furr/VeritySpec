# VeritySpec v0.15.0 Release Notes

VeritySpec v0.15.0 adds golden security-report fixture coverage so the
security report output shape is stable, reviewable, and protected by direct
generator and CLI tests.

## Highlights

- Added a committed golden fixture for the `examples/security`
  `security-report` generator output.
- Added direct generator coverage that compares normalized report output to the
  golden fixture.
- Added CLI generator coverage that compares normalized report output to the
  golden fixture.
- Normalized only dynamic fields in snapshot tests: generation timestamp,
  absolute workspace path, and package version.
- Documented security-report golden coverage in generator and security-pack
  docs.
- Documented the required AI operating loop for sprint work, release prep,
  PR verification, main verification, release tagging, release asset checks,
  and roadmap upkeep.
- Updated README, changelog, roadmap, and downstream CI release pins.

## Compatibility

- Package version: `0.15.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.15.0"
verity --version
```

PyPI publishing remains prepared but requires PyPI-side trusted publishing
setup before enabling `publish_pypi=true`.
