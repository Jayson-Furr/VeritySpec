# VeritySpec v0.44.0 Release Notes

VeritySpec v0.44.0 adds built-in mobile lifecycle and live operations packs for
release, store, privacy/data-safety posture, SDK inventory, monetization,
remote config, rollback, analytics, support, save migration, decommissioning,
data deletion, and archive handling contracts.

## Highlights

- Added built-in `verity.pack.mobile`.
- Added strict schemas for `mobile.app-release`, `mobile.store-listing`,
  `mobile.privacy-policy`, `mobile.apple-privacy-details`,
  `mobile.google-play-data-safety`, `mobile.att-consent`,
  `mobile.sdk-inventory`, `mobile.monetization-posture`,
  `mobile.entitlement`, `mobile.soft-launch`, `mobile.launch-candidate`, and
  `mobile.compatibility-matrix`.
- Added built-in `verity.pack.liveops`.
- Added strict schemas for `liveops.config`, `liveops.remote-config`,
  `liveops.rollback-plan`, `liveops.analytics-taxonomy`,
  `liveops.support-category`, `liveops.save-migration-policy`,
  `liveops.decommission-plan`, `liveops.data-deletion-policy`, and
  `liveops.archive-handling`.
- Added readiness gates and reference rules for mobile and liveops records,
  including engine-neutral Unity, Godot, and Unreal project relationships for
  mobile releases and liveops configs.
- Added executable `examples/mobile` and `examples/liveops` workspaces.
- Added mobile and liveops coverage to cross-pack coverage dashboards,
  compatibility manifests, schema-bundle checks, CI, README command smoke
  tests, pack docs, readiness docs, generator docs, release-checklist coverage,
  and AI-agent commands.
- Kept mobile and liveops claims scoped to product-contract vocabulary. This
  release does not assert legal, privacy-law, app-store, marketplace,
  platform-certification, support-readiness, or archival guarantees.

## Compatibility

- Package version: `0.44.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace format migration is required.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.44.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
