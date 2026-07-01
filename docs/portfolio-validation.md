# Portfolio-Level Validation Foundation

VeritySpec should eventually validate and report on groups of related
workspaces, not only one workspace at a time. This note defines the first
portfolio-level validation boundary for multi-workspace product, service,
library, and game portfolios before any aggregate report, dependency resolver,
lockfile, workspace-format change, or portfolio CLI command is implemented.
This is explicitly about multi-workspace product, service, library, and game portfolios.

No schema changes are introduced by this design note. The first implementation
work should stay local-only, deterministic, and based on existing workspace,
pack, validation, readiness, graph, and example behavior.

## Goal

Portfolio-level validation should help maintainers answer questions about a
set of related VeritySpec workspaces:

- Which workspaces are present, and what type of product contract does each
  represent?
- Which workspaces validate, lint, and pass readiness independently?
- Which integration workspaces prove shared-library or shared-engine
  relationships before first-class cross-workspace dependencies exist?
- Which workspaces are missing readiness, evidence, release, support,
  maintenance, archive, or decommission coverage?
- Which records or workspaces may be affected when a shared library, engine
  toolkit, event contract, design system, or platform service changes?

The goal is not a second validation system. A portfolio check should orchestrate
normal VeritySpec checks, preserve their issue codes, and summarize the
portfolio-level shape around them.

## Workspace Types

A portfolio may include several workspace shapes:

- Product workspaces for applications, tools, services, CLIs, APIs, or
  commercial products.
- Service workspaces for backend services, worker systems, data pipelines, and
  operational contracts.
- Library workspaces for shared SDKs, packages, runtime libraries, design
  systems, event contracts, and platform contracts.
- Game workspaces for Unity, Godot, Unreal, and engine-neutral game contracts.
- Engine-toolkit workspaces such as `VeritySpec.Unity`,
  `VeritySpec.Godot`, and `VeritySpec.Unreal`.
- Shared engine library workspaces for save systems, telemetry clients,
  liveops config loaders, localization helpers, editor tooling, scanners, and
  validation runners.
- Integration workspaces that combine one product or game with one or more
  shared library workspaces as a transitional validation pattern.
- Portfolio workspaces that summarize the inventory, ownership, readiness
  posture, and reporting expectations for the collection.

## Boundary

Portfolio-level validation should compose existing capabilities:

- `verity validate` remains the structural and semantic record check for one
  workspace.
- `verity lint --strict` remains the strict documentation, lifecycle, and graph
  hygiene check for one workspace.
- `verity readiness --strict` remains the readiness-gate check for one
  workspace.
- `verity graph` remains the record graph view for one workspace.
- Future portfolio reports may run those checks across many workspaces and
  summarize the results.

A portfolio check should not hide the original workspace issues. It should keep
stable issue codes, workspace paths, record IDs, and severity so CI and
maintainers can trace failures back to the underlying contract.

## Transitional Relationship Model

First-class cross-workspace dependencies are not implemented yet. Until they
are, portfolio validation should use explicit local patterns:

- integration workspaces for validating game-plus-shared-library or
  service-plus-shared-contract contexts
- portfolio workspaces for declaring the review scope and reporting posture
- local examples or fixtures for proving deterministic report behavior
- explicit exported-record and dependency-alias examples in fixtures before
  any resolver behavior ships

This keeps the current boundary honest. A portfolio workspace can describe the
collection, but it does not prove dependency resolution unless the relevant
records are loaded into an integration workspace or a future dependency-aware
validator.

## Engine Portfolio Pattern

Engine portfolios should keep engine-specific records in engine packs and
cross-cutting product delivery records in shared packs:

- `verity.pack.unity`, `verity.pack.godot`, and `verity.pack.unreal` describe
  engine-specific project, scene, package, plugin, tooling, scanner,
  validation-runner, readiness-dashboard, and agent-context exporter records.
- `verity.pack.game-core` and `verity.pack.game-assets` describe game identity,
  loops, modes, prototype scope, GDD sources, visual identity, identity images,
  and concept art.
- `verity.pack.product-delivery` describes repository delivery posture,
  project-management model, decisions, readiness profiles, evidence
  requirements, release process, support, maintenance, archive,
  decommissioning, scanners, generators, editor surfaces, validation runners,
  and agent-context exporters.
- `verity.pack.evidence`, `verity.pack.mobile`, and `verity.pack.liveops`
  describe implementation proof, mobile lifecycle posture, liveops, remote
  config, rollback, support categories, save migration, decommissioning, data
  deletion, and archive handling.

Unity additions should have Godot and Unreal equivalents where the concept
applies. Portfolio examples should show the three engines side by side when the
intent is engine-neutral.

## Portfolio Report Shape

A future aggregate report should be deterministic and reviewable. Useful
sections include:

- workspace inventory
- workspace type and owner
- pack inventory
- validation status
- lint status
- readiness status
- graph status
- dependency or integration-workspace status
- missing evidence requirements
- deprecated or removed record usage
- impact warnings for shared workspaces
- generated-artifact refresh needs
- agent-context refresh needs
- follow-up issue recommendations

The first report implementation should prefer JSON before Markdown so CI can
consume a stable contract. Markdown can follow once the JSON shape has settled.

## Non-Claims

Portfolio records and reports describe product-contract posture. They do not
make commercial, legal, privacy-law, marketplace, platform-certification,
store-review, pricing-approval, app-store-approval, or support-SLA guarantees.

Evidence records may show that reviewable artifacts exist. They do not prove external approval
unless a downstream organization records and owns that proof.

## First-Implementation Gate

The first implementation sprint after this design note should include:

- local-only portfolio or integration fixtures
- at least two workspace entries in the portfolio scenario
- deterministic validation of each workspace included in the scenario
- exported-record and dependency-alias fixture guidance before resolver
  behavior is added
- README and docs links that keep the pattern discoverable
- tests that run the example through validate, lint, readiness, and graph
- no remote registry, Git authentication, transitive dependency policy,
  lockfile enforcement, or aggregate-report command unless those are
  separately designed and tested

The first implementation should fail loudly on ambiguous scope. It should not
silently infer portfolio membership from unrelated directories.

The first local engine portfolio compatibility fixture now lives at
`tests/fixtures/engine_portfolio/portfolio/verityspec.json`. It shows Unity,
Godot, Unreal, and a shared exported game-core workspace side by side using the
`sharedGame` dependency alias. See
[engine portfolio compatibility fixtures](engine-portfolio-compatibility.md)
for the fixture boundary and local check commands.
