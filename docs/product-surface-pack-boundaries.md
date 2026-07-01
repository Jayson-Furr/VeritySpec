# Product Surface Pack Boundaries

VeritySpec should add large product surfaces through deliberate packs, not by
expanding the core kernel or creating a broad static catalog. This note defines
the initial boundaries for future GUI, desktop, lifecycle, and game packs.

`verity.pack.game-core`, `verity.pack.game-assets`, `verity.pack.unity`,
`verity.pack.godot`, `verity.pack.unreal`, `verity.pack.gameplay`,
`verity.pack.content`, `verity.pack.economy`,
`verity.pack.progression`, `verity.pack.product-delivery`,
`verity.pack.mobile`, `verity.pack.liveops`, and `verity.pack.evidence` now
provide the first narrow built-in game, engine, economy, progression,
spec-driven product-delivery, mobile lifecycle, live operations, and evidence
scopes. The remaining GUI, desktop, dependency, portfolio, and broader game
scopes should still use this note to define pack ownership, overlap rules, and
readiness expectations before implementation begins.

## Pack Boundary Rule

Each product-surface pack should own records for one product surface and should
reuse existing cross-cutting packs for concerns that are not unique to that
surface.

Cross-cutting concerns stay outside these surface packs:

- `verity.pack.security` owns security controls, privacy-sensitive control
  evidence, and security release gaps.
- `verity.pack.accessibility` owns accessibility claims, checks, and evidence.
- `verity.pack.observability` owns telemetry, metrics, dashboards, and alerts.
- `verity.pack.compliance` owns compliance mappings and compliance matrices.
- `verity.pack.deployment` owns generic runtime, hosting, release environment,
  rollback, and deployment report concerns.
- The evidence pack owns concrete proof records. Future release, dependency,
  and portfolio packs should own their own lifecycle concerns instead of being
  embedded into GUI, desktop, mobile, or game packs.

Surface packs may reference cross-cutting records, but they should not duplicate
their schemas.

## Future GUI Pack

Proposed pack ID: `verity.pack.gui`.

The GUI pack should describe user-interface product contracts that are not tied
to one runtime platform.

Likely ownership:

- screens, views, routes, dialogs, panels, and navigation flows
- design-system component contracts and reusable UI patterns
- user actions, UI states, empty states, loading states, and error states
- UI content requirements, localization key inventory, and copy ownership
- UI-to-product relationships, such as which product feature a screen supports

The GUI pack should not own:

- native desktop shell behavior, tray integration, installers, or OS-level
  menus
- mobile store metadata, device permission declarations, or app lifecycle
  behavior
- game mechanics, economy, progression, content taxonomies, or liveops events
- accessibility evidence or accessibility conformance claims

The first GUI schemas should wait until the pack can include executable
examples for at least one product workflow and at least one useful generator or
report, such as a UI inventory report or screen-reference document.

## Future Desktop Pack

Proposed pack ID: `verity.pack.desktop`.

The desktop pack should describe native desktop application contracts and
desktop-specific runtime integration.

Likely ownership:

- desktop application shells, windows, menus, command palettes, and tray
  integration
- desktop install, update, file association, protocol handler, and entitlement
  contracts
- operating-system support matrices for macOS, Windows, and Linux
- local filesystem, clipboard, notification, and background-process behavior
- desktop packaging and distribution requirements when they are specific to
  native desktop delivery

The desktop pack should not own:

- platform-neutral GUI screens or design-system components
- API, CLI, or event contracts exposed by the desktop app
- mobile lifecycle, app-store, or device permission records
- deployment infrastructure records that should belong to a deployment pack

The first desktop schemas should wait until the pack has examples that validate
at least one native application shell, one supported operating-system target,
and one readiness gate for release-impacting desktop metadata.

## Mobile Pack

Current pack ID: `verity.pack.mobile`.

The mobile pack describes the first narrow mobile lifecycle surface: app
releases, store listings, privacy policy evidence references, Apple privacy
details, Google Play Data Safety posture, ATT consent, SDK inventory,
monetization posture, entitlements, soft launches, launch candidates, and
compatibility matrices.

