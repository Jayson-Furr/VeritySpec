# VeritySpec v0.4.0 Release Notes

VeritySpec v0.4.0 adds version-aware workspace migration chains and promotes
the workspace format to `v0.2.0`.

## Highlights

- Workspace format `v0.2.0` is now the current format.
- `v0.2.0` workspaces declare `packPaths` explicitly, using `[]` when no local
  external packs are used.
- `v0.1.0` workspaces remain supported for compatibility.
- `verity migrate` now plans migration paths instead of relying on one
  hard-coded target rewrite.
- Legacy workspaces migrate through `legacy -> v0.1.0 -> v0.2.0` by default.
- `verity migrate --list` reports supported workspace versions and migration
  steps without requiring a workspace.
- The PrismSpec importer remains a conservative `v0.1.0` bridge, and docs now
  tell users to run `verity migrate` afterward to promote imports to the
  current workspace format.

## Compatibility

- Python: 3.9 through 3.12.
- VeritySpec workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- Package version: `0.4.0`.

## Publishing Notes

GitHub release artifacts are built by the release workflow. PyPI publishing is
prepared but still requires PyPI-side trusted-publishing setup before
`publish_pypi=true` can be used.
