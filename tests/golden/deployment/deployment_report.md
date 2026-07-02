# VeritySpec Deployment Report

- Generated: `<generatedAt>`
- VeritySpec: `<verityVersion>`
- Workspace: `examples.deployment`
- Workspace path: `<workspacePath>`
- Spec version: `v0.2.0`

> This report summarizes internal VeritySpec deployment-target, runtime, release-policy, and linked evidence coverage for release and operations review. The JSON deployment-report output remains the machine-readable contract for CI and downstream tooling. This Markdown report does not make legal, commercial, privacy-law, marketplace, app-store, platform-certification, pricing-approval, support-SLA, or production-readiness claims.

## Summary

| Metric | Count |
|---|---:|
| Deployment targets | 1 |
| Runtimes | 1 |

## Targets By Environment

| Value | Count |
|---|---:|
| production | 1 |

## Targets By Provider

| Value | Count |
|---|---:|
| aws | 1 |

## Targets By Platform

| Value | Count |
|---|---:|
| kubernetes | 1 |

## Runtimes By Type

| Value | Count |
|---|---:|
| container | 1 |

## Release Gaps

| Gap | Count | Records |
|---|---:|---|
| Targets without runtime | 0 | none |
| Runtimes without targets | 0 | none |
| Production without approval | 0 | none |
| Production without health checks | 0 | none |
| Targets without rollback plan | 0 | none |
| Production without security controls | 0 | none |
| Production without observability | 0 | none |
| Production without compliance mapping | 0 | none |
| Production without release evidence | 0 | none |
| Missing owners | 0 | none |

## Deployment Targets

| ID | Environment | Provider | Platform | Regions | Runtime | Approval | Health check | Rollback | Security | Observability | Compliance | Release evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deployment.target.checkout_production | production | aws | kubernetes | us-east-1, us-west-2 | deployment.runtime.checkout_api (container, python, 3.12) | strategy: rolling; approval required: yes; owner: release-management; change window: business-hours; freeze policy: holiday-freeze | https://checkout.example.com/healthz | docs/ops/checkout-production-rollback.md | security.control.checkout_access (security.control, ready) | observability.dashboard.checkout_delivery (observability.dashboard, ready) | compliance.mapping.checkout_delivery (compliance.mapping, ready) | evidence.ci-run.checkout_release (evidence.ci-run, ready, success), evidence.qa.checkout_release (evidence.qa, ready, passing), evidence.artifact.checkout_release_manifest (evidence.artifact, ready, ready) |

## Runtimes

| ID | Type | Runtime | Version | Artifact | Language | Entrypoint | Dependencies |
|---|---|---|---|---|---|---|---|
| deployment.runtime.checkout_api | container | python | 3.12 | container-image | python | verityspec-checkout-api | postgres, redis |
