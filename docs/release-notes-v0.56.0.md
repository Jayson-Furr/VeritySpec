# VeritySpec v0.56.0 Release Notes

VeritySpec v0.56.0 adds engine full-lifecycle support design guidance for
Unity, Godot, Unreal, shared engine libraries, lifecycle readiness, evidence,
liveops, decommissioning, archive, and portfolio examples.

## Highlights

- Added engine full-lifecycle support design guidance for Unity, Godot, and
  Unreal game workspaces.
- Defined workspace shapes for engine toolkit workspaces, shared engine
  library workspaces, game workspaces, integration workspaces, and portfolio
  workspaces.
- Captured lifecycle stages from concept through archive and named future
  readiness profiles such as `engine-prototype-ready`, `game-release-ready`,
  `liveops-ready`, `decommission-ready`, and `archive-ready`.
- Preserved engine parity expectations for Unity, Godot, and Unreal additions.
- Documented evidence, liveops, maintenance, decommissioning, archive, and
  agent-context boundaries without making commercial, legal, privacy-law,
  marketplace, platform-certification, or store-review guarantees.
- Added executable documentation tests, README links, changelog updates, and
  roadmap/Next 20 planning.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.56.0"
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
