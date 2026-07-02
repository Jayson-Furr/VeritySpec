# Generators

Generators turn a valid workspace into implementation or documentation
artifacts.

```bash
verity generate openapi examples/api-service --out build/openapi.json
verity generate asyncapi examples/events --out build/asyncapi.json
verity generate cli-reference examples/cli-tool --out build/cli-reference.md
verity generate typescript examples/basic --out build/types.ts
verity generate python-models examples/basic --out build/models.py
verity generate schema-bundle examples/basic --out build/schema-bundle.json
verity generate validation-report examples/basic --out build/validation-report.json
verity generate validation-report examples/basic --generated-at 2026-01-02T03:04:05Z --out build/validation-report.json
verity generate security-report examples/security --out build/security-report.json
verity generate security-report examples/security --format markdown --out build/security-report.md
verity generate observability-report examples/observability --out build/observability-report.json
verity generate accessibility-report examples/accessibility --out build/accessibility-report.json
verity generate compliance-matrix examples/compliance --out build/compliance-matrix.json
verity generate deployment-report examples/deployment --out build/deployment-report.json
verity generate evidence-report examples/evidence --out build/evidence-report.json
verity generate lifecycle-readiness-report examples/lifecycle-readiness --out build/lifecycle-readiness-report.json
verity generate schema-bundle examples/game-core --out build/game-core-schema-bundle.json
verity generate schema-bundle examples/game-assets --out build/game-assets-schema-bundle.json
verity generate schema-bundle examples/unity --out build/unity-schema-bundle.json
verity generate schema-bundle examples/godot --out build/godot-schema-bundle.json
verity generate schema-bundle examples/unreal --out build/unreal-schema-bundle.json
verity generate schema-bundle examples/gameplay --out build/gameplay-schema-bundle.json
verity generate schema-bundle examples/content --out build/content-schema-bundle.json
verity generate schema-bundle examples/economy --out build/economy-schema-bundle.json
verity generate schema-bundle examples/progression --out build/progression-schema-bundle.json
verity generate schema-bundle examples/product-delivery --out build/product-delivery-schema-bundle.json
verity generate schema-bundle examples/mobile --out build/mobile-schema-bundle.json
verity generate schema-bundle examples/liveops --out build/liveops-schema-bundle.json
verity generate schema-bundle examples/evidence --out build/evidence-schema-bundle.json
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --out build/coverage-dashboard.json
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --format markdown --out build/coverage-dashboard.md
verity generate pack-capability-index tests/fixtures/custom_pack_workspace --out build/pack-capability-index.json
verity generate product-impact tests/fixtures/product_impact/baseline tests/fixtures/product_impact/current --out build/product-impact.json
verity generate agent-context examples/product-delivery --record agent-context.exporter.implementation_bundle --format markdown --out build/agent-context.md
verity generate decision-index examples/product-delivery --out build/decision-index.json
verity generate decision-index examples/product-delivery --format markdown --out build/decision-index.md
verity generate roadmap-report . --out build/roadmap-report.json
verity generate roadmap-report . --format markdown --out build/roadmap-report.md
verity generate issue-code-catalog --out build/issue-code-catalog.json
verity generate issue-code-catalog --format markdown --out build/issue-code-catalog.md
verity generate schema-bundle examples/accessibility --out build/accessibility-schema-bundle.json
verity generate schema-bundle examples/compliance --out build/compliance-schema-bundle.json
verity generate typescript tests/fixtures/generator_maturity --out build/generator-maturity.ts
verity generate python-models tests/fixtures/generator_maturity --out build/generator-maturity.py
```

Packs advertise supported generators in `pack.json`. The preferred declaration
is structured metadata with `id`, `name`, `description`, `artifactType`,
`outputFormats`, and `recordKinds`; legacy string declarations remain valid for
older external packs. `verity pack list --format json` exposes both the
normalized generator ID list and `generatorMetadata`.

Most generators run validation first and fail if the product contract has
errors. `validation-report` is special: it always writes the report, then exits
with the validation result. `product-impact` also writes the report before
returning the validation result so release reviewers can inspect missing
references and graph impact while fixing contract errors.

Validation reports include:

- Generation timestamp
- VeritySpec CLI version
- Workspace path
- Loaded pack versions
- Known record kinds
- Issue summary and full issue list, including formatted issue locations and
  structured `locationDetails` when available

