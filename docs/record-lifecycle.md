# Record Lifecycle

Records use a small lifecycle:

```text
draft -> review -> ready -> deprecated -> removed
```

## Statuses

- `draft`: still being shaped and not release-ready.
- `review`: ready for contract review.
- `ready`: accepted as part of the active product contract.
- `deprecated`: still present, but should not be used by new records.
- `removed`: no active record should reference it.

Validation fails on references to removed records and warns on references to
deprecated records. Strict mode escalates warnings to errors.

