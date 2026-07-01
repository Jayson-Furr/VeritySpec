# VeritySpec v0.13.0 Release Notes

VeritySpec v0.13.0 hardens external pack authoring by proving generated pack
scaffolds can be used by a real workspace immediately.

## Highlights

- Added end-to-end CLI coverage that creates a pack with `verity pack init`.
- Verified the generated pack passes `verity pack validate`.
- Verified a sample workspace can load the generated pack through `packPaths`.
- Verified that workspace passes validation, strict linting, strict readiness,
  and schema-bundle generation.
- Updated generated pack scaffolds with a default `product` to generated-kind
  `uses` reference rule so starter workspaces can connect product contracts to
  external records without custom manifest editing.
- Added release badge bookkeeping to the AI-agent entry point and release
  checklist so README release updates include the visible badge.
- Updated README, changelog, roadmap, and pack docs.

## Compatibility

- Package version: `0.13.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.13.0"
verity --version
```

PyPI publishing remains prepared but requires PyPI-side trusted publishing
setup before enabling `publish_pypi=true`.
