# Versioning And Migrations

VeritySpec workspaces declare a `specVersion` in `verityspec.json`.

The current supported workspace format is:

```json
{
  "specVersion": "v0.1.0"
}
```

The CLI validates this version before treating a workspace as an executable
contract.

## Version Checks

Validation reports workspace version problems as normal issues:

| Code | Meaning |
|---|---|
| `workspace.version.missing` | `specVersion` is not present. |
| `workspace.version.invalid` | `specVersion` is not `vMAJOR.MINOR.PATCH`. |
| `workspace.version.unsupported` | The version is older or otherwise unsupported by this CLI. |
| `workspace.version.future` | The version is newer than this CLI supports. |

Future versions fail validation instead of being interpreted optimistically.
That keeps CI honest when a workspace requires a newer VeritySpec release.

## Migrate

`verity migrate` rewrites a workspace to a supported target version. The first
supported target is `v0.1.0`.

```bash
verity migrate ./workspace --dry-run --format json
verity migrate ./workspace --report-out build/migration-report.json
verity validate ./workspace
```

Dry-run mode reports the changes without writing files.

## Current Rewrite Rules

The `v0.1.0` migration normalizes conservative, common legacy shapes:

- `version` in workspace config becomes `specVersion`.
- Missing workspace `packs` becomes the default built-in pack set.
- Missing workspace `records` becomes `records/**/*.json`.
- Record `type` becomes `kind` when the value has a known VeritySpec mapping.
- Record `displayName` becomes `name`.
- Known legacy statuses such as `approved`, `active`, `locked`, and `stable`
  become `ready`.
- Missing record `name`, `status`, or `owner` receives a safe placeholder.
- Product records receive a default `version` when missing.

Every rewrite appears in the migration report. Placeholder owners and draft
statuses are also listed as manual follow-up items.

## Diffing

`verity diff` includes workspace-level version and pack metadata alongside
record additions, removals, and changes:

```bash
verity diff old-workspace new-workspace --format json
```

This makes migration review easier because a single diff shows both record
movement and contract-environment changes.