It owns:

- app release records and release-track posture
- store listing metadata posture
- privacy policy, Apple privacy details, Google Play Data Safety, and ATT
  consent posture records
- SDK inventory, monetization posture, and entitlement records
- soft-launch, launch-candidate, and compatibility matrix records
- engine-neutral links from Unity, Godot, and Unreal projects to mobile
  releases where those products target mobile platforms

The mobile pack should not own:

- platform-neutral GUI screen records
- backend API, event, security, observability, accessibility, or compliance
  records
- game mechanics or liveops records, even when a game ships on mobile
- generic deployment infrastructure records
- legal, privacy-law, app-store, platform-certification, marketplace, or
  pricing-approval guarantees

The first mobile schemas intentionally model reviewable product-contract
posture and evidence references. Downstream teams remain responsible for legal,
privacy, store, platform, marketplace, and pricing approvals.

## LiveOps Pack

Current pack ID: `verity.pack.liveops`.

The liveops pack describes the first narrow live operations lifecycle surface:
liveops configuration, remote config bounds, rollback plans, analytics
taxonomy, support categories, save migration policy, decommissioning, data
deletion posture, and archive handling.

It owns:

- liveops config and remote-config contract records
- rollback plan and bounded deployment posture records
- analytics taxonomy and support category records
- save-migration policy records
- decommission, data-deletion, and archive-handling records
- engine-neutral links from Unity, Godot, and Unreal projects to liveops
  configs where those products use live operations or remote configuration

The liveops pack should not own:

- generic gameplay, content, economy, platform-store, or deployment records
- security, privacy-law, compliance, observability, evidence, or support
  approval claims
- workspace-dependency semantics or portfolio impact analysis
- legal, platform, marketplace, store-review, support-readiness, or archival
  guarantees

The first liveops schemas intentionally model reviewable operational posture
and lifecycle links. Downstream teams remain responsible for operational,
support, legal, privacy, store, platform, marketplace, and archive approvals.

## Game Core, Game Assets, Engine, Gameplay, Content, Economy, Product Delivery, and Future Game Packs

Current pack IDs: `verity.pack.game-core`, `verity.pack.game-assets`,
`verity.pack.unity`, `verity.pack.godot`, `verity.pack.unreal`,
`verity.pack.gameplay`, `verity.pack.content`, `verity.pack.economy`,
`verity.pack.product-delivery`, `verity.pack.mobile`, and
`verity.pack.liveops`.

The game-core pack describes the first narrow game product-contract surface:
game product identity, playable modes, game loops, and prototype scope. It is
not the whole game domain.

The game-assets pack describes the first narrow creative-source surface: GDD
source records, visual identity records, identity images, and concept art. It
links creative sources to game-core records without becoming a full asset
pipeline, content, economy, or engine pack.

The Unity pack describes the engine-specific game implementation and tooling
surface: Unity project records, package dependencies, packages, shared
libraries, prefabs, assembly definitions, scanners, validation runners,
readiness dashboards, agent-context exporters, scenes, and build targets. It
does not define generic gameplay, content, economy, progression, liveops,
evidence, or workspace-dependency behavior.

The Godot pack describes the engine-specific game implementation and tooling
surface: Godot project records, addons, shared libraries, scenes, node
contracts, resources, scripts, autoloads, input actions, export presets,
scanners, validation runners, readiness dashboards, and agent-context
exporters. It does not define generic gameplay, content, economy, progression,
liveops, evidence, or workspace-dependency behavior.

The Unreal pack describes the engine-specific game implementation and tooling
surface: Unreal project records, plugins, modules, targets, maps, Blueprints,
data assets, gameplay tags, input actions, scanners, validation runners,
readiness dashboards, and agent-context exporters. It supports games made with
Unreal without defining generic gameplay, content, economy, progression,
liveops, evidence, or workspace-dependency behavior.

The gameplay pack describes the first narrow playable-system surface: mechanics,
abilities, rules, and encounters. It does not define content manifests,
economy, progression, liveops, evidence, or engine-specific implementation
records.

