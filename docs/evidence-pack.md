# Evidence Pack

`verity.pack.evidence` adds built-in records for concrete implementation,
quality, release, and archival proof. It complements
`product-delivery` `evidence.requirement` records: product-delivery can say
what evidence is required, while this pack records the evidence that exists.

The pack does not assert legal, privacy, marketplace, platform certification,
support, or store-review approval. It only models evidence records that
downstream teams can review.

## Record Kinds

- `evidence.test`: test command, type, result, and evidence URI.
- `evidence.ci-run`: CI provider, run ID, run URL, conclusion, and commit.
- `evidence.build`: build artifact path, artifact type, platform, version, and
  result.
- `evidence.review`: reviewer, review type, decision, timestamp, and review
  URI.
- `evidence.screenshot`: image path, capture timestamp, and purpose.
- `evidence.video`: video path, capture timestamp, purpose, and optional
  duration.
- `evidence.qa`: QA report path, scope, result, and checklist counts.
- `evidence.playtest`: playtest report path, date, participant count, summary,
  and result.
- `evidence.certification-checklist`: platform checklist path and status.
- `evidence.artifact`: retained artifact path, type, hash, and retention
  policy.

## Relationships

The pack declares reference rules for:

- `product` to `evidence.artifact` with `hasEvidence`
- `readiness.profile` and `evidence.requirement` to evidence records
- `release.process` to CI, build, and review evidence
- mobile launch candidates to QA and certification evidence
- liveops save migration policy to test evidence
- progression gates to playtest and QA evidence
- Unity, Godot, and Unreal validation runners to test evidence
- Unity, Godot, and Unreal readiness dashboards to QA evidence
- test evidence to Unity project and scene records, Godot project and scene
  records, and Unreal project and map records
- build evidence to Unity build-target records, Godot export-preset records,
  and Unreal target records
- evidence records to the product, release, decision, archive, progression,
  mobile, and product-delivery records they prove, review, capture, or archive

For blocked or incomplete engine checks, use `evidence.test.result` values such
as `skipped` or `inconclusive` with a normal `proves` reference to the engine
record. The pack does not introduce a separate gap relationship vocabulary for
engine evidence.

## Evidence Report

`verity generate evidence-report` emits a JSON report with:

- workspace and VeritySpec version metadata
- evidence record count
- counts by evidence kind, lifecycle status, owner, and evidence status
- release gaps for missing subjects, missing artifact/URI fields, failing
  evidence, and inconclusive evidence
- per-evidence subject resolution and URI detail

## Commands

```bash
verity validate examples/evidence
verity lint examples/evidence --strict
verity readiness examples/evidence --strict
verity graph examples/evidence
verity generate evidence-report examples/evidence --out build/evidence-report.json
verity generate schema-bundle examples/evidence --out build/evidence-schema-bundle.json
```

The executable example records test, CI, build, review, screenshot, video, QA,
playtest, certification-checklist, and artifact evidence linked to
product-delivery records. The Unity, Godot, and Unreal examples also include
engine-specific test and build evidence records that directly prove their
project, scene or map, and build/export target contracts.
