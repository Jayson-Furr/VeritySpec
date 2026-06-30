# Release Checklist

Use this checklist for public releases.

## Before Tagging

- Confirm `CHANGELOG.md` has an entry for the release.
- Confirm the version in `pyproject.toml` and `src/verityspec/__init__.py`
  matches the intended tag.
- Run local checks:

```bash
python -m pip install --upgrade build twine
python -m unittest discover -s tests -v
verity pack validate
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity validate examples/security
verity lint examples/security --strict
verity readiness examples/security --strict
verity validate tests/fixtures/custom_pack_workspace
verity validate tests/fixtures/generator_maturity
verity generate security-report examples/security --out build/security-report.json
python -m build
twine check dist/*
```

## Tag

```bash
VERSION=v0.6.0
git tag -a "$VERSION" -m "VeritySpec $VERSION"
git push origin "$VERSION"
```

Pushing a `v*` tag runs the release workflow, builds the distributions, checks
them, smoke-tests the wheel, and creates a GitHub release with the artifacts.

## PyPI

PyPI publishing is prepared through GitHub Actions trusted publishing. Before
using it:

- Create the `verityspec` project on PyPI or claim the name.
- Configure PyPI trusted publishing for `Jayson-Furr/VeritySpec`.
- Confirm the GitHub `pypi` environment exists.
- Run the `Release` workflow manually with `publish_pypi=true`.
