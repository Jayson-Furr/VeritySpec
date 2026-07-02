# VeritySpec v0.68.0 Release Notes

VeritySpec v0.68.0 adds an installed-pack compatibility metadata design note
for future official extension packages before runtime enforcement or
specialized-pack detachment begins.

## Highlights

- Added the public
  [installed-pack compatibility metadata](installed-pack-compatibility-metadata.md)
  design note.
- Defined the proposed compatibility metadata shape for supported VeritySpec
  versions, workspace format versions, pack API level, and official
  extension-package lifecycle states.
- Documented lifecycle states for `bundled`, `mirrored`, `official-preview`,
  `detached`, `deprecated`, and `removed` extension-package states.
- Clarified discovery and source precedence across `verityspec.packs`, local
  `packPaths`, built-in pack ID reservation, and future official detach gates.
- Linked the design note from README, pack docs, specialized-pack separation
  guidance, official-extension fixture guidance, engine/product-delivery pack
  direction, ADR guidance, and branching guidance.
- Added tests that keep the design note discoverable and preserve the
  no-runtime-enforcement boundary.
- Rotated the next-20 roadmap queue after converting the metadata design note
  into sprint 145.

This release does not enforce compatibility metadata at runtime, detach bundled
specialized packs, publish official extension packages, change
`verityspec.packs` entry-point loading behavior, allow installed packages to
shadow built-in pack IDs, rename pack IDs or record kinds, or change pack
manifest validation requirements.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.68.0"
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
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release.
