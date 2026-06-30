# Product Surface Pack Boundaries

VeritySpec should add large product surfaces through deliberate packs, not by
expanding the core kernel or creating a broad static catalog. This note defines
the initial boundaries for future GUI, desktop, mobile, and game packs.

`verity.pack.game-core`, `verity.pack.game-assets`, and `verity.pack.unity`
now provide the first narrow built-in game and engine scopes. The remaining
GUI, desktop, mobile, gameplay, content, liveops, evidence, dependency,
portfolio, and broader game scopes should still use this note to define pack
ownership, overlap rules, and readiness expectations before implementation
begins.

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
- Future release, evidence, dependency, and portfolio packs should own their
  own lifecycle concerns instead of being embedded into GUI, desktop, mobile,
  or game packs.

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

## Future Mobile Pack

Proposed pack ID: `verity.pack.mobile`.

The mobile pack should describe mobile application contracts and mobile-specific
platform obligations.

Likely ownership:

- mobile app manifests, app lifecycle states, foreground/background behavior,
  and deep-link contracts
- iOS and Android platform targets, minimum versions, entitlements,
  permissions, and store submission metadata
- device capability requirements such as camera, location, Bluetooth, push
  notifications, biometrics, and offline storage
- mobile release-channel records such as beta, staged rollout, and store
  review gates
- mobile-specific crash, performance, and compatibility evidence references

The mobile pack should not own:

- platform-neutral GUI screen records
- backend API, event, security, observability, accessibility, or compliance
  records
- game mechanics or liveops records, even when a game ships on mobile
- generic deployment infrastructure records

The first mobile schemas should wait until the pack includes store-submission
readiness examples and validates at least one iOS or Android platform target
with explicit permission rationale.

## Game Core, Game Assets, and Future Game Packs

Current pack IDs: `verity.pack.game-core`, `verity.pack.game-assets`,
`verity.pack.unity`.

The game-core pack describes the first narrow game product-contract surface:
game product identity, playable modes, game loops, and prototype scope. It is
not the whole game domain.

The game-assets pack describes the first narrow creative-source surface: GDD
source records, visual identity records, identity images, and concept art. It
links creative sources to game-core records without becoming a full asset
pipeline, content, economy, or engine pack.

The Unity pack describes the first narrow engine-specific implementation
surface: Unity project records, package dependencies, scenes, and build
targets. It does not define generic gameplay, content, liveops, evidence, or
workspace-dependency behavior.

Future broader game packs may use pack IDs such as `verity.pack.game`,
`verity.pack.gameplay`, `verity.pack.content`, or `verity.pack.liveops`.

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
- Game engine, shared library, and cross-workspace dependency records should be
  handled by separate packs or workspace-dependency features.
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
