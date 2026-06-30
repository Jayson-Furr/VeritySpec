# VeritySpec v0.3.0 Release Notes

VeritySpec v0.3.0 improves generator precision, Python model output, extension
pack authoring, and repository operating discipline for humans and AI agents.

## Highlights

- OpenAPI generator precision: path parameters are inferred from endpoint paths,
  explicit endpoint parameters are emitted, duplicates are avoided, and golden
  output coverage protects the generated contract.
- Python model generation now emits nested dataclasses for inline object schemas
  and inline object schemas inside arrays.
- Pack authoring now starts from `verity pack init`, which creates a validating
  local pack scaffold with a manifest, starter schema, readiness gate, and
  schema-bundle generator declaration.
- The repository now has a formal branching strategy and AI-agent rules for
  branch selection, shell discipline, post-commit context refresh, README and
  changelog bookkeeping, and local verification when GitHub Actions is
  unavailable for billing, credit, quota, or runner reasons.
- README badges and install guidance now reflect the current publishing state:
  GitHub release installs are active, while PyPI publishing remains prepared but
  not enabled.

## Compatibility

- Python: 3.9 through 3.12.
- VeritySpec workspace format: `v0.1.0`.
- Package version: `0.3.0`.

## Publishing Notes

GitHub release artifacts are built by the release workflow. PyPI publishing is
prepared but still requires PyPI-side trusted-publishing setup before
`publish_pypi=true` can be used.
