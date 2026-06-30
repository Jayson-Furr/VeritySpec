# Security Policy

VeritySpec is a product-specification toolchain. Please do not report sensitive
security issues in public issues.

For security concerns, contact the repository owner directly through GitHub.
Include enough detail to reproduce or understand the issue, affected versions,
and any known workaround.

## Product-Contract Security Controls

VeritySpec models release-relevant security controls as `security.control`
records in the `verity.pack.security` pack. The `security.control.release`
readiness gate blocks release readiness when a critical control is unverified:

- `coverage` must be `verified`,
- `verification.method` must not be `not-verified`, and
- `verification.evidence` must be a non-empty string.

Unverified critical controls surface as `readiness.unverified_critical` from
`verity readiness --strict` instead of only appearing in the generated
security report. See [docs/security-pack.md](docs/security-pack.md).

