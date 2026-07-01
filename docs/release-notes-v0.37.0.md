# VeritySpec v0.37.0 Release Notes

VeritySpec v0.37.0 adds the first built-in Unity implementation pack:
`verity.pack.unity`.

## Highlights

- Added built-in `verity.pack.unity`.
- Added strict schemas for `unity.project`, `unity.package-dependency`,
  `unity.scene`, and `unity.build-target`.
- Added Unity readiness gates that require traceable Unity project metadata,
  package dependency intent, scene contracts, build-target contracts, and
  implementation references.
- Added Unity reference rules that connect products and game products to Unity
  projects, Unity projects to packages, scenes, and build targets, scenes to
  package dependencies, and build targets to scenes and packages.
- Added executable `examples/unity` using the Dream Extraction concept,
  composed with `verity.core`, `verity.pack.game-core`, and
  `verity.pack.unity`.
- Added Unity support to cross-pack coverage dashboards and golden coverage
  fixtures.
- Added schema-bundle smoke coverage for Unity records.
- Updated README, pack docs, generator docs, readiness docs, CI docs, release
  checklist, roadmap, changelog, workflow checks, and AI-agent guidance.
- Kept future game expansion scoped: gameplay, content, liveops, evidence,
  dependencies, archive, and portfolio behavior remain future packs or
  features.

## Compatibility

- Package version: `0.37.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace format migration is required.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.37.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
