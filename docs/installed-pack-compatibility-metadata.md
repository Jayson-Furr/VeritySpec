# Installed Pack Compatibility Metadata

VeritySpec can discover installed pack packages through the
`verityspec.packs` Python entry-point group. That discovery contract is useful,
but official extension packages also need an explicit compatibility contract
before bundled specialized packs can safely move out of the core wheel.

This note defines the intended metadata shape and adoption path.

No runtime compatibility enforcement is introduced by this design note.

## Goals

- Give installed and future official extension packs a machine-readable way to
  declare supported VeritySpec versions.
- Declare supported workspace format versions separately from package versions.
- Define a pack API level so pack authors can state which manifest, schema,
  readiness, reference-rule, generator, and discovery features they require.
- Name official extension-package lifecycle states before a detach gate exists.
- Keep current bundled-pack behavior stable while compatibility metadata is
  reviewed, tested, and later enforced deliberately.

## Proposed Metadata Shape

Future pack manifests or package metadata should expose a `compatibility`
object with this shape:

```json
{
  "compatibility": {
    "verityspec": {
      "supportedVersions": [">=0.68.0,<1.0.0"],
      "testedVersions": ["0.68.0"]
    },
    "workspaceFormats": {
      "supportedVersions": ["v0.1.0", "v0.2.0"],
      "defaultVersion": "v0.2.0"
    },
    "packApi": {
      "level": "2026.07",
      "features": [
        "json-schema",
        "readiness-gates",
        "reference-rules",
        "generator-metadata",
        "installed-pack-entry-point"
      ]
    },
    "officialExtension": {
      "state": "bundled",
      "distribution": "verityspec-pack-unity",
      "packIds": ["verity.pack.unity"],
      "bundledFallback": true
    }
  }
}
```

The exact schema can evolve before enforcement. The stable intent is that
compatibility metadata answers four questions:

- Which `verityspec` package versions can load this pack?
- Which workspace format versions can use records from this pack?
- Which pack API level and features does this pack require?
- Which official extension-package lifecycle state is this package in?

## Field Semantics

`compatibility.verityspec.supportedVersions` should use package-version ranges
that future tooling can evaluate before loading a pack into a workspace.
`testedVersions` is evidence-oriented and should identify versions used in CI
or release verification.

`compatibility.workspaceFormats.supportedVersions` should list workspace
format versions such as `v0.1.0` and `v0.2.0`. Workspace format support is not
the same as the Python package version. A pack can support multiple workspace
formats while requiring a newer `verityspec` package to load or validate.

`compatibility.packApi.level` should identify the VeritySpec pack contract the
package expects. Initial levels should be calendar-like and conservative, such
as `2026.07`, until a formal API-version scheme is accepted. `features` should
name required pack surfaces, not product-domain record kinds.

`compatibility.officialExtension.state` should describe packaging maturity
without changing source precedence. The distribution name is the Python
package name, such as `verityspec-pack-unity`; the pack ID remains stable, such
as `verity.pack.unity`.

## Lifecycle States

Official extension packages should use explicit lifecycle states:

| State | Meaning |
|---|---|
| `bundled` | The pack is carried in the `verityspec` wheel. |
| `mirrored` | A candidate package mirrors a bundled pack for comparison only. |
| `official-preview` | An official package exists but bundled fallback remains the default. |
| `detached` | A controlled official detach gate can load the package for a formerly bundled pack ID. |
| `deprecated` | The package or pack surface still resolves but should not be used for new work. |
| `removed` | The package or pack surface is no longer valid and must fail when referenced. |

These states are packaging lifecycle states.

Record lifecycle remains governed by the record status model, and workspace
format support remains governed by workspace versioning and migrations.

## Discovery And Precedence

Compatibility metadata should complement existing discovery rules:

- installed packages expose pack paths through `verityspec.packs`;
- the entry-point name must still match the pack manifest `id`;
- explicit local `packPaths` and `--pack-path` entries remain explicit
  overrides;
- built-in pack IDs remain reserved until a controlled official detach gate
  exists; and
- arbitrary installed packages must not shadow built-in pack IDs.

Future enforcement should report incompatibilities through `verity pack
doctor`, `verity pack validate`, and CI-friendly JSON diagnostics before a
workspace attempts readiness or generator work.

## Adoption Phases

1. Document the metadata contract and keep existing runtime behavior unchanged.
2. Add optional manifest validation warnings and diagnostics once the schema is
   reviewed.
3. Add official-extension mirror fixtures that include compatibility metadata.
4. Add non-throwing `verity pack doctor --format json` compatibility reports.
5. Add strict validation or detach-gate enforcement only after migration and
   rollback guidance exists.

## Validation Intent

When runtime enforcement is added later, VeritySpec should be able to detect:

- installed pack versions that do not support the current `verityspec`
  package;
- packs that do not support the current workspace format version;
- packs that require a newer pack API level than the runtime implements;
- official extension packages that claim a detached state without a supported
  detach gate;
- package metadata that names pack IDs not present in the manifest; and
- deprecated or removed official extension packages still referenced by
  workspaces.

## Non-Goals

This design note does not:

- enforce compatibility metadata at runtime;
- detach bundled specialized packs;
- publish official extension packages;
- change `verityspec.packs` entry-point loading behavior;
- allow installed packages to shadow built-in pack IDs;
- rename pack IDs, record kinds, or workspace `packs` entries; or
- change pack manifest validation requirements in this release.

The specialized-pack separation plan remains the governing document for any
future bundled-pack detach sprint.
