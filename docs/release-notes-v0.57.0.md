# VeritySpec v0.57.0 Release Notes

VeritySpec v0.57.0 adds the first portfolio-level validation foundation for
multi-workspace product, service, library, game, engine-toolkit, shared-library,
integration, and portfolio workspaces.

## Highlights

- Added `docs/portfolio-validation.md` to define portfolio-level validation
  boundaries before aggregate reports, workspace dependency resolution,
  lockfiles, workspace-format changes, or portfolio CLI behavior.
- Added `examples/portfolio`, an executable product-delivery workspace that
  models local-only portfolio validation posture, readiness profiles, evidence
  requirements, future report capabilities, validation runners, editor
  surfaces, and agent-context handoff boundaries.
- Updated the workspace compatibility manifest and tests so the portfolio
  example validates, lints, passes readiness, and remains covered across
  supported workspace format versions.
- Documented engine portfolio patterns for Unity, Godot, Unreal, game-core,
  game-assets, product-delivery, evidence, mobile, and liveops workspaces
  without making commercial, legal, privacy-law, marketplace,
  platform-certification, store-review, pricing-approval, app-store-approval,
  or support-SLA claims.
- Added organization-wide agent reuse, work-ledger, and content-opportunity
  guidance to `AGENTS.md` so future reusable terms and practices consult the
  organization pattern and glossary repositories.
- Updated README, changelog, roadmap, release checklist, downstream workflow
  pins, evidence fixtures, and release-integrity surfaces for v0.57.0.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.57.0"
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
verity validate examples/portfolio
verity lint examples/portfolio --strict
verity readiness examples/portfolio --strict
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release.
