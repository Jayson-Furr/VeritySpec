# VeritySpec v0.12.0 Release Notes

VeritySpec v0.12.0 makes pack generator capabilities more explicit for humans,
tools, and agents.

## Highlights

- Added structured generator metadata support in pack manifests.
- Preserved legacy string generator declarations for existing external packs.
- Kept `pack.generators` as a normalized generator ID list for compatibility.
- Added `generatorMetadata` to `verity pack list --format json`.
- Updated built-in pack manifests and `verity pack init` scaffolds to advertise
  generator name, description, artifact type, output formats, and record kinds.
- Added validation and tests for structured generator metadata.
- Updated README, changelog, roadmap, and generator/pack docs.

## Compatibility

- Package version: `0.12.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.12.0"
verity --version
```

PyPI publishing remains prepared but requires PyPI-side trusted publishing
setup before enabling `publish_pypi=true`.
