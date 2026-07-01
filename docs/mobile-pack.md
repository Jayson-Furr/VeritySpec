# Mobile Pack

`verity.pack.mobile` adds built-in vocabulary for mobile release lifecycle,
store posture, privacy and data-safety evidence references, SDK inventory,
monetization posture, entitlements, soft launches, launch candidates, and
compatibility matrices.

The pack is engine-neutral. Unity, Godot, and Unreal projects can all link to a
mobile release with the same `targetsMobileRelease` relationship when the
product targets mobile platforms. Engine-specific mobile additions should keep
that parity or document why an equivalent does not apply.

This pack does not assert legal, privacy-law, platform-certification,
marketplace, app-store, Apple App Store, or Google Play readiness. Those claims
require downstream review, policy, and evidence outside this built-in
vocabulary.

## Record Kinds

The pack contributes these record kinds:

- `mobile.app-release`
- `mobile.store-listing`
- `mobile.privacy-policy`
- `mobile.apple-privacy-details`
- `mobile.google-play-data-safety`
- `mobile.att-consent`
- `mobile.sdk-inventory`
- `mobile.monetization-posture`
- `mobile.entitlement`
- `mobile.soft-launch`
- `mobile.launch-candidate`
- `mobile.compatibility-matrix`

## Readiness

Mobile readiness gates require owners, descriptions, release/store/privacy
metadata, SDK or monetization inventory where relevant, and graph links for
records that affect release review.

Examples:

- `mobile.app-release` records should link to store listing, privacy,
  SDK-inventory, monetization, launch, compatibility, and liveops records.
- `mobile.store-listing` records should identify target stores and content
  rating status.
- `mobile.privacy-policy`, `mobile.apple-privacy-details`, and
  `mobile.google-play-data-safety` records should capture evidence-oriented
  privacy and data-safety posture without claiming legal sufficiency.
- `mobile.sdk-inventory` records should list SDKs and review posture.
- `mobile.soft-launch` records should define markets, success criteria, and
  telemetry references.
- `mobile.launch-candidate` records should link to the release and privacy or
  readiness records that support candidate review.

Run the executable example:

```bash
verity validate examples/mobile
verity lint examples/mobile --strict
verity readiness examples/mobile --strict
verity graph examples/mobile
verity generate schema-bundle examples/mobile --out build/mobile-schema-bundle.json
```

When mobile records are combined with product-delivery and liveops records,
generate a lifecycle readiness gap report:

```bash
verity generate lifecycle-readiness-report examples/lifecycle-readiness --out build/lifecycle-readiness-report.json
```

The report summarizes implementation-ready, soft-launch, launch-candidate,
remote-config, rollback, support, save-migration, decommission,
data-deletion, and archive-review coverage without asserting store,
marketplace, legal, privacy-law, platform-certification, support, or archival
readiness.

## Reference Rules

The pack defines reference rules for:

- `product`, `game.product`, and `product.scope` to `mobile.app-release` with
  `hasMobileRelease`
- `unity.project`, `godot.project`, and `unreal.project` to
  `mobile.app-release` with `targetsMobileRelease`
- `mobile.app-release` to store listing, privacy policy, Apple privacy details,
  Google Play data safety, ATT consent, SDK inventory, monetization posture,
  entitlement, soft launch, launch candidate, compatibility matrix, and liveops
  config records
- `mobile.launch-candidate` to the release, store, privacy, and readiness
  records it is reviewing

These rules let `verity validate` reject unknown or mismatched mobile lifecycle
edges instead of treating mobile release records as isolated JSON documents.

## Example

The executable example at
[`examples/mobile`](../examples/mobile/verityspec.json) models a mobile game
soft-launch release slice with store, privacy, data-safety, ATT, SDK,
monetization, Remove Ads entitlement, compatibility, launch-candidate, and
liveops links.

The example is included in the workspace compatibility matrix and CI contract.
