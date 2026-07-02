# VeritySpec Evidence Report

- Generated: `<generatedAt>`
- VeritySpec: `<verityVersion>`
- Workspace: `examples.evidence`
- Workspace path: `<workspacePath>`
- Spec version: `v0.2.0`

> This report summarizes internal VeritySpec implementation, QA, release, review, playtest, certification, and artifact evidence coverage for product-contract review. The JSON evidence-report output remains the machine-readable contract for CI and downstream tooling. This Markdown report does not make legal, commercial, privacy-law, marketplace, app-store, platform-certification, pricing-approval, support-SLA, or production-readiness claims.

## Summary

| Metric | Count |
|---|---:|
| Evidence records | 10 |
| Missing subjects | 0 |
| Missing artifacts | 0 |
| Failing evidence | 0 |
| Inconclusive evidence | 0 |

## Evidence By Kind

| Kind | Evidence |
|---|---:|
| evidence.artifact | 1 |
| evidence.build | 1 |
| evidence.certification-checklist | 1 |
| evidence.ci-run | 1 |
| evidence.playtest | 1 |
| evidence.qa | 1 |
| evidence.review | 1 |
| evidence.screenshot | 1 |
| evidence.test | 1 |
| evidence.video | 1 |

## Evidence By Lifecycle Status

| Status | Evidence |
|---|---:|
| ready | 10 |

## Evidence By Evidence Status

| Evidence status | Evidence |
|---|---:|
| approved | 1 |
| passing | 4 |
| positive | 1 |
| ready | 3 |
| success | 1 |

## Evidence By Owner

| Owner | Evidence |
|---|---:|
| design | 1 |
| docs | 2 |
| qa | 2 |
| release | 5 |

## Release Gaps

| Gap | Count | Records |
|---|---:|---|
| Missing subjects | 0 | none |
| Missing artifacts | 0 | none |
| Failing evidence | 0 | none |
| Inconclusive evidence | 0 | none |

## Evidence Records

| ID | Kind | Lifecycle status | Evidence status | Owner | Subject | URI | References |
|---|---|---|---|---|---|---|---|
| evidence.artifact.release_manifest | evidence.artifact | ready | ready | release | release.process.evidence_demo (release.process, Evidence Demo Release Process, resolved) | archive/releases/manifest.json | archives: archive.policy.release_artifacts, proves: release.process.evidence_demo |
| evidence.build.release_wheel | evidence.build | ready | passing | release | release.process.evidence_demo (release.process, Evidence Demo Release Process, resolved) | dist/verityspec-0.83.0-py3-none-any.whl | proves: release.process.evidence_demo |
| evidence.certification-checklist.release_candidate | evidence.certification-checklist | ready | passing | release | release.process.evidence_demo (release.process, Evidence Demo Release Process, resolved) | release/checklists/candidate.md | proves: release.process.evidence_demo |
| evidence.ci-run.release_ci | evidence.ci-run | ready | success | release | release.process.evidence_demo (release.process, Evidence Demo Release Process, resolved) | https://github.com/Jason-Furr/verity-spec/actions/runs/28489756302 | proves: release.process.evidence_demo |
| evidence.playtest.prototype_loop | evidence.playtest | ready | positive | design | product.scope.evidence_demo (product.scope, Evidence Demo Scope, resolved) | playtests/prototype-loop.md | proves: product.scope.evidence_demo |
| evidence.qa.release_qa | evidence.qa | ready | passing | qa | release.process.evidence_demo (release.process, Evidence Demo Release Process, resolved) | qa/reports/release-qa.md | proves: release.process.evidence_demo |
| evidence.review.release_review | evidence.review | ready | approved | release | decision.record.release_evidence (decision.record, Release Evidence Is Required, resolved) | https://github.com/Jason-Furr/verity-spec/pull/208 | reviews: decision.record.release_evidence |
| evidence.screenshot.release_dashboard | evidence.screenshot | ready | ready | docs | product.scope.evidence_demo (product.scope, Evidence Demo Scope, resolved) | docs/screenshots/release-dashboard.png | captures: product.scope.evidence_demo |
| evidence.test.release_tests | evidence.test | ready | passing | qa | release.process.evidence_demo (release.process, Evidence Demo Release Process, resolved) | build/evidence/tests.json | proves: release.process.evidence_demo |
| evidence.video.release_walkthrough | evidence.video | ready | ready | docs | product.scope.evidence_demo (product.scope, Evidence Demo Scope, resolved) | docs/videos/release-walkthrough.mp4 | captures: product.scope.evidence_demo |