JSON report generators support `--generated-at <ISO datetime>` for
deterministic fixture generation. The value is written directly to
`generatedAt` after ISO 8601 validation. When omitted, VeritySpec writes the
current UTC timestamp.

Security reports include:

- Workspace and VeritySpec version metadata
- Security-control count
- Control counts by coverage and risk level
- Verified-control count
- Critical unverified control IDs
- Release gaps for critical unverified controls, stale evidence, and missing
  verification dates
- Per-control owner, category, objective, verification evidence, and target records
- Optional Markdown output for maintainers who need a human-readable
  release-review artifact

The JSON security-report output remains the machine-readable contract for CI
and downstream tooling. The Markdown output is a derived internal review
artifact and does not make legal, compliance, privacy-law,
security-certification, penetration-test, marketplace, app-store,
platform-certification, pricing-approval, support-SLA, or production-readiness
claims.

Accessibility reports include:

- Workspace and VeritySpec version metadata
- Accessibility-claim count
- Claim counts by owner, standard, level, impact, and coverage
- Verified-claim count
- Release gaps for critical unverified claims, claims without targets, missing
  owners, and missing verification dates
- Per-claim owner, criterion, user need, surface, verification evidence,
  assistive technologies, acceptance criteria, and target records

Compliance matrices include:

- Workspace and VeritySpec version metadata
- Compliance-mapping count
- Mapping counts by owner, framework, requirement, mapping type, and coverage
- Verified-mapping count
- Release gaps for missing targets, missing evidence, reviewed-but-unverified
  mappings, missing mapping owners, and targets without owners
- Per-mapping framework metadata, verification state, mapped targets, and
  grouped security, accessibility, and observability evidence

Evidence reports include:

- Workspace and VeritySpec version metadata
- Evidence counts by kind, lifecycle status, owner, and evidence status
- Release gaps for missing subjects, missing artifact or URI fields, failing
  evidence, and inconclusive evidence
- Per-evidence subject resolution, URI, and reference detail

Lifecycle readiness reports include:

- Workspace and VeritySpec version metadata
- Loaded lifecycle pack IDs for product-delivery, mobile, and liveops records
- Product-delivery, mobile, and liveops surface coverage
- Stage coverage for implementation-ready, soft-launch, launch-candidate,
  remote-config, rollback, support, save-migration, decommission,
  data-deletion, and archive-review summaries
- Gap entries for missing record kinds, non-ready records, and missing owners
- Claim boundaries stating that the report does not assert commercial, legal,
  privacy-law, marketplace, app-store, platform-certification, live-service,
  support, or archival readiness

Deployment reports include:

- Workspace and VeritySpec version metadata
- Runtime and deployment-target counts
- Target counts by environment, provider, and platform
- Runtime counts by runtime type
- Release gaps for missing runtime links, production approval, production
  health checks, rollback plans, and owners
- Per-runtime and per-target release-review detail

Coverage dashboards include:

- Workspace and VeritySpec version metadata
- Loaded pack IDs and total product-contract record count
- Tracked product-surface coverage for API, CLI, events, security,
  accessibility, observability, compliance, deployment, game-core, game-assets,
  Unity, Godot, Unreal, gameplay, content, economy, progression,
  product-delivery, mobile, liveops, and evidence records
- Counts by product surface and record kind
- Release gaps for missing surface records, loaded surface packs without
  records, products without surface references, and product-specific missing
  surface references
- Per-surface records and product relationship targets for release review
- Optional Markdown output for maintainers who need a human-readable
  release-review artifact

The JSON coverage-dashboard output remains the machine-readable contract for
CI and downstream tooling. The Markdown output is a derived internal review
artifact and does not make legal, commercial, privacy-law,
platform-certification, marketplace, app-store, store-review, pricing-approval,
or support-SLA claims.

Pack capability indexes include:

- Workspace and VeritySpec version metadata
- Requested pack IDs, local `packPaths`, and loaded pack IDs
- Pack counts split by built-in, installed, and external source
- Schema, readiness gate, conditional readiness rule, reference rule, and
  generator declaration counts
