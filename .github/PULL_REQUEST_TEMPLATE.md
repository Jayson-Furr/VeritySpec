## Summary

Describe what changed and why.

## Verification

- [ ] `PYTHONPATH=src python3 -m unittest discover -s tests -v`
- [ ] `PYTHONPATH=src python3 -m verityspec validate examples/basic`
- [ ] `PYTHONPATH=src python3 -m verityspec lint examples/basic --strict`
- [ ] `PYTHONPATH=src python3 -m verityspec readiness examples/basic --strict`

