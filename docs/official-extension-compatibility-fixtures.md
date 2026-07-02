# Official Extension Compatibility Fixtures

Official extension packages are a future packaging path for domain-heavy packs
that are currently bundled with `verityspec`. Before any bundled pack can move
out of the core wheel, maintainers need a fixture that proves the candidate
extension package mirrors the bundled pack contract.

This fixture guidance is for mirror validation only. It does not detach
bundled packs, does not publish official extension packages, does not make a
package marketplace claim, and does not allow arbitrary installed packages to
shadow built-in pack IDs.

## Mirror Contract

An official-extension mirror fixture should preserve these surfaces from the
bundled source pack:

- manifest identity: `id`, `version`, `name`, and `description`;
- schema declarations: every declared record kind and schema path;
- schema JSON content: strict schemas, required envelope fields, enums,
  references, and pack-specific fields;
- readiness gates: gate IDs, target kinds, required fields, and cardinality
  rules;
- reference rules: source kinds, relationship names, and target kinds;
- generator metadata: generator IDs, output formats, artifact types, and
  record kinds;
- example or workspace coverage that proves the record kinds still validate,
  lint, pass readiness, and graph as expected once a real detach gate exists.

The mirror should keep the existing pack ID and record kinds. Packaging changes
must not force workspaces to rename `packs` entries or record `kind` values.

## Fixture Layout

The first mirror fixture lives at:

```text
tests/fixtures/official_extension_mirrors/
  verityspec-pack-unity/
    pack/
      pack.json
      schemas/
```

`verityspec-pack-unity` is the candidate Python distribution name. The pack ID
inside the fixture remains `verity.pack.unity`.

## Commands

Use `verity pack compare` to compare the bundled pack with a mirror path
without loading the mirror into the active registry:

```bash
verity pack compare verity.pack.unity \
  --mirror tests/fixtures/official_extension_mirrors/verityspec-pack-unity/pack
```

Use JSON output in CI and release review:

```bash
verity pack compare verity.pack.unity \
  --mirror tests/fixtures/official_extension_mirrors/verityspec-pack-unity/pack \
  --format json
```

The command intentionally does not change source precedence. Built-in pack IDs
remain reserved until a controlled official detach gate exists.

## Acceptance Gate

A future official extension package is not ready to detach from the bundled
wheel unless maintainers can show:

- `verity pack compare <pack-id> --mirror <mirror-path> --format json` passes;
- `verity pack doctor --format json` has no installed-package discovery
  errors for the candidate package;
- `verity pack list --format json` can explain whether the pack is loaded from
  `built-in`, `installed`, or `external` source;
- example workspaces validate with `verity validate`;
- examples pass `verity lint --strict`;
- release-ready examples pass `verity readiness --strict`;
- graph behavior remains stable for reference-heavy packs;
- generator golden output either matches the bundled source or ships an
  explicit migration note;
- rollback instructions restore the bundled pack path without renaming records.

## Non-Goals

This guidance does not:

- detach `verity.pack.unity` or any other bundled pack;
- enable installed packages to shadow built-in pack IDs;
- define the future official registry policy;
- define compatibility metadata enforcement;
- create PyPI packages;
- replace migration or rollback guidance.

Specifically, it does not detach bundled packs and does not allow arbitrary installed packages to shadow built-in pack IDs.

The specialized-pack separation plan remains the governing document for the
larger packaging transition.