- Per-kind schema ownership and schema file paths
- Per-gate required fields, `minItems`, conditional rules, and owning pack
- Per-reference-rule source kind, relationship, target kind, and owning pack
- Generator capability indexes that deduplicate generator IDs across packs
- Per-pack details for source type, path, schemas, readiness gates, reference
  rules, and normalized generator metadata

Product-impact reports include:

- Baseline and current workspace metadata
- The same structural diff summary returned by `verity diff`
- Changed, added, and removed records expanded through the reference graph
- Upstream dependents and downstream dependencies for each changed record
- A deduplicated impacted-record list for release reviewers
- Missing references in the baseline and current graphs
- Release-review risk level and focus areas based on breaking changes,
  removed records, impacted records, and missing references

`product-impact` compares two workspace paths:

```bash
verity generate product-impact previous-workspace current-workspace --out build/product-impact.json
```

Agent-context artifacts include:

- Workspace identity, VeritySpec version, workspace format, and selected
  exporter target
- Target exporter metadata, output path, included record kinds, privacy policy,
  and redaction policy
- Relevant product-contract records selected from the exporter, declared
  included kinds, and connected graph records
- Graph links between selected records
- Generated artifacts named by the exporter
- Deprecated or removed selected records
- Safety boundaries stating that generated context does not replace
  `AGENTS.md`, tests, readiness checks, or evidence records
- Verification commands for validation, linting, readiness, graph review, and
  regenerating the agent-context Markdown artifact

`agent-context` requires `--record` and currently supports Markdown output
only. The target record must be `agent-context.exporter`,
`unity.agent-context-exporter`, `godot.agent-context-exporter`, or
`unreal.agent-context-exporter`. VeritySpec validates the workspace before
generation and fails on validation errors instead of silently producing stale
or incomplete handoff context.

```bash
verity generate agent-context examples/product-delivery --record agent-context.exporter.implementation_bundle --format markdown --out build/agent-context.md
```

JSON output remains future work until the handoff contract stabilizes enough
for downstream tooling and CI integrations.

Decision indexes include:

- Workspace and VeritySpec version metadata
- Product-delivery `decision.record` count
- Decision counts by decision status, record lifecycle status, decision type,
  and owner
- Index gaps for accepted decisions without `decidedAt`, decisions with no
  graph links, proposed decisions, and superseded decisions
- Per-decision summaries with owner, type, status, decided date, decision text,
  rationale, references, supersession metadata, and graph-link counts
- Graph links where a decision record is the source or target
- Optional Markdown output for ADR and governance review

The JSON decision-index output is the machine-readable contract. The Markdown
output is a derived internal review artifact. Neither output approves
decisions, replaces ADR prose, or makes legal, commercial, privacy-law,
marketplace, platform-certification, support-SLA, or
implementation-readiness claims.

```bash
verity generate decision-index examples/product-delivery --out build/decision-index.json
verity generate decision-index examples/product-delivery --format markdown --out build/decision-index.md
```

Roadmap reports include:

- Roadmap path and VeritySpec version metadata
- Release milestone sections and their sprint rows
- Counts for released milestones, active milestones, completed sprints, and
  in-progress sprints
- The latest released milestone and currently active milestones
- The Next 20 roadmap planning points used for project governance
- Optional human-readable Markdown output for maintainer release-governance
  reviews

`roadmap-report` reads a repository directory containing `ROADMAP.md` or a
direct path to a roadmap file. It does not require the path to be a VeritySpec
workspace.

```bash
verity generate roadmap-report . --out build/roadmap-report.json
verity generate roadmap-report . --format markdown --out build/roadmap-report.md
```

Issue-code catalogs include:

- VeritySpec version and generation timestamp metadata
- Known issue codes from the canonical `verity explain` metadata
- Per-code category, title, severity, description, and resolution fields
- Summary counts by severity and category for docs sites and CI integrations

`issue-code-catalog` does not require a workspace path. JSON remains the
machine-readable contract; Markdown is intended for documentation sites,
release review, and human-readable issue-code references.

```bash
verity generate issue-code-catalog --out build/issue-code-catalog.json
verity generate issue-code-catalog --format markdown --out build/issue-code-catalog.md
```

## Current Guarantees

OpenAPI output includes:

- Product title, version, and description in `info`
- Component schemas from `schema.object` records
- Request and response schema references where records declare them
- Inferred path parameters from templated paths such as `/users/{userId}`
- Explicit endpoint parameters for path, query, header, and cookie locations
- Operation tags, VeritySpec IDs, owners, statuses, and deprecation metadata

