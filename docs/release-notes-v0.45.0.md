# VeritySpec v0.45.0 Release Notes

VeritySpec v0.45.0 adds built-in progression and evidence pack foundations.

## Highlights

- Added `verity.pack.progression` for XP models, levels, unlocks, tracks, and
  progression gates.
- Added `verity.pack.evidence` for concrete test, CI, build, review,
  screenshot, video, QA, playtest, certification-checklist, and artifact
  evidence records.
- Added `verity generate evidence-report` for summarizing evidence coverage,
  subject resolution, and release gaps.
- Added executable `examples/progression` and `examples/evidence` workspaces.
- Expanded cross-pack coverage dashboards to track progression and evidence as
  first-class product surfaces.
- Preserved engine parity with Unity, Godot, and Unreal reference rules for
  progression implementation and evidence-producing validation/readiness
  tooling.

## Verification

Release verification should include:

```bash
verity pack validate
verity validate examples/progression
verity lint examples/progression --strict
verity readiness examples/progression --strict
verity graph examples/progression
verity validate examples/evidence
verity lint examples/evidence --strict
verity readiness examples/evidence --strict
verity graph examples/evidence
verity generate evidence-report examples/evidence --out build/evidence-report.json
verity generate schema-bundle examples/progression --out build/progression-schema-bundle.json
verity generate schema-bundle examples/evidence --out build/evidence-schema-bundle.json
```

VeritySpec can model evidence and readiness requirements, but downstream teams
remain responsible for legal, privacy, marketplace, platform certification,
support, and store-review approvals.
