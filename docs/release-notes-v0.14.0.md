# VeritySpec v0.14.0 Release Notes

VeritySpec v0.14.0 makes downstream GitHub Actions adoption copyable,
version-pinned, and covered by release-tag drift tests.

## Highlights

- Added maintained downstream workflow templates for direct-install,
  reusable-workflow, and local-pack product-contract checks.
- Updated downstream CI documentation to point to maintained template files.
- Updated the reusable product-contract workflow default install command to the
  current release tag.
- Added tests that fail when downstream templates, docs, or reusable workflow
  defaults reference stale VeritySpec release tags.
- Updated README, changelog, roadmap, and downstream CI docs.

## Compatibility

- Package version: `0.14.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.14.0"
verity --version
```

PyPI publishing remains prepared but requires PyPI-side trusted publishing
setup before enabling `publish_pypi=true`.
