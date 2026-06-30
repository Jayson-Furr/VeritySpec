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
python -m build
twine check dist/*
```

## Tag

```bash
git tag -a v0.1.0 -m "VeritySpec v0.1.0"
git push origin v0.1.0
```

Pushing a `v*` tag runs the release workflow, builds the distributions, checks
them, smoke-tests the wheel, and creates a GitHub release with the artifacts.

## PyPI

PyPI publishing is prepared through GitHub Actions trusted publishing. Before
using it:

- Create the `verityspec` project on PyPI or claim the name.
- Configure PyPI trusted publishing for `Jayson-Furr/VeritySpec`.
- Create the GitHub `pypi` environment.
- Run the `Release` workflow manually with `publish_pypi=true`.

