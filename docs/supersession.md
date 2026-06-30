# PrismSpec to VeritySpec

PrismSpec was the original public prototype for a universal
product-specification repository. Its core idea remains valid: product intent,
interfaces, targets, capabilities, assets, compliance, telemetry, packaging,
and versioning should be describable in a structured, versioned, traceable way.

VeritySpec supersedes PrismSpec by making that idea executable. A VeritySpec
workspace is not only a catalog of records. It is a product contract that can be
validated, linted, checked for release readiness, analyzed as a graph, diffed
across versions, and used to generate artifacts.

The intended public positioning is:

```text
PrismSpec established the initial product-specification vocabulary.
VeritySpec supersedes it with a smaller kernel, a pack-based architecture,
executable validation, readiness gates, graph analysis, diffing, generators,
and migration tooling.
```

