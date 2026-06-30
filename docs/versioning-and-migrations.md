# Versioning And Migrations

VeritySpec workspaces declare a `specVersion` in `verityspec.json`.

The current workspace format is:

```json
{
  "specVersion": "v0.2.0",
  "packPaths": []
}
```

The CLI validates this version before treating a workspace as an executable
contract. VeritySpec currently supports both `v0.1.0` and `v0.2.0`; `v0.2.0`
is the current format.

## Version Checks

Validation reports workspace version problems as normal issues:

| Code | Meaning |
|---|---|
| `workspace.version.missing` | `specVersion` is not present. |
| `workspace.version.invalid` | `specVersion` is not `vMAJOR.MINOR.PATCH`. |
| `workspace.version.unsupported` | The version is older or otherwise unsupported by this CLI. |
| `workspace.version.future` | The version is newer than this CLI supports. |
| `workspace.packPaths.missing` | A `v0.2.0` workspace does not declare `packPaths`. |
| `workspace.packPaths.invalid` | A `v0.2.0` workspace declares `packPaths` in the wrong shape. |

Future versions fail validation instead of being interpreted optimistically.
That keeps CI honest when a workspace requires a newer VeritySpec release.

## Compatibility Matrix

The test suite rewrites positive fixture workspaces across every supported
workspace `specVersion` and runs validation, lint, and readiness checks. This
guards against accidental drift when the current workspace format changes while
older supported formats remain valid.

## Migrate

`verity migrate` rewrites a workspace to a supported target version. By
default, it migrates to the current format, `v0.2.0`.

```bash
verity migrate --list --format json
verity migrate ./workspace --dry-run --format json
verity migrate ./workspace --report-out build/migration-report.json
verity validate ./workspace
```

Dry-run mode reports the changes without writing files. `--list` reports the
supported workspace versions and migration steps without requiring a workspace.
The test suite includes committed dry-run fixtures for each supported migration
edge so migration reports and non-mutating behavior stay stable as the format
registry grows.

The current migration path from legacy workspaces is:

```text
legacy -> v0.1.0 -> v0.2.0
```

Use `--to v0.1.0` when a legacy workspace must be rewritten only to the initial
supported format.

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

The `v0.2.0` migration makes external pack resolution explicit:

- `specVersion` becomes `v0.2.0`.
- Missing or invalid `packPaths` becomes `[]`.

## Diffing

`verity diff` includes workspace-level version and pack metadata alongside
record additions, removals, and changes:

```bash
verity diff old-workspace new-workspace --format json
```

This makes migration review easier because a single diff shows both record
movement and contract-environment changes.

JSON output keeps the legacy top-level fields and also includes
machine-readable change metadata:

- `summary.totalChanges`
- `summary.breakingChanges`
- `summary.hasBreakingChanges`
- `summary.bySeverity`
- `changes[]` with `type`, `severity`, `breaking`, `reasons`, and the affected
  `recordId` or `packId`

Breaking changes currently include removed packs, removed records, record kind
changes, records marked removed, API endpoint method/path changes, removed API
response status codes, and schema-object contract removals such as removed
properties, required fields, enum values, or type changes.

Text output prints the same severity summary and a breaking-change section
before the existing pack and record lists.
