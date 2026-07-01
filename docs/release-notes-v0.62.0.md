# VeritySpec v0.62.0 Release Notes

VeritySpec v0.62.0 adds the first executable local workspace dependency
prototype. Workspaces can now declare direct local, readonly dependencies,
reference exported dependency records through aliases, validate those
cross-workspace references, and include exported dependency records in graph
JSON output.

## Highlights

- Added optional workspace `dependencies` declarations for direct local
  workspace dependencies.
- Added alias-qualified dependency references such as
  `sharedUnity::unity.package.save_system`.
- Added dependency validation for missing sources, load failures, workspace ID
  mismatches, version constraints, duplicate or unknown aliases, missing
  dependency records, invalid export lists, and non-exported dependency
  references.
- Added manifest-level dependency workspace `exports` lists for the prototype
  exported-record boundary.
- Added dependency-aware graph JSON output with alias-qualified dependency
  nodes and top-level dependency metadata.
- Added Unity shared-runtime dependency fixtures with positive and negative
  validation coverage.
- Added stable issue-code explanations and issue-code catalog coverage for the
  new dependency issues.
- Updated workspace-format, graph-check, cross-workspace dependency,
  versioning, README, changelog, and roadmap documentation.

This release remains intentionally local-only. It does not add remote
registries, Git authentication, transitive dependency policy, lockfiles,
dependency update commands, or record-level visibility fields.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.62.0"
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
verity validate tests/fixtures/workspace_dependencies/consumer
verity lint tests/fixtures/workspace_dependencies/consumer --strict
verity readiness tests/fixtures/workspace_dependencies/consumer --strict
verity graph tests/fixtures/workspace_dependencies/consumer --format json
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release.
