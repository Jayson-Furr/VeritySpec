# VeritySpec Security Report

- Generated: `<generatedAt>`
- VeritySpec: `<verityVersion>`
- Workspace: `examples.security`
- Workspace path: `<workspacePath>`
- Spec version: `v0.2.0`

> This report summarizes internal VeritySpec security-control coverage for release review. The JSON security-report output remains the machine-readable contract for CI and downstream tooling. This Markdown report does not make legal, compliance, privacy-law, security-certification, penetration-test, marketplace, app-store, platform-certification, pricing-approval, support-SLA, or production-readiness claims.

## Summary

| Metric | Count |
|---|---:|
| Security controls | 1 |
| Verified controls | 1 |
| Critical unverified controls | 0 |
| Stale evidence records | 0 |
| Missing verification dates | 0 |

## Coverage

| Coverage | Controls |
|---|---:|
| verified | 1 |

## Risk Levels

| Risk level | Controls |
|---|---:|
| high | 1 |

## Release Gaps

| Gap | Count | Records |
|---|---:|---|
| Critical unverified controls | 0 | none |
| Stale evidence | 0 | none |
| Missing verification dates | 0 | none |

## Security Controls

| ID | Name | Status | Owner | Risk | Coverage | Verified | Verification | Targets |
|---|---|---|---|---|---|---|---|---|
| security.control.account_access | Account Access Control | ready | platform-security | high | verified | yes | method: automated-test; evidence: tests/security/test_account_access.py::test_owner_or_support_required; last verified: 2026-06-30 | api.accounts.get (api.endpoint), schema.account (schema.object) |