AsyncAPI output includes:

- Product title, version, and description in `info`
- Component schemas and message components
- Message IDs, channel subscriptions, payload references, and VeritySpec metadata

Security report output includes:

- `security.control` records from workspaces that load `verity.pack.security`
- Verification status based on `coverage`, `verification.method`, and
  `verification.evidence`
- Release-gap summaries for critical unverified controls, stale evidence based
  on `verification.reviewCadenceDays`, and missing `verification.lastVerified`
  dates
- Target records from explicit `appliesTo` references

The `examples/security` security report JSON and Markdown shapes are covered
by committed golden fixtures. Tests normalize only the dynamic timestamp,
absolute workspace path, and package version before comparing generated report
output.

Accessibility report output includes:

- `accessibility.claim` records from workspaces that load
  `verity.pack.accessibility`
- Verification status based on `coverage`, `verification.method`, and
  `verification.evidence`
- Target records from explicit `appliesTo` references

Compliance matrix output includes:

- `compliance.mapping` records from workspaces that load
  `verity.pack.compliance`
- Verification status based on `verification.method` and
  `verification.evidence`
- Target records from explicit `covers` references
- Evidence groups for linked `security.control`, `accessibility.claim`, and
  `observability.*` records

Deployment report output includes:

- `deployment.runtime` and `deployment.target` records from workspaces that
  load `verity.pack.deployment`
- Runtime links from target `runtimeRef` fields
- Linked security controls, observability dashboards, compliance mappings, and
  release evidence records from deployment targets
- Release gap summaries for production controls, target ownership, and missing
  release evidence links

Coverage dashboard output includes:

- Product-surface records from all currently supported built-in packs
- Product-level references through `exposes`, `ships`, `emits`, `securedBy`,
  `accessibilityCoveredBy`, `observes`, `complianceMappedBy`, `deploysTo`,
  `describes`, `hasGameAssets`, `hasUnityProject`, `hasGodotProject`,
  `hasUnrealProject`, `hasGameplay`, `hasContentManifest`, `hasEconomy`,
  `hasProductScope`, `hasMobileRelease`, and `hasLiveOpsConfig`
- Summary coverage percentages based on the supported non-core product
  surfaces
- Golden fixture coverage through `tests/fixtures/cross_pack_coverage`

Pack capability index output includes:

- Built-in, installed, and local external pack summaries from the loaded pack
  registry
- Schema, readiness, reference-rule, and generator capability indexes
- Legacy external pack generator declarations normalized alongside structured
  generator metadata
- Golden fixture coverage through `tests/fixtures/custom_pack_workspace`

Product-impact output includes:

- `oldWorkspace` and `newWorkspace` metadata
- `diff` details for changed packs and records
- `changedRecords` entries with `upstream` and `downstream` graph expansion
- `impactedRecords` for review assignment and release notes triage
- `missingReferences` for graph integrity review

TypeScript and Python model generators support:

- `$ref` values that point at `#/components/schemas/...`
- Arrays
- String, number, integer, boolean, and object types
- String and scalar enums
- Nullable fields
- Optional fields
- Inline nested object shapes for TypeScript
- Inline nested dataclasses for Python object properties
- Inline nested dataclasses for Python array item objects
- Field descriptions in generated comments

OpenAPI, TypeScript, and Python output for `tests/fixtures/generator_maturity`
is covered by golden-file tests. The `examples/security` security report,
`examples/observability` observability report and schema bundle, deployment
report, evidence report, lifecycle readiness report, cross-pack coverage
dashboard, pack capability index, and product-impact report are also covered
by committed golden fixtures. Game-core, game-assets, Unity, Godot, Unreal,
gameplay, content, economy,
progression, product-delivery, mobile, liveops, and evidence schema-bundle
smoke checks cover bundled schema generation for the built-in game, engine,
progression, delivery, mobile, liveops, and evidence packs.

When generator behavior intentionally changes, follow the
[fixture refresh guide](fixture-refresh.md). It documents deterministic
`--generated-at` usage, the committed golden fixture locations, placeholder
normalization, and intentional output drift review before updating
`tests/golden`.

Known limits:

- Generators do not yet emit client/server stubs.
