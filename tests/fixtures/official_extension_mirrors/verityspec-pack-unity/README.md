# Unity Official-Extension Mirror Fixture

This fixture mirrors the bundled `verity.pack.unity` pack as a candidate
layout for a future `verityspec-pack-unity` Python distribution.

It is not a detached package. The manifest keeps the existing
`verity.pack.unity` pack ID so `verity pack compare` can verify that a future
official extension package preserves the bundled contract before any detach
gate exists.

Run:

```bash
verity pack compare verity.pack.unity --mirror tests/fixtures/official_extension_mirrors/verityspec-pack-unity/pack --format json
```
