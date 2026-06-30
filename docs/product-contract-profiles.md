# Product Contract Profiles

Product-contract profiles are named enforcement modes for validation, lint,
readiness, and diagnostics. They let a workspace choose a policy posture that
matches the product context without changing the workspace format.

Profiles are available on:

```bash
verity validate examples/basic --profile release
verity lint examples/basic --profile strict
verity readiness examples/basic --profile release
verity doctor examples/basic --profile public-api --format json
```

`--profile` can be combined with `--format json`, `--github-annotations`, and
`--pack-path`. Explicit `--strict` and `--fail-on` flags still work; when they
are supplied, they make the selected profile stricter or change the exit policy
for the current command.

## Built-In Profiles

| Profile | Strict | Fail on | Purpose |
|---|---:|---|---|
| `release` | yes | error | Release-gate enforcement for shippable product contracts. |
| `strict` | yes | error | Strict validation, lint, and readiness enforcement. |
| `regulated` | yes | error | Release enforcement with governance pack coverage. |
| `public-api` | yes | error | Public API enforcement requiring API contract coverage. |
| `internal-tool` | no | error | Internal-tool enforcement where warnings remain advisory. |

## Profile-Specific Checks

`regulated` requires these packs:

- `verity.pack.security`
- `verity.pack.accessibility`
- `verity.pack.compliance`

`public-api` requires:

- `verity.pack.api`
- at least one `api.endpoint` record

Missing profile requirements produce `profile.required_pack` or
`profile.required_record_kind` issues.

## JSON Output

When `--profile` is used, JSON output includes profile metadata:

```json
{
  "command": "validate",
  "passed": true,
  "profile": {
    "id": "release",
    "name": "Release",
    "strict": true,
    "failOn": "error",
    "effectiveStrict": true,
    "effectiveFailOn": "error"
  }
}
```

Machine clients should read `effectiveStrict` and `effectiveFailOn` to
understand the actual command policy after combining the profile with explicit
CLI flags.

## Choosing a Profile

Use `internal-tool` for early internal utilities where warnings should guide
work without failing the command.

Use `strict` when you want all validation and lint warnings promoted to errors
without adding product-surface assumptions.

Use `release` for normal shippable product-contract checks.

Use `public-api` for products whose public API contract must be present and
release-clean.

Use `regulated` for workspaces that must include security, accessibility, and
compliance governance coverage before release.
