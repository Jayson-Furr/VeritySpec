# VeritySpec v0.28.0 Release Notes

VeritySpec v0.28.0 adds the first deployment-target pack for runtime, hosting,
release environment, rollback, and production readiness contracts.

## Highlights

- Added `verity.pack.deployment`.
- Added `deployment.runtime` records for runtime type, runtime name, version,
  artifact type, entrypoint, language, and dependencies.
- Added `deployment.target` records for environment, provider, platform,
  regions, runtime links, release policy, rollback plan, health check URL, and
  deployment configuration paths.
- Added `runtimeRef` graph reference resolution so deployment targets can prove
  their runtime contract exists and is allowed.
- Added production readiness controls requiring approval, rollback, and health
  check coverage for production deployment targets.
- Added `verity generate deployment-report` for release and operations review.
- Added `examples/deployment` as an executable deployment workspace.
- Added deployment report golden coverage, example compatibility coverage, CLI
  tests, and package-data wheel smoke verification.
- Updated README, CI, release checklist, pack docs, generator docs, readiness
  docs, changelog, roadmap, and AI-agent command guidance.

## Compatibility

- Package version: `0.28.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.28.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
