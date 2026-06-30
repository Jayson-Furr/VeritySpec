# Game Assets Pack

`verity.pack.game-assets` adds the first built-in creative-source records for
game workspaces without moving the broader game, engine, liveops, evidence, or
portfolio lifecycle into the core kernel.

## Record Kinds

- `game.gdd-source`: a source design document record for a GDD, pitch, design
  note, or external creative source, including its path, source type, summary,
  revision, and derived-record references.
- `game.visual-identity`: a visual identity contract with tone, art direction,
  style keywords, palette values, and references to identity and concept art.
- `game.identity-image`: an identity image asset record for logo, key art,
  color board, mood board, style frame, or similar brand-defining images.
- `game.concept-art`: a concept art asset record for characters, enemies,
  environments, items, modes, loops, UI concepts, or other creative subjects.

## Relationships

The pack declares these reference relationships:

- `product` `hasGameAssets` `game.visual-identity`
- `game.product` `derivedFrom` `game.gdd-source`
- `game.product` `hasVisualIdentity` `game.visual-identity`
- `game.gdd-source` `derivesRecord` `game.product`
- `game.gdd-source` `derivesRecord` `game.mode`
- `game.gdd-source` `derivesRecord` `game.loop`
- `game.gdd-source` `derivesRecord` `game.prototype-scope`
- `game.visual-identity` `usesIdentityImage` `game.identity-image`
- `game.visual-identity` `usesConceptArt` `game.concept-art`
- `game.concept-art` `supportsMode` `game.mode`
- `game.concept-art` `supportsLoop` `game.loop`

This scope composes with `verity.pack.game-core`: game-core defines early game
product intent, modes, loops, and prototype scope; game-assets links that intent
to GDD and creative-source records.

## Readiness

Strict readiness checks require each ready game-assets record to have enough
metadata for creative review and handoff:

- GDD sources need a path, source type, summary, and at least one derived-record
  reference.
- Visual identities need tone, art direction, at least one style keyword, and
  at least two creative asset references.
- Identity images need path, image type, format, and intended usage.
- Concept art needs path, concept type, subject, format, at least one style tag,
  and at least one supporting reference.

## Commands

```bash
verity validate examples/game-assets
verity lint examples/game-assets --strict
verity readiness examples/game-assets --strict
verity graph examples/game-assets
verity generate schema-bundle examples/game-assets --out build/game-assets-schema-bundle.json
```

The example workspace models the Dream Extraction game concept with one GDD
source, one visual identity, one key-art identity image, and one concept-art
record tied back to the game mode and core loop.