The content pack describes the first narrow content surface: content items,
levels, loot tables, and content manifests. It composes with gameplay and Unity
records without becoming an economy, progression, liveops, or asset-pipeline
pack.

The economy pack describes the first narrow economy surface: currencies,
sources, sinks, rewards, and offers. It composes with gameplay and content
records without becoming a progression, liveops, pricing approval, or platform
store pack.

The progression pack describes the first narrow game progression surface: XP
models, levels, unlocks, tracks, and gates. It composes with gameplay, content,
economy, liveops, and engine records without owning those surfaces.

The product-delivery pack describes the first narrow spec-driven repository
delivery surface: product scope, commercial posture, project-management model,
decision records, readiness profiles, evidence requirements, release process,
operations, support, maintenance, archive, decommission, scanner, generator,
validation-runner, editor-surface, and agent-context exporter records. It
does not provide legal, privacy-law, marketplace, platform-certification,
mobile-store, liveops, or pricing-approval guarantees.

The evidence pack describes concrete proof records: tests, CI runs, builds,
reviews, screenshots, videos, QA reports, playtests, certification checklists,
and retained artifacts. Product-delivery owns evidence requirements; evidence
owns the proof records that can satisfy those requirements.

The mobile and liveops packs provide engine-neutral lifecycle and operations
records that can be referenced by game and engine workspaces. They are not
Unity-specific; when Unity projects can link to mobile releases or liveops
configs, Godot and Unreal projects should have equivalent relationship support
where the concept applies.

Future broader game packs may use pack IDs such as `verity.pack.game`,
`verity.pack.quest`, or other domain-specific game packs.

Future game packs should describe game product contracts, especially the bridge
between game design intent, implementation scope, QA, telemetry, liveops, and
release planning, without duplicating game-core records unless the schema
evolution is explicit.

Likely ownership:

- game identity, genre, target audience, player fantasy, and source GDD links
- game modes, loops, systems, mechanics, content taxonomies, levels, quests,
  encounters, progression, economy, and monetization records
- concept art, identity art, asset provenance, and creative-source references
- prototype, vertical-slice, production, release, liveops, maintenance,
  decommissioning, and archive readiness profiles
- game-specific feature, content, balance, and liveops impact relationships

The game pack should not own:

- Unity, Unreal, Godot, or engine-specific implementation records
- generic GUI screen records, except as references to GUI records
- security, accessibility, observability, compliance, evidence, release,
  dependency, or portfolio records that belong in dedicated packs
- shared-library workspace dependency semantics

Additional game schemas should start from a narrow proposal that chooses the
next game scope. A minimum future scope should include examples, readiness
gates, graph checks, and a generator or report that is useful for game
development rather than a broad catalog of game concepts.

## Relationship Model

These packs should compose through references:

- GUI records can be used by desktop, mobile, web, and game products.
- Desktop and mobile records can reference GUI records for screens and flows.
- Game records can reference GUI records for player-facing surfaces and mobile
  or desktop records for platform delivery.
- Game engine and shared-library records for games made with Unity, Godot,
  Unreal, or another engine should be handled by engine packs;
  cross-workspace dependency records should be handled by workspace-dependency
  features.
- Readiness profiles should aggregate cross-cutting evidence instead of copying
  the evidence model into every surface pack.

This keeps VeritySpec from making one large pack that tries to model every
runtime, interface, and lifecycle concern at once.

## First-Schema Gate

Before any of these packs adds its first schemas, the sprint should include:

- a GitHub issue and milestone that names the exact first scope
- a pack proposal that identifies record kinds, ownership boundaries,
  references, readiness gates, examples, and generator or report output
- strict JSON Schemas using the shared record envelope
- positive examples and negative fixtures
- library and CLI tests for validation, lint, readiness, and generation where
  relevant
- public docs linked from `README.md` and `docs/packs.md`
- changelog and roadmap updates
- a compatibility statement for future schema evolution

If the first useful behavior is still unclear, the project should add another
design note or fixture before adding schemas.
