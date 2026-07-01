# VeritySpec v0.46.0 Release Notes

VeritySpec v0.46.0 adds the installed-pack discovery foundation needed before
domain-heavy packs can eventually move into official extension packages.

## Highlights

- Added the `verityspec.packs` Python entry-point group for installed pack
  packages.
- Loaded installed packs by pack ID without requiring manual `packPaths`.
- Preserved bundled built-in pack behavior and explicit local pack path
  precedence.
- Added installed-pack source reporting to pack summaries and pack capability
  indexes.
- Added tests that simulate installed pack entry points without publishing a
  package.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.46.0"
verity --version
```

PyPI publishing is prepared but not enabled yet. GitHub release installation
remains the canonical public install path for this release.

## Verification

Release verification should include:

```bash
verity pack list --format json
verity pack validate
verity validate tests/fixtures/custom_pack_workspace
verity generate pack-capability-index tests/fixtures/custom_pack_workspace --out build/pack-capability-index.json
python -m json.tool build/pack-capability-index.json >/dev/null
```

Existing built-in packs remain bundled in this release. Installed-pack
discovery is additive and does not separate any bundled pack yet.
