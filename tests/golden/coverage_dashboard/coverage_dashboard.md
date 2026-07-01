# VeritySpec Coverage Dashboard

- Generated: `<generatedAt>`
- VeritySpec: `<verityVersion>`
- Workspace: `fixtures.cross_pack_coverage`
- Workspace path: `<workspacePath>`
- Spec version: `v0.2.0`

> This report summarizes internal VeritySpec product-contract coverage for release review. It does not make legal, commercial, privacy-law, platform-certification, marketplace, app-store, store-review, pricing-approval, or support-SLA claims.

## Summary

| Metric | Count |
|---|---:|
| Records | 127 |
| Products | 1 |
| Tracked surfaces | 21 |
| Loaded surface packs | 21 |
| Covered surfaces | 21 |
| Coverage percent | 100.0% |

## Release Gaps

| Gap | Count | Items |
|---|---:|---|
| Missing surface records | 0 | none |
| Loaded packs without surface records | 0 | none |
| Products without surface references | 0 | none |
| Product surface gaps | 0 | none |

## Surface Coverage

| Surface | Pack | Loaded | Records | Product refs | Covered | Relationships |
|---|---|---|---:|---:|---|---|
| Core | verity.core | yes | 2 | 0 | yes | none |
| API | verity.pack.api | yes | 1 | 1 | yes | exposes |
| CLI | verity.pack.cli | yes | 1 | 1 | yes | ships |
| Events | verity.pack.events | yes | 1 | 1 | yes | emits |
| Security | verity.pack.security | yes | 1 | 1 | yes | securedBy |
| Accessibility | verity.pack.accessibility | yes | 1 | 1 | yes | accessibilityCoveredBy |
| Observability | verity.pack.observability | yes | 4 | 1 | yes | observes |
| Compliance | verity.pack.compliance | yes | 1 | 1 | yes | complianceMappedBy |
| Deployment | verity.pack.deployment | yes | 2 | 1 | yes | deploysTo |
| Game Core | verity.pack.game-core | yes | 4 | 1 | yes | describes |
| Game Assets | verity.pack.game-assets | yes | 4 | 1 | yes | hasGameAssets |
| Unity | verity.pack.unity | yes | 12 | 1 | yes | hasUnityProject |
| Godot | verity.pack.godot | yes | 14 | 1 | yes | hasGodotProject |
| Unreal | verity.pack.unreal | yes | 13 | 1 | yes | hasUnrealProject |
| Gameplay | verity.pack.gameplay | yes | 4 | 1 | yes | hasGameplay |
| Content | verity.pack.content | yes | 4 | 1 | yes | hasContentManifest |
| Economy | verity.pack.economy | yes | 5 | 1 | yes | hasEconomy |
| Progression | verity.pack.progression | yes | 5 | 1 | yes | hasProgressionTrack |
| Product Delivery | verity.pack.product-delivery | yes | 17 | 1 | yes | hasProductScope |
| Mobile | verity.pack.mobile | yes | 12 | 1 | yes | hasMobileRelease |
| LiveOps | verity.pack.liveops | yes | 9 | 1 | yes | hasLiveOpsConfig |
| Evidence | verity.pack.evidence | yes | 10 | 1 | yes | hasEvidence |

## Product Surface References

| Product | Status | Owner | Missing surfaces | Surface refs |
|---|---|---|---|---:|
| product.coverage_dashboard | ready | platform | none | 21 |
