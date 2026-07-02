# VeritySpec v0.65.0 Release Notes

VeritySpec v0.65.0 adds installed-pack health diagnostics for maintainers who
debug separately installed or local extension packs. The release adds a
non-throwing `verity pack doctor` command that reports discovery health without
changing the existing strict loader behavior used by workspace validation,
readiness, graphing, generators, `verity pack list`, or `verity pack validate`.

## Highlights

- Added `verity pack doctor` with text and JSON output.
- Reported installed `verityspec.packs` entry-point load failures, missing or
  invalid manifests, entry-point name mismatches, duplicate installed pack IDs,
  and installed pack IDs that collide with built-in packs.
- Reported local external pack path failures, invalid manifests, duplicate
  local pack IDs, and local pack IDs that collide with built-in packs.
- Added explicit local override warnings for cases where `packPaths`,
  `--pack-path`, or `verity pack --path` entries take precedence over
  installed packs with the same ID.
- Added stable issue-code explanations and refreshed issue-code catalog
  fixtures for the new diagnostics.
- Updated README, pack docs, CI guidance, release checklist, external-pack
  review guidance, specialized-pack separation guidance, roadmap, changelog,
  and canonical AI-agent command examples.

This release does not detach bundled specialized packs, publish official
extension packages, allow arbitrary installed packages to shadow built-in pack
IDs, add compatibility metadata enforcement, or guarantee third-party package
health beyond observable local Python entry-point and pack-manifest
diagnostics.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.65.0"
verity --version
```

PyPI publishing is prepared but not enabled yet. GitHub release installation
remains the canonical public install path for this release.

## Verification

Release verification should include:

```bash
python -m unittest discover -s tests -v
verity pack validate
verity pack doctor --format json
verity pack doctor --path tests/fixtures/custom_pack --format json
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release.
