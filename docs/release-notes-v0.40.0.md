# VeritySpec v0.40.0 Release Notes

VeritySpec v0.40.0 expands the built-in Unity pack from the first Unity
implementation records into a broader Unity implementation and engine-tooling
contract surface.

## Highlights

- Expanded built-in `verity.pack.unity`.
- Added strict schemas for `unity.package`, `unity.shared-library`,
  `unity.prefab`, `unity.asmdef`, `unity.scanner`,
  `unity.validation-runner`, `unity.readiness-dashboard`, and
  `unity.agent-context-exporter`.
- Added Unity readiness gates and reference rules for package/library,
  prefab/assembly, scanner, validation-runner, dashboard, and agent-context
  handoff records.
- Expanded `examples/unity` with executable package, shared-library, prefab,
  assembly, scanner, validation-runner, readiness-dashboard, and
  agent-context-exporter records.
- Added Unity graph checks to CI guidance, the release checklist, the main CI
  workflow, and AI-agent common commands.
- Updated cross-pack coverage fixtures and golden compatibility outputs so the
  expanded Unity surface is reviewed intentionally.
- Updated the engine/product-delivery roadmap so future Godot and Unreal packs
  are planned as engine plus game-workspace packs, not tooling-only packs.

## Compatibility

- Package version: `0.40.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace format migration is required.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.40.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
