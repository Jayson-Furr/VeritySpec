# VeritySpec v0.2.0 Release Notes

VeritySpec v0.2.0 turns the initial executable package into a more complete
product-contract toolchain.

## Highlights

- Public package polish with badges, install guidance, PyPI trusted-publishing
  preparation, and GitHub `pypi` environment setup.
- Contract intelligence commands: `verity doctor`, `verity explain`,
  `--fail-on`, graph focus/orphan/cycle filters, and richer validation reports.
- PrismSpec migration bridge with conservative mappings and explicit migration
  reports.
- Workspace version registry, workspace version validation, `verity migrate`,
  and version-aware diff metadata.
- External pack loading through workspace `packPaths`, CLI `--pack-path`, and
  external pack list/validate support.
- Generator maturity improvements for OpenAPI, AsyncAPI, TypeScript, and Python
  models, with golden snapshot tests.
- Canonical AI-agent entry point through `AGENTS.md` and thin adapter files for
  common AI coding agents.
- Downstream product-contract CI guidance and a reusable GitHub Actions workflow.

## Compatibility

- Python: 3.9 through 3.12.
- VeritySpec workspace format: `v0.1.0`.
- Package version: `0.2.0`.

## Publishing Notes

GitHub release artifacts are built by the release workflow. PyPI publishing is
prepared but still requires PyPI-side trusted-publishing setup before
`publish_pypi=true` can be used.
