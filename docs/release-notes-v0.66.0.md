# VeritySpec v0.66.0 Release Notes

VeritySpec v0.66.0 adds official-extension compatibility fixture groundwork for
future specialized pack separation. The release adds `verity pack compare`,
which compares a loaded source pack with a mirror pack path without loading that
mirror into the active registry.

## Highlights

- Added `verity pack compare <pack-id> --mirror <path>` with text and JSON
  output.
- Compared manifest identity, schema declarations, schema JSON content,
  readiness gates, reference rules, and generator metadata.
- Added stable issue-code explanations for mirror ID mismatches, invalid mirror
  paths, and source/mirror surface drift.
- Added the first official-extension mirror fixture for the future
  `verityspec-pack-unity` package.
- Documented the mirror fixture contract, acceptance gate, CI usage, and
  non-goals before any bundled-pack detach sprint begins.
- Updated README, pack docs, CI guidance, release checklist, specialized-pack
  separation guidance, roadmap, changelog, and canonical AI-agent command
  examples.

This release does not detach bundled specialized packs, publish official
extension packages, allow arbitrary installed packages to shadow built-in pack
IDs, add package compatibility metadata enforcement, or guarantee third-party
package compatibility beyond explicit mirror fixture comparison.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.66.0"
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
verity pack compare verity.pack.unity --mirror tests/fixtures/official_extension_mirrors/verityspec-pack-unity/pack --format json
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release.
