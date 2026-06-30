# PyPI Publishing

VeritySpec is prepared for PyPI publishing through GitHub Actions trusted
publishing.

## User Installation

After the `verityspec` project is published on PyPI:

```bash
pip install verityspec
verity --version
```

Until PyPI publishing is enabled, install from GitHub:

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.2.0"
verity --version
```

## Repository Setup Completed

- Release workflow builds source and wheel distributions.
- Release workflow checks distributions with `twine check`.
- Release workflow smoke-tests the built wheel.
- GitHub `pypi` environment exists.
- Manual release workflow has a `publish_pypi` option.

## Required PyPI-Side Setup

Before using `publish_pypi=true`:

1. Create or claim the `verityspec` project on PyPI.
2. Configure PyPI trusted publishing for:
   - Owner: `Jayson-Furr`
   - Repository: `VeritySpec`
   - Workflow: `release.yml`
   - Environment: `pypi`
3. Run the `Release` workflow manually with `publish_pypi=true`.

No PyPI API token should be committed to this repository.
