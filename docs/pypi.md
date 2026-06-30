# PyPI Publishing

VeritySpec is prepared for PyPI publishing through GitHub Actions trusted
publishing, but PyPI publishing is not enabled yet.

Current publishing decision:

- Do not publish `verityspec` to PyPI until PyPI-side trusted publishing is
  configured and the maintainer explicitly enables publishing.
- Use GitHub release installation as the canonical public install path until
  that decision changes.
- Keep `publish_pypi=false` unless a release run is intentionally publishing
  to PyPI.

As of June 30, 2026, `https://pypi.org/pypi/verityspec/json` returned `404` in
the readiness check for this sprint. That is an observation, not a guarantee;
re-check PyPI immediately before claiming or publishing the package name.

## User Installation

After the `verityspec` project is published on PyPI:

```bash
pip install verityspec
verity --version
```

Until PyPI publishing is enabled, install from GitHub:

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.18.0"
verity --version
```

## Repository Setup Completed

- Release workflow builds source and wheel distributions.
- Release workflow checks distributions with `twine check`.
- Release workflow smoke-tests the built wheel.
- GitHub `pypi` environment exists.
- Manual release workflow has a `publish_pypi` option.
- Release checklist requires local distribution build, `twine check`, and wheel
  smoke testing before tagging.
- Tests keep this document's GitHub install fallback tag aligned with the
  current package version.

## Current Blockers

- The `verityspec` project still needs to be created or claimed on PyPI.
- PyPI trusted publishing must be configured on the PyPI project.
- A maintainer must explicitly choose to publish a release to PyPI.

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

## Readiness Verification

Before enabling PyPI publishing, verify:

```bash
python3 -m pip install --upgrade build twine
rm -rf dist
python3 -m build
python3 -m twine check dist/*
python3 -m venv /tmp/verityspec-wheel
/tmp/verityspec-wheel/bin/python -m pip install --upgrade pip
/tmp/verityspec-wheel/bin/pip install dist/*.whl
/tmp/verityspec-wheel/bin/verity --version
/tmp/verityspec-wheel/bin/verity pack validate
/tmp/verityspec-wheel/bin/verity validate examples/basic
```

Then verify the PyPI project and trusted-publishing configuration outside the
repository before running the release workflow with `publish_pypi=true`.
