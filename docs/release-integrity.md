# Release Integrity Checks

VeritySpec release prep includes a test-backed consistency check for public
version and release surfaces.

The release integrity tests live in `tests/test_release_integrity.py`. They
read the current package version from `pyproject.toml` and
`src/verityspec/__init__.py`, then verify that release-facing files agree with
that version.

The checked surfaces include:

- README release badge, latest-release text, GitHub install command,
  package-version text, and current release-notes link.
- `CHANGELOG.md` and the current release-notes document.
- Downstream CI docs, reusable workflow defaults, and maintained workflow
  templates under `templates/github-actions/`.
- `docs/pypi.md` GitHub fallback install guidance.
- `docs/release-checklist.md` tag examples.
- Evidence example and golden fixture release-artifact references.

Run the focused check during release prep:

```bash
PYTHONPATH=src:. python3 -m pytest -q tests/test_release_integrity.py
```

The full test suite also runs these checks. When a release version is bumped,
the release PR should update these surfaces together instead of fixing them
after the tag is already public.
